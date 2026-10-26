"""Catálogo de mensagens dos logs (fase 0 — viabilidade)."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.table import Table

from urna_logs.config import REPORTS_DIR, ensure_dirs, zip_path
from urna_logs.parse_log import (
    DIGITAL_MESARIO,
    HAB_BIO,
    HABILITADO,
    PEDIDO_MANUAL,
    SEM_BIO,
    iter_events_from_zip,
)

console = Console()

SIGNAL_PATTERNS = {
    "eleitor_habilitado": HABILITADO,
    "sem_biometria": SEM_BIO,
    "tipo_habilitacao_bio": HAB_BIO,
    "habilitacao_manual": PEDIDO_MANUAL,
    "digital_mesario": DIGITAL_MESARIO,
    "tipo_habilitacao_qualquer": re.compile(
        r"Tipo de habilita[cç][aã]o do eleitor", re.I
    ),
    "solicita_digital": re.compile(r"Solicita digital\. Tentativa", re.I),
    "voto_confirmado": re.compile(r"Voto confirmado|voto computado", re.I),
    "encerramento": re.compile(r"Encerramento|urna encerrada|Fim da vota", re.I),
}


def build_catalog(uf: str, turno: int, *, max_events: int | None = None) -> dict:
    ensure_dirs()
    zpath = zip_path(uf, turno)
    if not zpath.exists():
        raise FileNotFoundError(f"ZIP não encontrado: {zpath}. Rode o download antes.")

    msg_counter: Counter[str] = Counter()
    app_counter: Counter[str] = Counter()
    signal_hits: Counter[str] = Counter()
    after_17_habilitados = 0
    total_habilitados = 0
    sample_by_signal: dict[str, list[str]] = {k: [] for k in SIGNAL_PATTERNS}
    extensions: Counter[str] = Counter()
    total_events = 0

    import zipfile

    with zipfile.ZipFile(zpath) as zf:
        for name in zf.namelist():
            if name.endswith("/"):
                continue
            lower = name.lower()
            # TSE 2026: o...-bu.dat, o...-log.jez, o...-rdv.dat, o...-vota.vsc
            if lower.endswith("-bu.dat") or lower.endswith(".bu"):
                extensions["bu"] += 1
            elif lower.endswith("-log.jez") or lower.endswith(".logjez"):
                extensions["logjez"] += 1
            elif lower.endswith("-rdv.dat") or lower.endswith(".rdv"):
                extensions["rdv"] += 1
            elif lower.endswith("-imgbu.dat") or lower.endswith(".imgbu"):
                extensions["imgbu"] += 1
            elif lower.endswith(".vsc") or lower.endswith(".vscmr"):
                extensions["assinatura"] += 1
            elif lower.endswith(".zip"):
                extensions["zip_aninhado"] += 1
            elif lower.endswith(".pdf"):
                extensions["pdf"] += 1
            else:
                ext = Path(name).suffix.lower() or "(sem_ext)"
                extensions[ext] += 1

    for ev in iter_events_from_zip(zpath):
        total_events += 1
        # normaliza mensagem para catálogo (remove scores numéricos variáveis)
        norm = re.sub(r"\d+", "N", ev.mensagem)
        norm = re.sub(r"\s+", " ", norm).strip()
        msg_counter[f"{ev.aplicativo}|{norm}"] += 1
        app_counter[ev.aplicativo] += 1

        for key, pat in SIGNAL_PATTERNS.items():
            if pat.search(ev.mensagem):
                signal_hits[key] += 1
                if len(sample_by_signal[key]) < 5:
                    sample_by_signal[key].append(
                        f"{ev.data} {ev.hora} {ev.aplicativo} {ev.mensagem}"
                    )

        if HABILITADO.search(ev.mensagem):
            total_habilitados += 1
            if ev.after_17h:
                after_17_habilitados += 1

        if max_events and total_events >= max_events:
            break

    top_msgs = msg_counter.most_common(200)
    result = {
        "uf": uf.upper(),
        "turno": turno,
        "zip": str(zpath),
        "zip_size_bytes": zpath.stat().st_size,
        "total_events_parsed": total_events,
        "total_habilitados": total_habilitados,
        "habilitados_apos_17h": after_17_habilitados,
        "pct_habilitados_apos_17h": (
            round(100 * after_17_habilitados / total_habilitados, 4)
            if total_habilitados
            else None
        ),
        "extensions_in_zip": dict(extensions.most_common()),
        "apps": dict(app_counter.most_common()),
        "signal_hits": dict(signal_hits),
        "signal_samples": sample_by_signal,
        "top_messages": [{"key": k, "count": c} for k, c in top_msgs],
        "viability": _assess_viability(signal_hits, extensions, total_habilitados),
    }
    return result


def _assess_viability(
    signals: Counter[str],
    extensions: Counter[str],
    total_habilitados: int,
) -> dict[str, dict]:
    has_bu = extensions.get("bu", 0) > 0 or any(
        k.endswith(".bu") or k == ".bu" for k in extensions
    )
    has_log = (
        extensions.get("logjez", 0) > 0
        or extensions.get("zip_aninhado", 0) > 0
        or any(k in extensions for k in (".logjez", ".jez", ".log"))
    )

    return {
        "totais_votos": {
            "status": "go" if has_bu or total_habilitados else "no-go",
            "reason": (
                "BU presente no pacote e/ou habilitações no log"
                if has_bu or total_habilitados
                else "Sem BU nem eventos de habilitação"
            ),
            "has_bu": has_bu,
            "habilitados_no_log": total_habilitados,
        },
        "pct_sem_digital": {
            "status": (
                "go"
                if signals.get("tipo_habilitacao_bio")
                or signals.get("habilitacao_manual")
                or signals.get("sem_biometria")
                else "review"
            ),
            "reason": (
                "Habilitações biométricas e/ou manuais identificáveis no log; "
                "em 2026 o fluxo sem digital aparece como 'habilitação manual' "
                "(ano de nascimento + digital do mesário). "
                + (
                    "Mensagem explícita 'sem biometria' também presente."
                    if signals.get("sem_biometria")
                    else "Mensagem explícita 'não possui biometria' rara/ausente neste pacote."
                )
            ),
            "hits": {
                k: signals.get(k, 0)
                for k in (
                    "sem_biometria",
                    "tipo_habilitacao_bio",
                    "tipo_habilitacao_qualquer",
                    "habilitacao_manual",
                    "digital_mesario",
                    "solicita_digital",
                )
            },
        },
        "impacto_apos_17h": {
            "status": "go" if total_habilitados else "no-go",
            "reason": (
                "Timestamps parseáveis com eventos de habilitação"
                if total_habilitados
                else "Sem habilitações para analisar horário"
            ),
            "has_log": has_log,
        },
    }


def save_catalog(result: dict, uf: str, turno: int) -> Path:
    ensure_dirs()
    out_json = REPORTS_DIR / f"catalog_{uf.upper()}_{turno}t.json"
    out_csv = REPORTS_DIR / f"catalog_messages_{uf.upper()}_{turno}t.csv"
    out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    pd.DataFrame(result["top_messages"]).to_csv(out_csv, index=False)
    return out_json


def print_catalog_summary(result: dict) -> None:
    console.print(
        f"\n[bold]Catálogo {result['uf']} {result['turno']}º turno[/bold] — "
        f"{result['total_events_parsed']:,} eventos"
    )
    table = Table(title="Sinais de viabilidade")
    table.add_column("Análise")
    table.add_column("Status")
    table.add_column("Detalhe")
    for name, info in result["viability"].items():
        status = info["status"]
        color = {"go": "green", "no-go": "red", "review": "yellow"}.get(status, "white")
        table.add_row(name, f"[{color}]{status}[/{color}]", info["reason"])
    console.print(table)

    sig = Table(title="Hits de sinais")
    sig.add_column("Sinal")
    sig.add_column("Count", justify="right")
    for k, v in result["signal_hits"].items():
        sig.add_row(k, f"{v:,}")
    console.print(sig)

    ext = Table(title="Extensões no ZIP")
    ext.add_column("Ext")
    ext.add_column("Count", justify="right")
    for k, v in result["extensions_in_zip"].items():
        ext.add_row(k, f"{v:,}")
    console.print(ext)
