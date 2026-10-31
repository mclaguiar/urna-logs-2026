"""Assinatura de hardware do `-vota.vsc` (Ed521, UE2020/UE2022).

O certificado embutido é conferido com a AC publicada (UE2020 ou UE2022).
Cada hash do `.vsc` e a autoassinatura são conferidos com a chave desse
certificado. A mensagem assinada é SHA-512 do hash já gravado no arquivo,
como nos scripts públicos do formato da urna. Não valida a chave de software
da cerimônia.

ECPy com a curva Ed521 é dependência opcional (`pip install -e ".[hw]"`).
"""

from __future__ import annotations

import base64
import hashlib
from functools import lru_cache

_OID_ED521 = "1.3.6.1.4.1.44588.2.1"
_OID_CN = "2.5.4.3"

# Certificados públicos da AC da urna (dpc.acue2020.tse.jus.br), usados só
# para conferir o emissor do certificado embutido no `.vsc`.
_AC_UE2020_B64 = """
MIIDITCCAoegAwIBAgIBBTAMBgorBgEEAYLcLAIBMIGCMRMwEQYDVQQDDApBQyBV
Uk5BIHYyMQswCQYDVQQIDAJERjELMAkGA1UEBhMCQlIxIjAgBgkqhkiG9w0BCQEW
E2FjdXJuYXYyQHRzZS5qdXMuYnIxDDAKBgNVBAoMA1RTRTEMMAoGA1UECwwDU1RJ
MREwDwYDVQQHDAhCcmFzaWxpYTAeFw0yMTA3MDUyMTMxNTZaFw0zNzA3MDEyMTMx
NTZaMIGBMRIwEAYDVQQDDAlBQyBVRTIwMjAxCzAJBgNVBAgMAkRGMQswCQYDVQQG
EwJCUjEiMCAGCSqGSIb3DQEJARYTYWN1ZTIwMjBAdHNlLmp1cy5icjEMMAoGA1UE
CgwDVFNFMQwwCgYDVQQLDANTVEkxETAPBgNVBAcMCEJyYXNpbGlhMFMwDAYKKwYB
BAGC3CwCAQNDAF09dk0RI6kU77+TiS2ztj0vPF03oPFKLTbUSQXMdCi5dDVRcd94
wqBk5jCzCLBhpH+wvVVxX8W2lBm/yS7VcK65AaOB8DCB7TAMBgNVHRMEBTADAQH/
MAsGA1UdDwQEAwIBBjAdBgNVHQ4EFgQUvLNUXe7qQy4egy6BKDy4rpSOQAswHwYD
VR0jBBgwFoAU0CVmxJEDSzqTE7MHSSHsqbUA4h8wPAYDVR0fBDUwMzAxoC+gLYYr
aHR0cDovL2xjci5hY3VybmF2Mi50c2UuanVzLmJyL2FjdXJuYXYyLmNybDBSBgNV
HSAESzBJMEcGAwAAADBAMD4GCCsGAQUFBwIBFjJodHRwOi8vZHBjLmFjdXJuYXYy
LnRzZS5qdXMuYnIvRFBDLVBDLUFDVVJOQVYyLlBERjAMBgorBgEEAYLcLAIBA4GF
ADuPH84sRDCnd7vmSDb3ae7qtPoUCcPbeOJb3zFtArAUm6ki7bV0Fa0jUri4LtEm
XYgrhOETAvqaRBlBk2vRH409gRbpHpMf9cvzgoMGAp+ShXHwlZ4m6XJuFXi77hMc
qGvoUFpGzp0yXzbP1uK1QMvfyVakWpczXQnvS3zay18ik9NFAA==
"""

_AC_UE2022_B64 = """
MIIDITCCAoegAwIBAgIBCDAMBgorBgEEAYLcLAIBMIGCMRMwEQYDVQQDDApBQyBV
Uk5BIHYyMQswCQYDVQQIDAJERjELMAkGA1UEBhMCQlIxIjAgBgkqhkiG9w0BCQEW
E2FjdXJuYXYyQHRzZS5qdXMuYnIxDDAKBgNVBAoMA1RTRTEMMAoGA1UECwwDU1RJ
MREwDwYDVQQHDAhCcmFzaWxpYTAeFw0yMzAyMjgxMzQ2NDlaFw0zOTAyMjQxMzQ2
NDlaMIGBMRIwEAYDVQQDDAlBQyBVRTIwMjIxCzAJBgNVBAgMAkRGMQswCQYDVQQG
EwJCUjEiMCAGCSqGSIb3DQEJARYTYWN1ZTIwMjJAdHNlLmp1cy5icjEMMAoGA1UE
CgwDVFNFMQwwCgYDVQQLDANTVEkxETAPBgNVBAcMCEJyYXNpbGlhMFMwDAYKKwYB
BAGC3CwCAQNDADcTiMAO2BJpyn3QVzU5bKqWqCBe/X4uls8WVXtSR15k6Sietkdo
S87iRk2Im3FVzsivJPK+TSGho6sVgFzfVdTsAKOB8DCB7TAMBgNVHRMEBTADAQH/
MAsGA1UdDwQEAwIBBjAdBgNVHQ4EFgQUu3xRfylKW5b5v2qWTE8lWnVfaYowHwYD
VR0jBBgwFoAU0CVmxJEDSzqTE7MHSSHsqbUA4h8wPAYDVR0fBDUwMzAxoC+gLYYr
aHR0cDovL2xjci5hY3VybmF2Mi50c2UuanVzLmJyL2FjdXJuYXYyLmNybDBSBgNV
HSAESzBJMEcGAwAAADBAMD4GCCsGAQUFBwIBFjJodHRwOi8vZHBjLmFjdXJuYXYy
LnRzZS5qdXMuYnIvRFBDLVBDLUFDVVJOQVYyLlBERjAMBgorBgEEAYLcLAIBA4GF
AChtHrhxscJ/SiePj3cCI/aPt5uJxC43PR6FjNENukBYxwkkWvFRbPblU/2muJZM
82ezEJtfcQ+3hWHoIZXKnkdTASSo0OX4TwykkFSb3/jX+D65ePsKUPGmYyWzt05A
+appfWxFCmWlib09waOnIQ6NmmrNPW8GGgaCiU54Xc3mElhTAA==
"""

_EMISSORES_B64 = {
    "AC UE2020": _AC_UE2020_B64,
    "AC UE2022": _AC_UE2022_B64,
}


def _b(data) -> bytes:
    if isinstance(data, bytes):
        return data
    return bytes(data)


def _der_items(buf: bytes):
    i = 0
    n = len(buf)
    while i < n:
        start = i
        tag = buf[i]
        i += 1
        ln = buf[i]
        i += 1
        if ln & 0x80:
            nbytes = ln & 0x7f
            ln = int.from_bytes(buf[i : i + nbytes], "big")
            i += nbytes
        content = buf[i : i + ln]
        i += ln
        yield tag, content, buf[start:i]


def _oid_str(content: bytes) -> str:
    first = content[0]
    parts = [str(first // 40), str(first % 40)]
    val = 0
    for byte in content[1:]:
        val = (val << 7) | (byte & 0x7F)
        if not byte & 0x80:
            parts.append(str(val))
            val = 0
    return ".".join(parts)


def _pem_to_der(data: bytes) -> bytes:
    raw = _b(data).strip()
    if raw.startswith(b"-----BEGIN"):
        body = b"".join(
            line.strip()
            for line in raw.splitlines()
            if line and not line.startswith(b"-----")
        )
        return base64.b64decode(body)
    return raw


def _cert_partes(der: bytes):
    body = next(_der_items(der))[1]
    partes = list(_der_items(body))
    tbs_full = partes[0][2]
    tbs = partes[0][1]
    sig_alg = partes[1][1]
    sig = partes[2][1][1:]
    campos = list(_der_items(tbs))
    if campos and campos[0][0] == 0xA0:
        emissor, spki = campos[3][1], campos[6][1]
    else:
        emissor, spki = campos[2][1], campos[5][1]
    return tbs_full, sig_alg, sig, emissor, spki


def _alg_oid(alg_content: bytes) -> str:
    return _oid_str(next(_der_items(alg_content))[1])


def _common_name(name_content: bytes) -> str:
    for _, rdn, _ in _der_items(name_content):
        for _, atv, _ in _der_items(rdn):
            seq = list(_der_items(atv))
            if _oid_str(seq[0][1]) == _OID_CN:
                return seq[1][1].decode("utf-8", "replace")
    return ""


def _chave_spki(spki: bytes):
    partes = list(_der_items(spki))
    oid = _alg_oid(partes[0][1])
    ponto = partes[1][1][1:]
    return oid, ponto


def _eddsa():
    from ecpy.eddsa import EDDSA

    return EDDSA(hashlib.shake_256, hash_len=132)


def _chave_ed521(ponto: bytes):
    from ecpy.curves import Curve
    from ecpy.keys import ECPublicKey

    curva = Curve.get_curve("Ed521")
    return ECPublicKey(curva.decode_point(ponto))


def conferir_ed521(mensagem: bytes, assinatura: bytes, ponto: bytes) -> bool:
    """Confere uma assinatura Ed521. `mensagem` já é o bloco assinado."""
    try:
        chave = _chave_ed521(ponto)
        return bool(_eddsa().verify(_b(mensagem), _b(assinatura), chave))
    except Exception:
        return False


@lru_cache(maxsize=4)
def _chave_emissora(nome: str):
    der = base64.b64decode("".join(_EMISSORES_B64[nome].split()))
    _, _, _, _, spki = _cert_partes(der)
    oid, ponto = _chave_spki(spki)
    if oid != _OID_ED521:
        raise ValueError(f"emissor {nome} não é Ed521 ({oid})")
    return _chave_ed521(ponto)


def _mensagem(hash_arquivo: bytes) -> bytes:
    return hashlib.sha512(_b(hash_arquivo)).digest()


def verificar_hw(ent: dict, arquivos: list[dict]) -> tuple[bool, str]:
    """Confere certificado, autoassinatura e cada hash assinado no HW."""
    info = ent["assinaturaHW"]["informacaoChave"]
    if not (isinstance(info, tuple) and info[0] == "certificadoDigital"):
        return False, "sem certificadoDigital HW"
    try:
        der = _pem_to_der(info[1])
        tbs, sig_alg, assinatura_cert, emissor, spki = _cert_partes(der)
        oid, ponto = _chave_spki(spki)
    except Exception as exc:
        return False, f"certificado HW ilegível: {exc}"
    if oid != _OID_ED521 or _alg_oid(sig_alg) != _OID_ED521:
        return False, f"algoritmo do certificado não é Ed521 ({oid})"
    nome = _common_name(emissor)
    if nome not in _EMISSORES_B64:
        return False, f"emissor HW fora das AC UE2020/UE2022 ({nome or 'sem CN'})"
    try:
        chave_urna = _chave_ed521(ponto)
        chave_ac = _chave_emissora(nome)
        verificador = _eddsa()
    except ImportError:
        raise
    except Exception as exc:
        return False, f"chave Ed521: {exc}"

    def _ok(mensagem: bytes, assinatura: bytes, chave) -> bool:
        try:
            return bool(verificador.verify(_b(mensagem), _b(assinatura), chave))
        except Exception:
            return False

    if not _ok(tbs, assinatura_cert, chave_ac):
        return False, f"certificado não confere com {nome}"

    for item in arquivos:
        nome_arq = str(item["nomeArquivo"])
        bloco = item["assinatura"]
        if not _ok(_mensagem(bloco["hash"]), bloco["assinatura"], chave_urna):
            return False, f"assinatura HW inválida: {nome_arq}"

    auto = ent["assinaturaHW"]["autoAssinado"]["assinatura"]
    if not _ok(_mensagem(auto["hash"]), auto["assinatura"], chave_urna):
        return False, "autoassinatura HW inválida"
    return True, f"Ed521 ok ({len(arquivos)} arquivos + auto + {nome})"
