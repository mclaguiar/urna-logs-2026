"""Amostra reprodutível de logs e o molde de cada mensagem.

Os detectores só reconhecem frases que este catálogo tiver visto.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from urna_logs.config import PROJECT_ROOT, zip_path
from urna_logs.parse_log import _events_from_jez_bytes
from urna_logs.zip_logs import list_log_members, read_member_from_open_zip

EVENTOS_MD = PROJECT_ROOT / "eventos_log.md"
_DIGITO = re.compile(r"\d+")
_ESPACO = re.compile(r"\s+")

# Frases vistas em eventos_log.md. Ausente na amostra não entra.
FRASES: dict[str, str] = {
    "voto_computado": "O voto do eleitor foi computado",
    "ajuste_hora": "Data e hora atualizada",
    "reinicio": "Reiniciando a urna",
    "contingencia_inicio": "Início do procedimento de contingência",
    "contingencia_modo": "Modo de carga da UE - Urna de contingência",
}


def molde(mensagem: str) -> str:
    texto = _DIGITO.sub("N", mensagem)
    return _ESPACO.sub(" ", texto).strip()


def amostrar(uf: str, turno: int, ano: int, *, n: int = 50) -> list[tuple[str, int, str]]:
    """Os N primeiros logs, em ordem de nome. Devolve (molde, contagem, exemplo)."""
    import zipfile

    zpath = zip_path(uf, turno, ano)
    membros = sorted(list_log_members(zpath))[:n]
    contagem: Counter[str] = Counter()
    exemplo: dict[str, str] = {}
    with zipfile.ZipFile(zpath) as zf:
        for membro in membros:
            raw = read_member_from_open_zip(zf, membro)
            for ev in _events_from_jez_bytes(raw, membro):
                chave = molde(ev.mensagem)
                contagem[chave] += 1
                exemplo.setdefault(chave, ev.mensagem.strip())
    return [(m, contagem[m], exemplo[m]) for m in contagem]


def escrever(linhas: list[tuple[str, int, str]], *, origem: str, destino: Path = EVENTOS_MD) -> Path:
    total = sum(n for _, n, _ in linhas)
    blocos = [
        "# Eventos do log da urna",
        "",
        f"Amostra: {origem}. {len(linhas)} moldes, {total} eventos.",
        "O molde troca cada sequência de dígitos por N. O exemplo é o texto de uma linha real.",
        "Detector só entra no código se a frase exata estiver nesta lista.",
        "",
        "| Contagem | Molde | Exemplo |",
        "|---:|---|---|",
    ]
    for molde_txt, n, ex in sorted(linhas, key=lambda r: (-r[1], r[0])):
        blocos.append(
            f"| {n} | {molde_txt.replace('|', '/')} | {ex.replace('|', '/')} |"
        )
    blocos.append("")
    destino.write_text("\n".join(blocos), encoding="utf-8")
    return destino
