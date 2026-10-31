"""Assinatura de hardware do `-vota.vsc`.

O par declarado em `origemAssinaturaHW` escolhe o verificador. Não há segunda
tentativa se o certificado for de outro algoritmo.

- UE2020/UE2022 e `eddsa`: Ed521, certificado conferido com a AC UE2020 ou UE2022.
- UE2013/UE2015 e `ecdsa`: ECDSA P-521. A assinatura dos arquivos é conferida
  com a chave do certificado. A cadeia confere o certificado da urna com a
  AC URNA publicada em `_AC_ECDSA_B64`. Sem essa chave, o resultado é cadeia
  pendente. A conta não olha a data de validade do certificado da AC.

A mensagem assinada dos arquivos é SHA-512 do hash já gravado no arquivo.
No ECDSA esse digest entra direto na verificação. A assinatura do certificado
ECDSA, quando a AC está fixada, é SHA-512 do TBS. Não valida a chave de
software da cerimônia.

ECPy é dependência opcional (`pip install -e ".[hw]"`).
"""

from __future__ import annotations

import base64
import hashlib
from functools import lru_cache

_OID_ED521 = "1.3.6.1.4.1.44588.2.1"
_OID_EC_PUBLIC = "1.2.840.10045.2.1"
_OID_SECP521R1 = "1.3.132.0.35"
_OID_ECDSA_SHA512 = "1.2.840.10045.4.3.4"
_OID_CN = "2.5.4.3"
_CN_AC_URNA = "AC URNA"

# modeloEquipamento, algoritmoAssinatura → caminho. Fora daqui é inconsistência.
_CAMINHOS = {
    (13, 2): "ecdsa",
    (15, 2): "ecdsa",
    (20, 4): "eddsa",
    (22, 4): "eddsa",
}

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

# AC URNA (ECDSA P-521), http://acurna.tse.jus.br/crt/acurna.crt
# Emissor AC RAIZ UE. Identificador da chave
# cdaaf4b29701b3f0deb2b54258594a6d34ada48a.
# Validade do certificado: 2011-07-22 a 2026-07-18.
_AC_URNA_B64 = """
MIID+jCCA1ygAwIBAgIBAzAKBggqhkjOPQQDBDCBgjELMAkGA1UEBhMCQlIxDDAK
BgNVBAoTA1RTRTEMMAoGA1UECxMDU1RJMRMwEQYDVQQDEwpBQyBSQUlaIFVFMQsw
CQYDVQQIEwJERjERMA8GA1UEBxMIQnJhc2lsaWExIjAgBgkqhkiG9w0BCQEWE2Fj
cmFpenVlQHRzZS5qdXMuYnIwHhcNMTEwNzIyMjE1OTU3WhcNMjYwNzE4MjE1OTU3
WjB9MRAwDgYDVQQDEwdBQyBVUk5BMQswCQYDVQQIEwJERjELMAkGA1UEBhMCQlIx
IDAeBgkqhkiG9w0BCQEWEWFjdXJuYUB0c2UuanVzLmJyMQwwCgYDVQQKEwNUU0Ux
DDAKBgNVBAsTA1NUSTERMA8GA1UEBxMIQnJhc2lsaWEwgZswEAYHKoZIzj0CAQYF
K4EEACMDgYYABACBR0E65ux46ll8Z41Fi0QJf+LWQqUZDI2wIvB4+F9vHqrw0/tb
6pasdXwwxxdRia5oI21UrKsN2f0VxCtWGPAzzwHPPXSY4w9bSIg/evLDXFZ9QNKK
EWt83xzz1U6nsd2H+XI2sNSOWQS485ZYQ7nnThRgPhRsYsbCKb6Gmt7JTNudkqOC
AYIwggF+MAwGA1UdEwQFMAMBAf8wga8GA1UdIwSBpzCBpIAUhmiDe7vjSM0ZthAw
pInV395nQsChgYikgYUwgYIxCzAJBgNVBAYTAkJSMQwwCgYDVQQKEwNUU0UxDDAK
BgNVBAsTA1NUSTETMBEGA1UEAxMKQUMgUkFJWiBVRTELMAkGA1UECBMCREYxETAP
BgNVBAcTCEJyYXNpbGlhMSIwIAYJKoZIhvcNAQkBFhNhY3JhaXp1ZUB0c2UuanVz
LmJyggEBMB0GA1UdDgQWBBTNqvSylwGz8N6ytUJYWUptNK2kijALBgNVHQ8EBAMC
AYYwPAYDVR0fBDUwMzAxoC+gLYYraHR0cDovL2xjci5hY3JhaXp1ZS50c2UuanVz
LmJyL2FjcmFpenVlLmNybDBSBgNVHSAESzBJMEcGAwAAADBAMD4GCCsGAQUFBwIB
FjJodHRwOi8vZHBjLmFjcmFpenVlLnRzZS5qdXMuYnIvRFBDLVBDLUFDUkFJWlVF
LnBkZjAKBggqhkjOPQQDBAOBiwAwgYcCQS2Qnvfn3wF8Ft96nAjZH5tp/0VKwp0j
iJYy1+7Bx5PB94lW6D7Hqvfe6XClC9faSrNTQL1XFdZg2yw/hMROUb2uAkIBe8l4
fiGIaXNVTLstkxNGYoXCjJvGtBc1zeFBRXKA3S95lskEMn8QJ06vYRK6PiUu5foM
yaLcujRjcz9Mb7zpTfo=
"""

_AC_ECDSA_B64: dict[str, str] = {_CN_AC_URNA: _AC_URNA_B64}


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


def _chave_spki(spki: bytes) -> tuple[str, str, bytes]:
    """OID do algoritmo, OID da curva (vazio se o campo não traz) e ponto."""
    partes = list(_der_items(spki))
    alg_items = list(_der_items(partes[0][1]))
    oid = _oid_str(alg_items[0][1])
    curva = ""
    if len(alg_items) > 1 and alg_items[1][0] == 0x06:
        curva = _oid_str(alg_items[1][1])
    ponto = partes[1][1][1:]
    return oid, curva, ponto


def _eddsa():
    from ecpy.eddsa import EDDSA

    return EDDSA(hashlib.shake_256, hash_len=132)


def _chave_ed521(ponto: bytes):
    from ecpy.curves import Curve
    from ecpy.keys import ECPublicKey

    curva = Curve.get_curve("Ed521")
    return ECPublicKey(curva.decode_point(ponto))


def _chave_p521(ponto: bytes):
    from ecpy.curves import Curve
    from ecpy.keys import ECPublicKey

    curva = Curve.get_curve("secp521r1")
    return ECPublicKey(curva.decode_point(ponto))


def _ecdsa():
    from ecpy.ecdsa import ECDSA

    return ECDSA(fmt="DER")


def conferir_ed521(mensagem: bytes, assinatura: bytes, ponto: bytes) -> bool:
    """Confere uma assinatura Ed521. `mensagem` já é o bloco assinado."""
    try:
        chave = _chave_ed521(ponto)
        return bool(_eddsa().verify(_b(mensagem), _b(assinatura), chave))
    except Exception:
        return False


def conferir_ecdsa(digest: bytes, assinatura: bytes, ponto: bytes) -> bool:
    """Confere ECDSA P-521. `digest` já é o SHA-512 que a assinatura cobre."""
    try:
        chave = _chave_p521(ponto)
        return bool(_ecdsa().verify(_b(digest), _b(assinatura), chave))
    except Exception:
        return False


@lru_cache(maxsize=4)
def _chave_emissora(nome: str):
    der = base64.b64decode("".join(_EMISSORES_B64[nome].split()))
    _, _, _, _, spki = _cert_partes(der)
    oid, _curva, ponto = _chave_spki(spki)
    if oid != _OID_ED521:
        raise ValueError(f"emissor {nome} não é Ed521 ({oid})")
    return _chave_ed521(ponto)


@lru_cache(maxsize=2)
def _chave_ac_ecdsa(blob: str):
    der = base64.b64decode("".join(blob.split()))
    _, _, _, _, spki = _cert_partes(der)
    oid, curva, ponto = _chave_spki(spki)
    if oid != _OID_EC_PUBLIC or curva != _OID_SECP521R1:
        raise ValueError(f"AC URNA não é ECDSA P-521 ({oid}, {curva or 'sem curva'})")
    return _chave_p521(ponto)


def _data_utc(bruto: bytes) -> str:
    texto = bruto.decode()
    ano = int(texto[:2])
    ano += 2000 if ano < 50 else 1900
    return f"{ano:04d}-{texto[2:4]}-{texto[4:6]}"


@lru_cache(maxsize=2)
def _validade_ac_urna() -> str:
    """Data final do certificado da AC URNA, ou string vazia se não der para ler."""
    blob = _AC_ECDSA_B64.get(_CN_AC_URNA, "")
    if not blob.strip():
        return ""
    try:
        der = base64.b64decode("".join(blob.split()))
        body = next(_der_items(der))[1]
        tbs = list(_der_items(body))[0][1]
        campos = list(_der_items(tbs))
        idx = 1 if campos and campos[0][0] == 0xA0 else 0
        tempos = list(_der_items(campos[idx + 3][1]))
        return _data_utc(tempos[1][1])
    except Exception:
        return ""


def _mensagem(hash_arquivo: bytes) -> bytes:
    return hashlib.sha512(_b(hash_arquivo)).digest()


def _par_declarado(ent: dict) -> tuple[str | None, str]:
    origem = ent.get("origemAssinaturaHW") or {}
    modelo = origem.get("modeloEquipamento")
    alg = origem.get("algoritmoAssinatura")
    try:
        par = (int(modelo), int(alg))
    except (TypeError, ValueError):
        return None, f"par modelo/algoritmo fora da tabela ({modelo}/{alg})"
    caminho = _CAMINHOS.get(par)
    if caminho is None:
        return None, f"par modelo/algoritmo fora da tabela ({par[0]}/{par[1]})"
    return caminho, ""


def _assinaturas_com(chave, verificar, arquivos: list[dict], auto: dict) -> str:
    """Devolve mensagem de erro, ou string vazia se arquivo e auto conferem."""
    for item in arquivos:
        nome_arq = str(item["nomeArquivo"])
        bloco = item["assinatura"]
        if not verificar(_mensagem(bloco["hash"]), bloco["assinatura"], chave):
            return f"assinatura HW inválida: {nome_arq}"
    if not verificar(_mensagem(auto["hash"]), auto["assinatura"], chave):
        return "autoassinatura HW inválida"
    return ""


def _verificar_eddsa(tbs, sig_alg, assinatura_cert, emissor, ponto, arquivos, auto):
    oid_assinatura = _alg_oid(sig_alg)
    nome = _common_name(emissor)
    if nome not in _EMISSORES_B64:
        return False, "falha", f"emissor HW fora das AC UE2020/UE2022 ({nome or 'sem CN'})"
    try:
        chave_urna = _chave_ed521(ponto)
        chave_ac = _chave_emissora(nome)
        verificador = _eddsa()
    except ImportError:
        raise
    except Exception as exc:
        return False, "falha", f"chave Ed521: {exc}"

    def _ok(mensagem: bytes, assinatura: bytes, chave) -> bool:
        try:
            return bool(verificador.verify(_b(mensagem), _b(assinatura), chave))
        except Exception:
            return False

    if oid_assinatura != _OID_ED521:
        return (
            False,
            "falha",
            f"certificado não confere com o algoritmo declarado (eddsa, {oid_assinatura})",
        )
    if not _ok(tbs, assinatura_cert, chave_ac):
        return False, "falha", f"certificado não confere com {nome}"
    erro = _assinaturas_com(chave_urna, _ok, arquivos, auto)
    if erro:
        return False, "falha", erro
    return True, "ok", f"Ed521 ok ({len(arquivos)} arquivos + auto + {nome})"


def _cadeia_ecdsa(tbs: bytes, assinatura_cert: bytes) -> str:
    """`ok` com a AC fixada, `pendente` sem ela, `falha` se a conta não fecha."""
    blob = _AC_ECDSA_B64.get(_CN_AC_URNA, "")
    if not blob.strip():
        return "pendente"
    try:
        chave_ac = _chave_ac_ecdsa(blob)
        verificador = _ecdsa()
    except ImportError:
        raise
    except Exception as exc:
        return f"falha:{exc}"
    digest = hashlib.sha512(_b(tbs)).digest()
    try:
        fecha = bool(verificador.verify(digest, _b(assinatura_cert), chave_ac))
    except Exception:
        fecha = False
    if not fecha:
        return "falha"
    return "ok"


def _verificar_ecdsa(tbs, assinatura_cert, emissor, ponto, arquivos, auto):
    nome = _common_name(emissor)
    if nome != _CN_AC_URNA:
        return False, "falha", f"emissor HW fora da AC URNA ({nome or 'sem CN'})"
    try:
        chave_urna = _chave_p521(ponto)
        verificador = _ecdsa()
    except ImportError:
        raise
    except Exception as exc:
        return False, "falha", f"chave ECDSA: {exc}"

    def _ok(digest: bytes, assinatura: bytes, chave) -> bool:
        try:
            return bool(verificador.verify(_b(digest), _b(assinatura), chave))
        except Exception:
            return False

    erro = _assinaturas_com(chave_urna, _ok, arquivos, auto)
    if erro:
        return False, "falha", erro
    cadeia = _cadeia_ecdsa(tbs, assinatura_cert)
    if cadeia == "pendente":
        return (
            True,
            "pendente",
            f"ECDSA cadeia pendente ({len(arquivos)} arquivos + auto + AC URNA)",
        )
    if cadeia != "ok":
        detalhe = cadeia.removeprefix("falha:")
        msg = "certificado não confere com AC URNA"
        if detalhe and detalhe != "falha":
            msg = f"{msg}: {detalhe}"
        return False, "falha", msg
    ate = _validade_ac_urna()
    extra = f", certificado até {ate}" if ate else ""
    return True, "ok", f"ECDSA ok ({len(arquivos)} arquivos + auto + AC URNA{extra})"


def verificar_hw(ent: dict, arquivos: list[dict]) -> tuple[bool, str, str]:
    """Confere o HW pelo par declarado.

    Devolve `(assinatura_ok, cadeia, mensagem)`. `cadeia` é `ok`, `pendente`
    ou `falha`. `assinatura_ok` só fica verdadeiro quando os arquivos e a
    autoassinatura conferem com a chave do certificado.
    """
    caminho, erro_par = _par_declarado(ent)
    if caminho is None:
        return False, "falha", erro_par
    info = ent["assinaturaHW"]["informacaoChave"]
    if not (isinstance(info, tuple) and info[0] == "certificadoDigital"):
        return False, "falha", "sem certificadoDigital HW"
    try:
        der = _pem_to_der(info[1])
        tbs, sig_alg, assinatura_cert, emissor, spki = _cert_partes(der)
        oid, curva, ponto = _chave_spki(spki)
    except Exception as exc:
        return False, "falha", f"certificado HW ilegível: {exc}"
    auto = ent["assinaturaHW"]["autoAssinado"]["assinatura"]
    if caminho == "eddsa":
        if oid != _OID_ED521:
            return (
                False,
                "falha",
                f"certificado não confere com o algoritmo declarado (eddsa, {oid})",
            )
        return _verificar_eddsa(
            tbs, sig_alg, assinatura_cert, emissor, ponto, arquivos, auto
        )
    if oid != _OID_EC_PUBLIC or curva != _OID_SECP521R1 or _alg_oid(sig_alg) != _OID_ECDSA_SHA512:
        visto = curva or oid
        return (
            False,
            "falha",
            f"certificado não confere com o algoritmo declarado (ecdsa, {visto})",
        )
    return _verificar_ecdsa(tbs, assinatura_cert, emissor, ponto, arquivos, auto)
