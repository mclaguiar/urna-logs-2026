"""Testes de parse/hash do .vsc.

O caso sintético não usa ZIP do TSE. O piloto AC 1º só roda se o arquivo
estiver em data/raw.
"""

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
    assert r.erro == ""
    assert "Ed521 ok" in r.hw_sig_msg
