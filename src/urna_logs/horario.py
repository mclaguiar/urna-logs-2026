"""Distribuição horária das habilitações (curva do dia + pós-17h)."""

from __future__ import annotations

import re
from datetime import time
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn, TimeElapsedColumn
from rich.table import Table

from urna_logs.audit import join_key
from urna_logs.config import FUSO_UTC_OFFSET, REPORTS_DIR, ensure_dirs, zip_path
from urna_logs.parse_log import classify_habilitacoes, iter_events_from_zip

console = Console()

# o03220ac0100700090001  →  UF + mun + zona + seção
_STEM_RE = re.compile(
    r"(?P<stem>o\d{5}(?P<uf>[a-z]{2})(?P<mun>\d{5})(?P<zona>\d{4})(?P<secao>\d{4}))",
    re.I,
)


def fuso_offset(uf: str) -> int:
    """Offset UTC usado só como metadado; o relógio do log é tratado como hora local."""
    return int(FUSO_UTC_OFFSET.get(uf.upper(), -3))


def stem_from_source(source: str) -> str | None:
    m = _STEM_RE.search(source.replace("\\", "/").split("/")[-1])
    return m.group("stem").lower() if m else None


def join_key_from_stem(stem: str) -> str | None:
    m = _STEM_RE.fullmatch(stem.lower()) if stem else None
    if not m:
        m = _STEM_RE.search(stem or "")
    if not m:
        return None
    return join_key(
        m.group("uf"),
        int(m.group("mun")),
        int(m.group("zona")),
        int(m.group("secao")),
    )


def faixa_hora(hora: int | None) -> str:
    if hora is None:
        return "sem_hora"
    if hora < 8:
        return "antes_08h"
    if hora < 12:
        return "08_12h"
    if hora < 17:
        return "12_17h"
    if hora < 18:
        return "17_18h"
    if hora < 19:
        return "18_19h"
    return "19h_mais"


def compute_horario(uf: str, turno: int) -> pd.DataFrame:
    """Uma linha por habilitação, com hora local (relógio da urna) e join_key."""
    ensure_dirs()
    uf = uf.upper()
    zpath = zip_path(uf, turno)
    if not zpath.exists():
        raise FileNotFoundError(f"ZIP não encontrado: {zpath}")

    rows: list[dict] = []
    for hab in classify_habilitacoes(iter_events_from_zip(zpath)):
        stem = stem_from_source(hab.source)
        jk = join_key_from_stem(stem) if stem else None
        hora = hab.dt.hour if hab.dt is not None else None
        after = bool(hab.dt and hab.dt.time() >= time(17, 0, 0))
        rows.append(
            {
                "uf": uf,
                "turno": turno,
                "fuso_utc_offset": fuso_offset(uf),
                "id_ue": hab.id_ue,
                "stem": stem or "",
                "join_key": jk or "",
                "source": hab.source,
                "dt": hab.dt.isoformat(sep=" ") if hab.dt else None,
                "hora": hora,
                "faixa": faixa_hora(hora),
                "after_17h": after,
                "tipo": hab.tipo,
            }
        )
    if not rows:
        return pd.DataFrame(
            columns=[
                "uf",
                "turno",
                "fuso_utc_offset",
                "id_ue",
                "stem",
                "join_key",
                "source",
                "dt",
                "hora",
                "faixa",
                "after_17h",
                "tipo",
            ]
        )
    return pd.DataFrame(rows)


def aggregate_por_hora(df: pd.DataFrame) -> pd.DataFrame:
    """Contagem e % por hora (0–23) — base da curva."""
    if df.empty or df["hora"].isna().all():
        return pd.DataFrame(
            columns=["uf", "turno", "hora", "habilitacoes", "pct", "after_17h"]
        )
    uf = str(df["uf"].iloc[0]).upper()
    turno = int(df["turno"].iloc[0])
    total = int(df["hora"].notna().sum())
    counts = (
        df.dropna(subset=["hora"])
        .groupby("hora", as_index=False)
        .size()
        .rename(columns={"size": "habilitacoes"})
    )
    # completa horas faltantes
    full = pd.DataFrame({"hora": list(range(24))})
    out = full.merge(counts, on="hora", how="left")
    out["habilitacoes"] = out["habilitacoes"].fillna(0).astype(int)
    out["pct"] = out["habilitacoes"].apply(
        lambda n: round(100 * n / total, 4) if total else 0.0
    )
    out["after_17h"] = out["hora"] >= 17
    out["uf"] = uf
    out["turno"] = turno
    return out[["uf", "turno", "hora", "habilitacoes", "pct", "after_17h"]]


def summarize_horario(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "total_habilitacoes": 0,
            "com_hora": 0,
            "urnas": 0,
            "secoes": 0,
            "pct_apos_17h": None,
            "apos_17h_count": 0,
            "pct_17_18": None,
            "pct_18_19": None,
            "pct_19_mais": None,
            "hora_pico": None,
            "habilitacoes_pico": 0,
        }
    com_hora = df[df["hora"].notna()]
    total = len(com_hora)
    apos = int(com_hora["after_17h"].sum()) if total else 0
    f17 = int((com_hora["faixa"] == "17_18h").sum()) if total else 0
    f18 = int((com_hora["faixa"] == "18_19h").sum()) if total else 0
    f19 = int((com_hora["faixa"] == "19h_mais").sum()) if total else 0
    por_hora = com_hora.groupby("hora").size()
    hora_pico = int(por_hora.idxmax()) if not por_hora.empty else None
    return {
        "total_habilitacoes": int(len(df)),
        "com_hora": total,
        "urnas": int(df["id_ue"].nunique()),
        "secoes": int(df.loc[df["join_key"] != "", "join_key"].nunique()),
        "pct_apos_17h": round(100 * apos / total, 4) if total else None,
        "apos_17h_count": apos,
        "pct_17_18": round(100 * f17 / total, 4) if total else None,
        "pct_18_19": round(100 * f18 / total, 4) if total else None,
        "pct_19_mais": round(100 * f19 / total, 4) if total else None,
        "hora_pico": hora_pico,
        "habilitacoes_pico": int(por_hora.max()) if not por_hora.empty else 0,
        "fuso_utc_offset": int(df["fuso_utc_offset"].iloc[0]),
    }


def write_horario_reports(
    df: pd.DataFrame, por_hora: pd.DataFrame, summary: dict, uf: str, turno: int
) -> tuple[Path, Path, Path, Path]:
    ensure_dirs()
    uf = uf.upper()
    detail = REPORTS_DIR / f"horario_{uf}_{turno}t.parquet"
    hora_csv = REPORTS_DIR / f"horario_por_hora_{uf}_{turno}t.csv"
    summary_csv = REPORTS_DIR / f"horario_summary_{uf}_{turno}t.csv"
    md = REPORTS_DIR / f"horario_{uf}_{turno}t.md"

    df.to_parquet(detail, index=False)
    por_hora.to_csv(hora_csv, index=False)
    pd.DataFrame([{**summary, "uf": uf, "turno": turno}]).to_csv(summary_csv, index=False)

    lines = [
        f"# Curva horária — {uf} {turno}º turno",
        "",
        "Fonte: timestamps de **habilitação** no log da urna (`Eleitor foi habilitado`).",
        "Não é horário do voto em cada cargo; o RDV não traz timestamp por voto.",
        "",
        f"Relógio do log tratado como **hora local** da UF "
        f"(metadado fuso UTC{summary.get('fuso_utc_offset', -3):+d}).",
        "",
        "## Resumo",
        "",
        f"- Habilitações: **{summary['total_habilitacoes']:,}** "
        f"(com hora: **{summary['com_hora']:,}**)",
        f"- Seções (`join_key`): **{summary['secoes']:,}** · urnas: **{summary['urnas']:,}**",
        f"- Pico: **{summary['hora_pico']}h** ({summary['habilitacoes_pico']:,} habilitações)",
        f"- % ≥17h: **{summary['pct_apos_17h']}** · "
        f"17–18h: **{summary['pct_17_18']}** · "
        f"18–19h: **{summary['pct_18_19']}** · "
        f"19h+: **{summary['pct_19_mais']}**",
        "",
        "## Contagem por hora",
        "",
        "| Hora | Habilitações | % |",
        "|---:|---:|---:|",
    ]
    for _, row in por_hora.iterrows():
        if int(row["habilitacoes"]) == 0:
            continue
        lines.append(
            f"| {int(row['hora']):02d}h | {int(row['habilitacoes']):,} | {row['pct']} |"
        )
    lines += [
        "",
        "## Nota sobre forma da curva",
        "",
        "Não se espera distribuição normal: o padrão típico é multimodal "
        "(manhã / tarde) com cauda após 17h.",
        "",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")
    return detail, hora_csv, summary_csv, md


def print_horario_summary(summary: dict, por_hora: pd.DataFrame, uf: str, turno: int) -> None:
    console.print(f"\n[bold]Horário — {uf.upper()} {turno}º turno[/bold]")
    table = Table()
    table.add_column("Métrica")
    table.add_column("Valor", justify="right")
    table.add_row("Habilitações", f"{summary['total_habilitacoes']:,}")
    table.add_row("Seções", f"{summary['secoes']:,}")
    table.add_row(
        "% ≥17h",
        f"{summary['pct_apos_17h']}%" if summary["pct_apos_17h"] is not None else "—",
    )
    table.add_row(
        "Pico",
        f"{summary['hora_pico']}h ({summary['habilitacoes_pico']:,})"
        if summary["hora_pico"] is not None
        else "—",
    )
    console.print(table)

    top = Table(title="Horas com mais fluxo")
    top.add_column("Hora")
    top.add_column("N", justify="right")
    top.add_column("%", justify="right")
    ranked = por_hora.sort_values("habilitacoes", ascending=False).head(8)
    for _, row in ranked.iterrows():
        if int(row["habilitacoes"]) == 0:
            continue
        top.add_row(f"{int(row['hora']):02d}h", f"{int(row['habilitacoes']):,}", f"{row['pct']}")
    console.print(top)


def consolidate_horario(ufs: list[str], turno: int) -> tuple[Path, Path] | None:
    horas: list[pd.DataFrame] = []
    sums: list[pd.DataFrame] = []
    for uf in ufs:
        uf = uf.upper()
        hp = REPORTS_DIR / f"horario_por_hora_{uf}_{turno}t.csv"
        sp = REPORTS_DIR / f"horario_summary_{uf}_{turno}t.csv"
        if hp.exists():
            horas.append(pd.read_csv(hp))
        if sp.exists():
            sums.append(pd.read_csv(sp))
    if not horas:
        return None
    h_out = REPORTS_DIR / f"horario_por_hora_MULTI_{turno}t.csv"
    s_out = REPORTS_DIR / f"horario_summary_MULTI_{turno}t.csv"
    pd.concat(horas, ignore_index=True).to_csv(h_out, index=False)
    if sums:
        pd.concat(sums, ignore_index=True).to_csv(s_out, index=False)
    return h_out, s_out


def run_horario(ufs: list[str], turno: int) -> list[Path]:
    outputs: list[Path] = []
    done: list[str] = []
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("UFs", total=len(ufs))
        for uf in ufs:
            uf = uf.upper()
            progress.update(task, description=f"Horário {uf}")
            console.print(f"\n[bold]Horário {uf} {turno}º turno[/bold]")
            try:
                df = compute_horario(uf, turno)
            except FileNotFoundError as exc:
                console.print(f"[red]Pulando {uf}:[/red] {exc}")
                progress.advance(task)
                continue
            por_hora = aggregate_por_hora(df)
            summary = summarize_horario(df)
            print_horario_summary(summary, por_hora, uf, turno)
            paths = write_horario_reports(df, por_hora, summary, uf, turno)
            outputs.extend(paths)
            console.print(f"[green]Relatório:[/green] {paths[3]}")
            done.append(uf)
            progress.advance(task)

    if len(done) > 1:
        cons = consolidate_horario(done, turno)
        if cons:
            console.print(f"\n[green]Curva multi-UF:[/green] {cons[0]}")
            outputs.extend(cons)
    return outputs
