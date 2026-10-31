"""Testes de parse/hash do .vsc.

O caso sintético não usa ZIP do TSE. O piloto AC 1º só roda se o arquivo
estiver em data/raw.
"""

import base64
import hashlib
import io
import zipfile
from pathlib import Path

import pytest

from urna_logs.config import zip_path
from urna_logs.verificar_vsc import (
    _assinatura_codec,
    join_key_from_stem,
    run_verificar_vsc,
    verificar_stem,
)

_STEM = "o03220ac0101500020088"


def test_join_key_from_stem():
    assert join_key_from_stem("o03220ac0101500020088") == "AC:01015:0002:0088"
    assert join_key_from_stem("x") is None


def _arquivo_assinado(nome: str, data: bytes) -> dict:
    return {
        "nomeArquivo": nome,
        "assinatura": {
            "tamanho": 1,
            "hash": hashlib.sha512(data).digest(),
            "assinatura": b"\x00",
        },
    }


def _bloco_assinatura(payload: bytes) -> dict:
    return {
        "dataHoraCriacao": "20261030T120000",
        "versao": 2,
        "autoAssinado": {
            "usuario": {"nomeUsuario": "secao", "serial": 20261030},
            "algoritmoHash": {"algoritmo": 4},
            "algoritmoAssinatura": {"algoritmo": 4, "bits": 521},
            "assinatura": {
                "tamanho": 1,
                "hash": hashlib.sha512(payload).digest(),
                "assinatura": b"\x00",
            },
        },
        "conteudoAutoAssinado": payload,
        "informacaoChave": ("tagChaves", "202610301200"),
    }


def _vsc_bytes(files: dict[str, bytes]) -> bytes:
    """`.vsc` sintético: hashes SHA-512 corretos, sem assinatura Ed521."""
    codec = _assinatura_codec()
    payload = codec.encode(
        "Assinatura",
        {"arquivosAssinados": [_arquivo_assinado(n, d) for n, d in files.items()]},
    )
    return codec.encode(
        "EntidadeAssinaturaEcourna",
        {
            "assinaturaSW": _bloco_assinatura(payload),
            "assinaturaHW": _bloco_assinatura(payload),
            "origemAssinaturaHW": {
                "modeloEquipamento": 20,
                "algoritmoAssinatura": 4,
            },
        },
    )


def _zip_urna(files: dict[str, bytes], vsc: bytes) -> zipfile.ZipFile:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, data in files.items():
            zf.writestr(name, data)
        zf.writestr(f"{_STEM}-vota.vsc", vsc)
    buf.seek(0)
    return zipfile.ZipFile(buf, "r")


def _members() -> dict[str, str]:
    return {
        "bu.dat": f"{_STEM}-bu.dat",
        "rdv.dat": f"{_STEM}-rdv.dat",
        "log.jez": f"{_STEM}-log.jez",
        "vota.vsc": f"{_STEM}-vota.vsc",
    }


def test_nivel1_intacto_e_bu_adulterado():
    files = {
        f"{_STEM}-bu.dat": b"bu-original",
        f"{_STEM}-rdv.dat": b"rdv-original",
        f"{_STEM}-log.jez": b"log-original",
    }
    vsc = _vsc_bytes(files)

    intacto = verificar_stem(_zip_urna(files, vsc), _STEM, _members(), nivel=1)
    assert intacto.parse_ok
    assert intacto.auto_hash_hw_ok is True
    assert intacto.auto_hash_sw_ok is True
    assert intacto.n_hash_fail == 0
    assert intacto.criticos_ok is True
    assert intacto.nivel_ok == 1

    adulterado = dict(files)
    adulterado[f"{_STEM}-bu.dat"] = b"xu-original"
    ruim = verificar_stem(_zip_urna(adulterado, vsc), _STEM, _members(), nivel=1)
    assert ruim.n_hash_fail == 1
    assert ruim.criticos_ok is False
    assert ruim.nivel_ok == 0
    assert "bu.dat=hash_fail" in ruim.criticos_detalhe
    assert "rdv.dat=ok" in ruim.criticos_detalhe
    assert "log.jez=ok" in ruim.criticos_detalhe


@pytest.mark.skipif(
    not zip_path("AC", 1).exists(),
    reason="ZIP AC 1º não presente",
)
def test_verificar_vsc_ac_limit():
    paths = run_verificar_vsc(["AC"], 1, nivel=1, limit=5)
    assert paths
    pq = Path("reports/verificar_vsc_AC_1t.parquet")
    assert pq.exists()
    import pandas as pd

    df = pd.read_parquet(pq)
    assert len(df) == 5
    assert df["tem_vsc"].all()
    assert df["parse_ok"].all()
    assert (df["nivel_ok"] >= 1).all()
    assert df["n_hash_fail"].sum() == 0


def test_padrao_faz_hash_e_ed521():
    files = {
        f"{_STEM}-bu.dat": b"bu-original",
        f"{_STEM}-rdv.dat": b"rdv-original",
        f"{_STEM}-log.jez": b"log-original",
    }
    r = verificar_stem(_zip_urna(files, _vsc_bytes(files)), _STEM, _members())
    assert r.nivel_ok == 1
    assert r.n_hash_fail == 0
    assert r.hw_sig_ok is False
    assert "certificado" in r.erro


def test_nivel2_explicito_nao_confere_hash_do_zip():
    files = {
        f"{_STEM}-bu.dat": b"bu-original",
        f"{_STEM}-rdv.dat": b"rdv-original",
        f"{_STEM}-log.jez": b"log-original",
    }
    r = verificar_stem(
        _zip_urna(files, _vsc_bytes(files)), _STEM, _members(), nivel=2
    )
    assert r.n_presentes == 0
    assert r.criticos_ok is None
    assert r.nivel_ok == 0
    assert r.hw_sig_ok is False
    assert "certificado" in r.erro


def test_ed521_rejeita_octeto_alterado():
    pytest.importorskip("ecpy")
    from ecpy.curves import Curve
    from ecpy.eddsa import EDDSA
    from ecpy.keys import ECPrivateKey

    from urna_logs.vsc_hw import conferir_ed521

    curva = Curve.get_curve("Ed521")
    privada = ECPrivateKey(123456789, curva)
    signer = EDDSA(hashlib.shake_256, hash_len=132)
    publica = EDDSA.get_public_key(privada, hashlib.shake_256, 132)
    ponto = curva.encode_point(publica.W)
    mensagem = hashlib.sha512(b"hash-do-arquivo").digest()
    assinatura = signer.sign(mensagem, privada)
    assert conferir_ed521(mensagem, assinatura, ponto)
    alterada = bytearray(assinatura)
    alterada[0] ^= 0x01
    assert conferir_ed521(mensagem, bytes(alterada), ponto) is False


@pytest.mark.skipif(
    not zip_path("AC", 1).exists(),
    reason="ZIP AC 1º não presente",
)
def test_nivel2_ac_uma_secao():
    pytest.importorskip("ecpy")
    from urna_logs.verificar_vsc import _index_zip

    with zipfile.ZipFile(zip_path("AC", 1)) as zf:
        by_stem = _index_zip(zf)
        stem = next(s for s in sorted(by_stem) if "vota.vsc" in by_stem[s])
        r = verificar_stem(zf, stem, by_stem[stem])
    assert r.nivel_ok == 2
    assert r.n_hash_fail == 0
    assert r.criticos_ok is True
    assert r.hw_sig_ok is True
    assert r.hw_cadeia == "ok"
    assert r.erro == ""
    assert "Ed521 ok" in r.hw_sig_msg


def _der_len(n: int) -> bytes:
    if n < 0x80:
        return bytes([n])
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(raw)]) + raw


def _tlv(tag: int, content: bytes) -> bytes:
    return bytes([tag]) + _der_len(len(content)) + content


def _oid(oid: str) -> bytes:
    parts = [int(p) for p in oid.split(".")]
    body = bytearray([40 * parts[0] + parts[1]])
    for part in parts[2:]:
        enc = [part & 0x7F]
        part >>= 7
        while part:
            enc.append(0x80 | (part & 0x7F))
            part >>= 7
        body.extend(reversed(enc))
    return _tlv(0x06, bytes(body))


def _nome_cn(texto: str) -> bytes:
    atributo = _tlv(0x30, _oid("2.5.4.3") + _tlv(0x0C, texto.encode()))
    return _tlv(0x30, _tlv(0x31, atributo))


def _cert_p521(ponto: bytes, assinatura: bytes) -> tuple[bytes, bytes]:
    """Certificado mínimo ECDSA P-521 emitido pela AC URNA. Devolve (der, tbs)."""
    spki_alg = _tlv(0x30, _oid("1.2.840.10045.2.1") + _oid("1.3.132.0.35"))
    spki = _tlv(0x30, spki_alg + _tlv(0x03, b"\x00" + ponto))
    sigalg = _tlv(0x30, _oid("1.2.840.10045.4.3.4"))
    validade = _tlv(
        0x30,
        _tlv(0x17, b"160624030853Z") + _tlv(0x17, b"300303030853Z"),
    )
    tbs = _tlv(
        0x30,
        b"".join(
            (
                _tlv(0x02, b"\x01"),
                sigalg,
                _nome_cn("AC URNA"),
                validade,
                _nome_cn("ueao-teste"),
                spki,
            )
        ),
    )
    cert = _tlv(0x30, tbs + sigalg + _tlv(0x03, b"\x00" + assinatura))
    return cert, tbs


def _sig_ecdsa(priv, hash_arquivo: bytes) -> bytes:
    from ecpy.ecdsa import ECDSA

    return ECDSA(fmt="DER").sign(hashlib.sha512(hash_arquivo).digest(), priv)


def _chaves_p521(escalar: int):
    from ecpy.curves import Curve
    from ecpy.keys import ECPrivateKey

    curva = Curve.get_curve("secp521r1")
    privada = ECPrivateKey(escalar, curva)
    publica = privada.get_public_key()
    return privada, bytes(curva.encode_point(publica.W))


def test_ecdsa_rejeita_octeto_alterado():
    pytest.importorskip("ecpy")
    from urna_logs.vsc_hw import conferir_ecdsa

    privada, ponto = _chaves_p521(123456789)
    digest = hashlib.sha512(b"hash-do-arquivo").digest()
    from ecpy.ecdsa import ECDSA

    assinatura = ECDSA(fmt="DER").sign(digest, privada)
    assert conferir_ecdsa(digest, assinatura, ponto)
    alterada = bytearray(assinatura)
    alterada[-1] ^= 0x01
    assert conferir_ecdsa(digest, bytes(alterada), ponto) is False


def test_par_fora_da_tabela_nao_tenta_outro_algoritmo():
    from urna_logs.vsc_hw import verificar_hw

    ent = {
        "origemAssinaturaHW": {"modeloEquipamento": 15, "algoritmoAssinatura": 4},
        "assinaturaHW": {"informacaoChave": ("tagChaves", "202610301200")},
    }
    ok, cadeia, msg = verificar_hw(ent, [])
    assert ok is False
    assert cadeia == "falha"
    assert msg == "par modelo/algoritmo fora da tabela (15/4)"


def test_ecdsa_cadeia_pendente_nao_sobe_nivel_2():
    pytest.importorskip("ecpy")
    privada, ponto = _chaves_p521(987654321)
    files = {
        f"{_STEM}-bu.dat": b"bu-original",
        f"{_STEM}-rdv.dat": b"rdv-original",
        f"{_STEM}-log.jez": b"log-original",
    }
    cert, _tbs = _cert_p521(ponto, b"\x30\x06\x02\x01\x01\x02\x01\x01")
    codec = _assinatura_codec()
    assinados = []
    for nome, data in files.items():
        arquivo = _arquivo_assinado(nome, data)
        arquivo["assinatura"]["assinatura"] = _sig_ecdsa(
            privada, arquivo["assinatura"]["hash"]
        )
        assinados.append(arquivo)
    payload = codec.encode("Assinatura", {"arquivosAssinados": assinados})
    bloco = _bloco_assinatura(payload)
    bloco["autoAssinado"]["assinatura"]["assinatura"] = _sig_ecdsa(
        privada, bloco["autoAssinado"]["assinatura"]["hash"]
    )
    bloco["informacaoChave"] = ("certificadoDigital", cert)
    vsc = codec.encode(
        "EntidadeAssinaturaEcourna",
        {
            "assinaturaSW": _bloco_assinatura(payload),
            "assinaturaHW": bloco,
            "origemAssinaturaHW": {
                "modeloEquipamento": 15,
                "algoritmoAssinatura": 2,
            },
        },
    )
    from urna_logs import vsc_hw

    guardado = dict(vsc_hw._AC_ECDSA_B64)
    vsc_hw._AC_ECDSA_B64.clear()
    vsc_hw._chave_ac_ecdsa.cache_clear()
    vsc_hw._validade_ac_urna.cache_clear()
    try:
        r = verificar_stem(_zip_urna(files, vsc), _STEM, _members())
    finally:
        vsc_hw._AC_ECDSA_B64.clear()
        vsc_hw._AC_ECDSA_B64.update(guardado)
        vsc_hw._chave_ac_ecdsa.cache_clear()
        vsc_hw._validade_ac_urna.cache_clear()
    assert r.n_hash_fail == 0
    assert r.criticos_ok is True
    assert r.hw_sig_ok is True
    assert r.hw_cadeia == "pendente"
    assert r.nivel_ok == 1
    assert r.erro == ""
    assert "ECDSA cadeia pendente" in r.hw_sig_msg


def test_ecdsa_com_ac_sobe_nivel_2_e_assinatura_ruim_falha():
    pytest.importorskip("ecpy")
    from ecpy.ecdsa import ECDSA

    from urna_logs import vsc_hw

    urna, ponto_urna = _chaves_p521(111)
    ac, ponto_ac = _chaves_p521(222)
    h = hashlib.sha512(b"bu").digest()
    sig = _sig_ecdsa(urna, h)
    cert_ac, _tbs_ac = _cert_p521(ponto_ac, b"\x30\x06\x02\x01\x01\x02\x01\x01")
    _rascunho, tbs_urna = _cert_p521(ponto_urna, b"\x00")
    sig_cert = ECDSA(fmt="DER").sign(hashlib.sha512(tbs_urna).digest(), ac)
    cert_urna, tbs_assinado = _cert_p521(ponto_urna, sig_cert)
    assert tbs_assinado == tbs_urna
    arquivos = [
        {"nomeArquivo": "bu.dat", "assinatura": {"hash": h, "assinatura": sig}}
    ]
    auto_h = hashlib.sha512(b"auto").digest()
    ent = {
        "origemAssinaturaHW": {"modeloEquipamento": 13, "algoritmoAssinatura": 2},
        "assinaturaHW": {
            "informacaoChave": ("certificadoDigital", cert_urna),
            "autoAssinado": {
                "assinatura": {
                    "hash": auto_h,
                    "assinatura": _sig_ecdsa(urna, auto_h),
                }
            },
        },
    }
    blob = base64.b64encode(cert_ac).decode()
    guardado = dict(vsc_hw._AC_ECDSA_B64)
    vsc_hw._AC_ECDSA_B64["AC URNA"] = blob
    vsc_hw._chave_ac_ecdsa.cache_clear()
    vsc_hw._validade_ac_urna.cache_clear()
    try:
        ok, cadeia, msg = vsc_hw.verificar_hw(ent, arquivos)
        assert ok is True
        assert cadeia == "ok"
        assert msg.startswith("ECDSA ok")
        ruim = [dict(arquivos[0])]
        alterada = bytearray(ruim[0]["assinatura"]["assinatura"])
        alterada[-1] ^= 0x01
        ruim[0]["assinatura"] = dict(ruim[0]["assinatura"])
        ruim[0]["assinatura"]["assinatura"] = bytes(alterada)
        ok, cadeia, msg = vsc_hw.verificar_hw(ent, ruim)
        assert ok is False
        assert cadeia == "falha"
        assert msg == "assinatura HW inválida: bu.dat"
    finally:
        vsc_hw._AC_ECDSA_B64.clear()
        vsc_hw._AC_ECDSA_B64.update(guardado)
        vsc_hw._chave_ac_ecdsa.cache_clear()
        vsc_hw._validade_ac_urna.cache_clear()


def test_certificado_ecdsa_nao_entra_no_caminho_ed521():
    pytest.importorskip("ecpy")
    from urna_logs.vsc_hw import verificar_hw

    _privada, ponto = _chaves_p521(333)
    cert, _tbs = _cert_p521(ponto, b"\x30\x06\x02\x01\x01\x02\x01\x01")
    ent = {
        "origemAssinaturaHW": {"modeloEquipamento": 20, "algoritmoAssinatura": 4},
        "assinaturaHW": {
            "informacaoChave": ("certificadoDigital", cert),
            "autoAssinado": {"assinatura": {"hash": b"\x00" * 64, "assinatura": b"\x00"}},
        },
    }
    ok, cadeia, msg = verificar_hw(ent, [])
    assert ok is False
    assert cadeia == "falha"
    assert "não confere com o algoritmo declarado (eddsa" in msg


def test_ac_ue2020_continua_ed521():
    pytest.importorskip("ecpy")
    from urna_logs.vsc_hw import _chave_emissora

    _chave_emissora.cache_clear()
    chave = _chave_emissora("AC UE2020")
    assert chave.W is not None
