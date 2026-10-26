"""Relatório go/no-go de viabilidade (fase 0)."""

from __future__ import annotations

import re
import zipfile
from collections import Counter
from pathlib import Path

import pandas as pd
from rich.console import Console

from urna_logs.catalog import (
    SIGNAL_PATTERNS,
    _assess_viability,
    print_catalog_summary,
    save_catalog,
)
from urna_logs.config import REPORTS_DIR, ensure_dirs, zip_path
from urna_logs.metrics import print_summary, save_metrics, summarize
from urna_logs.parse_log import (
    HABILITADO,
    classify_habilitacoes,
    iter_events_from_zip,
)

console = Console()


def _extensions(zpath: Path) -> Counter[str]:
    extensions: Counter[str] = Counter()
    with zipfile.ZipFile(zpath) as zf:
        for name in zf.namelist():
            if name.endswith("/"):
                continue
            lower = name.lower()
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
    return extensions


def write_viability_report(uf: str, turno: int, catalog: dict, metrics_summary: dict) -> Path:
    ensure_dirs()
    path = REPORTS_DIR / f"viability_{uf.upper()}_{turno}t.md"
    v = catalog["viability"]
    lines = [
        f"# Viabilidade — {uf.upper()} {turno}º turno (Eleições 2026)",
        "",
        f"ZIP: `{catalog['zip']}` ({catalog['zip_size_bytes']:,} bytes)",
        f"Eventos parseados: **{catalog['total_events_parsed']:,}**",
        f"Habilitações no log: **{catalog['total_habilitados']:,}**",
        "",
        "## Decisão por análise",
        "",
        "| Análise | Status | Motivo |",
        "|---|---|---|",
    ]
    labels = {
        "totais_votos": "Total de votos (log × BU)",
        "pct_sem_digital": "% votos/habilitações sem digital",
        "impacto_apos_17h": "Impacto após 17h",
    }
    for key, label in labels.items():
        info = v[key]
        lines.append(f"| {label} | **{info['status']}** | {info['reason']} |")

    lines += ["", "## Sinais encontrados no log", ""]
    for k, c in catalog["signal_hits"].items():
        lines.append(f"- `{k}`: {c:,}")

    lines += ["", "## Extensões no pacote ZIP", ""]
    for ext, c in catalog["extensions_in_zip"].items():
        lines.append(f"- `{ext}`: {c:,}")

    lines += [
        "",
        "## Amostra de métricas (pipeline)",
        "",
        f"- Total habilitações classificadas: {metrics_summary.get('total_habilitacoes', 0):,}",
        f"- % sem digital **log** (sem_biometria + manual_falha; ≠ BU): "
        f"{metrics_summary.get('pct_sem_digital_log', metrics_summary.get('pct_sem_digital'))}",
        f"- % após 17h (BRT / ZZ local): {metrics_summary.get('pct_apos_17h')}",
        f"- Por tipo: `{metrics_summary.get('por_tipo', {})}`",
        "",
        "## Amostras de mensagens",
        "",
    ]
    for signal, samples in catalog.get("signal_samples", {}).items():
        if not samples:
            continue
        lines.append(f"### {signal}")
        for s in samples:
            lines.append(f"- `{s}`")
        lines.append("")

    lines += [
        "## Notas do spike AC 2026",
        "",
        "- Pacote por UF traz `-bu.dat`, `-log.jez`, `-rdv.dat`, `-vota.vsc` (sem imgbu neste conjunto).",
        "- Logs internos: `logd.dat` (latin-1) dentro de cada `-log.jez`.",
        "- Tipo biométrico: `Tipo de habilitação do eleitor [biométrica]`.",
        "- Liberação sem reconhecimento digital: fluxo `Solicitação de dado pessoal... habilitação manual` + digital do mesário.",
        "- Mensagem clássica `O eleitor não possui biometria` pode estar ausente; use o fluxo manual como proxy de “sem digital”.",
        "",
        "## Próximos passos",
        "",
        "- Escalar download para demais UFs e 2º turno.",
        "- Cruzar totais do BU (ASN.1/`-bu.dat`) com habilitações por seção.",
        "- Pós-17h: horário de Brasília (ZZ = local do posto); ver `urna_logs.fuso`.",
        "- Sem digital no **BU** = biografia + sem_biometria; no **log** = sem_biometria + manual_falha.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def run_viability(uf: str, turno: int) -> Path:
    """Uma passagem no ZIP: catálogo + métricas + relatório."""
    ensure_dirs()
    uf = uf.upper()
    zpath = zip_path(uf, turno)
    if not zpath.exists():
        raise FileNotFoundError(f"ZIP não encontrado: {zpath}. Rode o download antes.")

    console.print(f"[cyan]Processando[/cyan] {zpath.name} (passagem única)...")

    extensions = _extensions(zpath)
    msg_counter: Counter[str] = Counter()
    app_counter: Counter[str] = Counter()
    signal_hits: Counter[str] = Counter()
    sample_by_signal: dict[str, list[str]] = {k: [] for k in SIGNAL_PATTERNS}
    after_17_habilitados = 0
    total_habilitados = 0
    total_events = 0
    rows: list[dict] = []

    # classify_habilitacoes consome o iterator — alimentamos com os mesmos eventos
    def event_stream():
        nonlocal total_events, total_habilitados, after_17_habilitados
        for ev in iter_events_from_zip(zpath):
            total_events += 1
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
                if ev.apos_17h_oficial(uf):
                    after_17_habilitados += 1
            yield ev

    for hab in classify_habilitacoes(event_stream(), uf=uf):
        rows.append(
            {
                "uf": uf,
                "turno": turno,
                "id_ue": hab.id_ue,
                "source": hab.source,
                "dt": hab.dt.isoformat(sep=" ") if hab.dt else None,
                "after_17h": hab.after_17h,
                "tipo": hab.tipo,
                "mensagem_tipo": hab.mensagem_tipo,
            }
        )

    catalog = {
        "uf": uf,
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
        "top_messages": [
            {"key": k, "count": c} for k, c in msg_counter.most_common(200)
        ],
        "viability": _assess_viability(signal_hits, extensions, total_habilitados),
    }
    save_catalog(catalog, uf, turno)
    print_catalog_summary(catalog)

    df = pd.DataFrame(rows) if rows else pd.DataFrame(
        columns=["uf", "turno", "id_ue", "source", "dt", "after_17h", "tipo", "mensagem_tipo"]
    )
    summary = summarize(df)
    save_metrics(df, summary, uf, turno)
    print_summary(summary, uf, turno)

    report = write_viability_report(uf, turno, catalog, summary)
    return report
