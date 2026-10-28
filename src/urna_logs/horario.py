"""Distribuição horária das habilitações (curva do dia + pós-17h)."""

from __future__ import annotations

import os
import re
import zipfile
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import TypedDict

import pandas as pd
from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn, TimeElapsedColumn
from rich.table import Table

from urna_logs.audit import join_key
from urna_logs.config import REPORTS_DIR, ensure_dirs, zip_path
from urna_logs.fuso import (
    apos_encerramento_oficial,
    delta_local_para_brt,
    fuso_offset,
    hora_brasilia,
)

# Reexport — testes e callers históricos importavam daqui
__all__ = [
    "apos_encerramento_oficial",
    "delta_local_para_brt",
    "fuso_offset",
    "hora_brasilia",
    "faixa_hora",
    "run_horario",
    "compute_horario_curva",
    "compute_horario_secao",
    "refresh_horario_brt",
]
from urna_logs.parse_log import (
    classify_habilitacoes,
    count_habilitado_hours_from_jez_bytes,
    iter_events_from_zip,
)
from urna_logs.zip_logs import list_log_members, read_member_from_open_zip

console = Console()

_STEM_RE = re.compile(
    r"(?P<stem>o\d{5}(?P<uf>[a-z]{2})(?P<mun>\d{5})(?P<zona>\d{4})(?P<secao>\d{4}))",
    re.I,
)


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


def faixa_hora(hora: int | None, *, uf: str | None = None) -> str:
    """Faixas pelo horário de referência do encerramento (BRT, ou local se ZZ)."""
    if hora is None:
        return "sem_hora"
    h = hora_brasilia(int(hora), uf) if uf else int(hora)
    if h < 8:
        return "antes_08h"
    if h < 12:
        return "08_12h"
    if h < 17:
        return "12_17h"
    if h < 18:
        return "17_18h"
    if h < 19:
        return "18_19h"
    return "19h_mais"


class HorarioSummary(TypedDict, total=False):
    total_habilitacoes: int
    com_hora: int
    urnas: int
    secoes: int
    pct_apos_17h: float | None
    apos_17h_count: int
    pct_17_18: float | None
    pct_18_19: float | None
    pct_19_mais: float | None
    hora_pico: int | None
    habilitacoes_pico: int
    fuso_utc_offset: int
    delta_para_brt: int | None
    ref_encerramento: str
    modo: str


def _summary_from_counts_local(
    counts_local: list[int], uf: str, *, urnas: int, secoes: int, modo: str
) -> HorarioSummary:
    """Agrega pós-encerramento usando ≥17h Brasília (ZZ = local)."""
    total = sum(counts_local)
    counts_ref = [0] * 24
    for h_local, c in enumerate(counts_local):
        counts_ref[hora_brasilia(h_local, uf)] += c
    apos = sum(counts_ref[17:])
    f17, f18, f19 = counts_ref[17], counts_ref[18], sum(counts_ref[19:])
    hora_pico_local = (
        max(range(24), key=lambda h: counts_local[h]) if total else None
    )
    ref = "local" if uf.upper() == "ZZ" else "brasilia"
    return {
        "total_habilitacoes": total,
        "com_hora": total,
        "urnas": urnas,
        "secoes": secoes,
        "pct_apos_17h": round(100 * apos / total, 4) if total else None,
        "apos_17h_count": apos,
        "pct_17_18": round(100 * f17 / total, 4) if total else None,
        "pct_18_19": round(100 * f18 / total, 4) if total else None,
        "pct_19_mais": round(100 * f19 / total, 4) if total else None,
        "hora_pico": hora_pico_local,
        "habilitacoes_pico": counts_local[hora_pico_local]
        if hora_pico_local is not None
        else 0,
        "fuso_utc_offset": fuso_offset(uf),
        "delta_para_brt": delta_local_para_brt(uf),
        "ref_encerramento": ref,
        "modo": modo,
    }


def annotate_por_hora(por_hora: pd.DataFrame, uf: str) -> pd.DataFrame:
    """Marca after_17h pelo critério oficial (BRT, exceto ZZ)."""
    out = por_hora.copy()
    out["hora_brasilia"] = out["hora"].map(lambda h: hora_brasilia(int(h), uf))
    out["after_17h"] = out["hora"].map(
        lambda h: apos_encerramento_oficial(int(h), uf)
    )
    return out


def _count_chunk(payload: tuple[str, list[str]]) -> dict:
    """
    Processo filho: abre o ZIP **uma vez** e processa um lote de membros.
    Evita 1 ZipFile.open por log (matava UFs grandes tipo BA ~35k logs).
    """
    zpath_s, members = payload
    counts = [0] * 24
    urnas: set[str] = set()
    stems: set[str] = set()
    with zipfile.ZipFile(zpath_s) as zf:
        for member in members:
            raw = read_member_from_open_zip(zf, member)
            part, ids = count_habilitado_hours_from_jez_bytes(raw)
            for h, c in enumerate(part):
                counts[h] += c
            urnas.update(ids)
            st = stem_from_source(member)
            if st:
                stems.add(st)
    return {
        "counts": counts,
        "total": sum(counts),
        "n_logs": len(members),
        "urnas": list(urnas),
        "stems": list(stems),
    }


def _count_chunk_secao(payload: tuple[str, list[str]]) -> dict:
    """Processo filho: stem → contagem[24] (hora local)."""
    zpath_s, members = payload
    by_stem: dict[str, list[int]] = {}
    with zipfile.ZipFile(zpath_s) as zf:
        for member in members:
            raw = read_member_from_open_zip(zf, member)
            part, _ids = count_habilitado_hours_from_jez_bytes(raw)
            st = stem_from_source(member)
            if not st:
                continue
            bucket = by_stem.get(st)
            if bucket is None:
                bucket = [0] * 24
                by_stem[st] = bucket
            for h, c in enumerate(part):
                bucket[h] += c
    return {
        "by_stem": by_stem,
        "n_logs": len(members),
        "total": sum(sum(v) for v in by_stem.values()),
    }


def _chunked_by_size(items: list[str], size: int) -> list[list[str]]:
    size = max(1, size)
    return [items[i : i + size] for i in range(0, len(items), size)]


def compute_horario_curva(
    uf: str,
    turno: int,
    *,
    workers: int | None = None,
    on_progress: Callable[[int, int, int, int, int], None] | None = None,
) -> tuple[pd.DataFrame, dict]:
    """
    Modo rápido: agrega hora→contagem em lotes paralelos (1 ZipFile/lote).
    Não grava Parquet detalhado (1 linha/habilitação).

    on_progress(done_logs, total_logs, hab, lote_i, n_lotes) — opcional.
    """
    ensure_dirs()
    uf = uf.upper()
    zpath = zip_path(uf, turno)
    if not zpath.exists():
        raise FileNotFoundError(f"ZIP não encontrado: {zpath}")

    zip_mb = zpath.stat().st_size / (1024 * 1024)
    console.print(
        f"[dim]  {uf}: lendo índice do ZIP ({zip_mb:,.0f} MB)…[/dim]"
    )
    members = list_log_members(zpath)
    counts = [0] * 24
    urnas: set[str] = set()
    stems: set[str] = set()
    hab_so_far = 0
    logs_done = 0

    n_workers = workers or min(8, max(1, (os.cpu_count() or 4)))
    # ~500 logs/lote → barra atualiza com frequência sem reabrir o ZIP demais
    lote_size = 500 if len(members) >= 64 else max(len(members), 1)
    chunks = _chunked_by_size(members, lote_size)
    n_lotes = len(chunks)
    use_pool = len(members) >= 64 and n_workers > 1 and n_lotes > 1

    console.print(
        f"[dim]  {uf}: {len(members):,} logs · {n_lotes} lote(s) "
        f"(~{lote_size}/lote) · "
        f"{'pool '+str(n_workers)+' workers' if use_pool else 'série'}[/dim]"
    )

    def _absorb(part: dict, lote_i: int) -> None:
        nonlocal hab_so_far, logs_done
        for h, c in enumerate(part["counts"]):
            counts[h] += c
        urnas.update(part["urnas"])
        stems.update(part["stems"])
        logs_done += int(part["n_logs"])
        hab_so_far += int(part["total"])
        if on_progress:
            on_progress(logs_done, len(members), hab_so_far, lote_i, n_lotes)
        else:
            console.print(
                f"[dim]  {uf}: lote {lote_i}/{n_lotes} · "
                f"{logs_done:,}/{len(members):,} logs · "
                f"{hab_so_far:,} hab[/dim]"
            )

    if use_pool:
        with ProcessPoolExecutor(max_workers=n_workers) as pool:
            futures = {
                pool.submit(_count_chunk, (str(zpath), chunk)): i
                for i, chunk in enumerate(chunks, start=1)
            }
            finished = 0
            for fut in as_completed(futures):
                finished += 1
                _absorb(fut.result(), finished)
    else:
        for i, chunk in enumerate(chunks, start=1):
            _absorb(_count_chunk((str(zpath), chunk)), i)

    total = sum(counts)
    por_hora = annotate_por_hora(
        pd.DataFrame(
            {
                "uf": uf,
                "turno": turno,
                "hora": list(range(24)),
                "habilitacoes": counts,
                "pct": [
                    round(100 * c / total, 4) if total else 0.0 for c in counts
                ],
            }
        ),
        uf,
    )
    summary = _summary_from_counts_local(
        counts, uf, urnas=len(urnas), secoes=len(stems), modo="curva"
    )
    return por_hora, summary


def compute_horario_secao(
    uf: str,
    turno: int,
    *,
    workers: int | None = None,
    on_progress: Callable[[int, int, int, int, int], None] | None = None,
) -> pd.DataFrame:
    """
    Agrega habilitações pós-17h por seção (`join_key`), sem Parquet 1-linha/hab.
    Mesmo scan em lotes do modo curva.
    """
    ensure_dirs()
    uf = uf.upper()
    zpath = zip_path(uf, turno)
    if not zpath.exists():
        raise FileNotFoundError(f"ZIP não encontrado: {zpath}")

    members = list_log_members(zpath)
    by_stem: dict[str, list[int]] = {}
    logs_done = 0
    hab_so_far = 0

    n_workers = workers or min(8, max(1, (os.cpu_count() or 4)))
    lote_size = 500 if len(members) >= 64 else max(len(members), 1)
    chunks = _chunked_by_size(members, lote_size)
    n_lotes = len(chunks)
    use_pool = len(members) >= 64 and n_workers > 1 and n_lotes > 1

    console.print(
        f"[dim]  {uf} secao: {len(members):,} logs · {n_lotes} lote(s) · "
        f"{'pool '+str(n_workers) if use_pool else 'série'}[/dim]"
    )

    def _absorb(part: dict, lote_i: int) -> None:
        nonlocal logs_done, hab_so_far
        for st, counts in part["by_stem"].items():
            bucket = by_stem.get(st)
            if bucket is None:
                bucket = [0] * 24
                by_stem[st] = bucket
            for h, c in enumerate(counts):
                bucket[h] += c
        logs_done += int(part["n_logs"])
        hab_so_far += int(part["total"])
        if on_progress:
            on_progress(logs_done, len(members), hab_so_far, lote_i, n_lotes)
        else:
            console.print(
                f"[dim]  {uf} secao: lote {lote_i}/{n_lotes} · "
                f"{logs_done:,}/{len(members):,} logs · {hab_so_far:,} hab[/dim]"
            )

    if use_pool:
        with ProcessPoolExecutor(max_workers=n_workers) as pool:
            futures = {
                pool.submit(_count_chunk_secao, (str(zpath), chunk)): i
                for i, chunk in enumerate(chunks, start=1)
            }
            finished = 0
            for fut in as_completed(futures):
                finished += 1
                _absorb(fut.result(), finished)
    else:
        for i, chunk in enumerate(chunks, start=1):
            _absorb(_count_chunk_secao((str(zpath), chunk)), i)

    rows: list[dict] = []
    for stem, counts in by_stem.items():
        jk = join_key_from_stem(stem)
        if not jk:
            continue
        total = sum(counts)
        apos = sum(
            c for h, c in enumerate(counts) if apos_encerramento_oficial(h, uf)
        )
        rows.append(
            {
                "uf": uf,
                "turno": turno,
                "stem": stem,
                "join_key": jk,
                "hab_total": total,
                "hab_apos_17h": apos,
                "pct_apos_17h": round(100 * apos / total, 4) if total else None,
            }
        )
    return pd.DataFrame(rows) if rows else pd.DataFrame(
        columns=[
            "uf",
            "turno",
            "stem",
            "join_key",
            "hab_total",
            "hab_apos_17h",
            "pct_apos_17h",
        ]
    )


def write_horario_secao(df: pd.DataFrame, uf: str, turno: int) -> Path:
    ensure_dirs()
    path = REPORTS_DIR / f"horario_secao_{uf.upper()}_{turno}t.parquet"
    df.to_parquet(path, index=False)
    return path


def compute_horario(uf: str, turno: int) -> pd.DataFrame:
    """Modo detalhe: 1 linha por habilitação (mais lento; para cruzamentos finos)."""
    ensure_dirs()
    uf = uf.upper()
    zpath = zip_path(uf, turno)
    if not zpath.exists():
        raise FileNotFoundError(f"ZIP não encontrado: {zpath}")

    rows: list[dict] = []
    for hab in classify_habilitacoes(iter_events_from_zip(zpath), uf=uf):
        stem = stem_from_source(hab.source)
        jk = join_key_from_stem(stem) if stem else None
        hora = hab.dt.hour if hab.dt is not None else None
        rows.append(
            {
                "uf": uf,
                "turno": turno,
                "fuso_utc_offset": fuso_offset(uf),
                "delta_para_brt": delta_local_para_brt(uf),
                "id_ue": hab.id_ue,
                "stem": stem or "",
                "join_key": jk or "",
                "source": hab.source,
                "dt": hab.dt.isoformat(sep=" ") if hab.dt else None,
                "hora": hora,
                "hora_brasilia": hora_brasilia(hora, uf) if hora is not None else None,
                "faixa": faixa_hora(hora, uf=uf),
                "after_17h": hab.after_17h,
                "tipo": hab.tipo,
            }
        )
    if not rows:
        return pd.DataFrame(
            columns=[
                "uf",
                "turno",
                "fuso_utc_offset",
                "delta_para_brt",
                "id_ue",
                "stem",
                "join_key",
                "source",
                "dt",
                "hora",
                "hora_brasilia",
                "faixa",
                "after_17h",
                "tipo",
            ]
        )
    return pd.DataFrame(rows)


def aggregate_por_hora(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or df["hora"].isna().all():
        return pd.DataFrame(
            columns=[
                "uf",
                "turno",
                "hora",
                "habilitacoes",
                "pct",
                "hora_brasilia",
                "after_17h",
            ]
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
    full = pd.DataFrame({"hora": list(range(24))})
    out = full.merge(counts, on="hora", how="left")
    out["habilitacoes"] = out["habilitacoes"].fillna(0).astype(int)
    out["pct"] = out["habilitacoes"].apply(
        lambda n: round(100 * n / total, 4) if total else 0.0
    )
    out["uf"] = uf
    out["turno"] = turno
    return annotate_por_hora(
        out[["uf", "turno", "hora", "habilitacoes", "pct"]], uf
    )


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
            "modo": "detalhe",
        }
    uf = str(df["uf"].iloc[0]).upper()
    com_hora = df[df["hora"].notna()]
    counts = [0] * 24
    for h, n in com_hora.groupby("hora").size().items():
        counts[int(h)] = int(n)
    base = _summary_from_counts_local(
        counts,
        uf,
        urnas=int(df["id_ue"].nunique()),
        secoes=int(df.loc[df["join_key"] != "", "join_key"].nunique()),
        modo="detalhe",
    )
    base["total_habilitacoes"] = int(len(df))
    base["com_hora"] = int(len(com_hora))
    return base


def write_horario_reports(
    por_hora: pd.DataFrame,
    summary: dict,
    uf: str,
    turno: int,
    *,
    detail: pd.DataFrame | None = None,
) -> tuple[Path, ...]:
    ensure_dirs()
    uf = uf.upper()
    hora_csv = REPORTS_DIR / f"curva_horaria_{uf}_{turno}t.csv"
    summary_csv = REPORTS_DIR / f"horario_summary_{uf}_{turno}t.csv"
    md = REPORTS_DIR / f"horario_{uf}_{turno}t.md"
    outputs: list[Path] = []

    if detail is not None:
        detail_path = REPORTS_DIR / f"horario_{uf}_{turno}t.parquet"
        detail.to_parquet(detail_path, index=False)
        outputs.append(detail_path)

    por_hora.to_csv(hora_csv, index=False)
    pd.DataFrame([{**summary, "uf": uf, "turno": turno}]).to_csv(summary_csv, index=False)

    modo = summary.get("modo", "curva")
    ref = summary.get("ref_encerramento", "local" if uf == "ZZ" else "brasilia")
    if ref == "local":
        criterio = "≥17h no **horário local** do posto (exterior)"
    else:
        delta = summary.get("delta_para_brt")
        extra = (
            f" (local +{delta}h → BRT)"
            if isinstance(delta, int) and delta
            else ""
        )
        criterio = f"≥17h no **horário de Brasília**{extra}"
    lines = [
        f"# Curva horária — {uf} {turno}º turno",
        "",
        f"Modo: **{modo}**"
        + (" (agregado; sem Parquet detalhado)" if modo == "curva" else " (1 linha/habilitação)"),
        "",
        "Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).",
        "Não é horário do voto em cada cargo.",
        "",
        f"Relógio do log = **hora local** da urna "
        f"(metadado fuso UTC{summary.get('fuso_utc_offset', -3):+d}).",
        f"Critério pós-encerramento: {criterio}.",
        "",
        "## Resumo",
        "",
        f"- Habilitações: **{summary['total_habilitacoes']:,}** "
        f"(com hora: **{summary['com_hora']:,}**)",
        f"- Seções: **{summary['secoes']:,}** · urnas: **{summary['urnas']:,}**",
        f"- Pico (hora local): **{summary['hora_pico']}h** "
        f"({summary['habilitacoes_pico']:,})",
        f"- % ≥17h (ref. {ref}): **{summary['pct_apos_17h']}** · "
        f"17–18h: **{summary['pct_17_18']}** · "
        f"18–19h: **{summary['pct_18_19']}** · "
        f"19h+: **{summary['pct_19_mais']}**",
        "",
        "## Distribuição horária (relógio local)",
        "",
        "| Hora local | Habilitações | % | ≥17h BRT* |",
        "|---:|---:|---:|:---:|",
    ]
    for _, row in por_hora.iterrows():
        if int(row["habilitacoes"]) == 0:
            continue
        flag = "sim" if bool(row.get("after_17h")) else ""
        lines.append(
            f"| {int(row['hora']):02d}h | {int(row['habilitacoes']):,} | "
            f"{row['pct']} | {flag} |"
        )
    lines += [
        "",
        f"\\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.",
        "",
        "## Nota",
        "",
        "Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.",
        "",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")
    outputs.extend([hora_csv, summary_csv, md])
    return tuple(outputs)


def print_horario_summary(summary: dict, por_hora: pd.DataFrame, uf: str, turno: int) -> None:
    console.print(
        f"\n[bold]Horário — {uf.upper()} {turno}º turno[/bold] "
        f"[dim]({summary.get('modo', '?')})[/dim]"
    )
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


def refresh_horario_brt(uf: str, turno: int) -> list[Path] | None:
    """
    Reescreve summary/% ≥17h e after_17h a partir da curva horária local
    já existente (sem reabrir o ZIP).
    """
    uf = uf.upper()
    hora_path = REPORTS_DIR / f"curva_horaria_{uf}_{turno}t.csv"
    if not hora_path.exists():
        legacy = REPORTS_DIR / f"horario_por_hora_{uf}_{turno}t.csv"
        if legacy.exists():
            hora_path = legacy
    summary_path = REPORTS_DIR / f"horario_summary_{uf}_{turno}t.csv"
    if not hora_path.exists() or not summary_path.exists():
        return None

    por_hora = pd.read_csv(hora_path)
    if "hora" not in por_hora.columns or "habilitacoes" not in por_hora.columns:
        return None

    counts = [0] * 24
    for _, row in por_hora.iterrows():
        h = int(row["hora"])
        if 0 <= h < 24:
            counts[h] = int(row["habilitacoes"])

    old = pd.read_csv(summary_path).iloc[0].to_dict()
    summary = _summary_from_counts_local(
        counts,
        uf,
        urnas=int(old.get("urnas") or 0),
        secoes=int(old.get("secoes") or 0),
        modo=str(old.get("modo") or "curva"),
    )
    # preserva totais se o summary antigo tinha com_hora distinto
    if "total_habilitacoes" in old and pd.notna(old["total_habilitacoes"]):
        summary["total_habilitacoes"] = int(old["total_habilitacoes"])
    if "com_hora" in old and pd.notna(old["com_hora"]):
        summary["com_hora"] = int(old["com_hora"])

    base = por_hora.copy()
    if "uf" not in base.columns:
        base["uf"] = uf
    if "turno" not in base.columns:
        base["turno"] = turno
    if "pct" not in base.columns:
        tot = int(base["habilitacoes"].sum())
        base["pct"] = base["habilitacoes"].apply(
            lambda n: round(100 * int(n) / tot, 4) if tot else 0.0
        )
    annotated = annotate_por_hora(
        base[["uf", "turno", "hora", "habilitacoes", "pct"]], uf
    )
    return list(write_horario_reports(annotated, summary, uf, turno))


def consolidate_horario(ufs: list[str], turno: int) -> tuple[Path, Path] | None:
    horas: list[pd.DataFrame] = []
    sums: list[pd.DataFrame] = []
    for uf in ufs:
        uf = uf.upper()
        hp = REPORTS_DIR / f"curva_horaria_{uf}_{turno}t.csv"
        if not hp.exists():
            hp = REPORTS_DIR / f"horario_por_hora_{uf}_{turno}t.csv"
        sp = REPORTS_DIR / f"horario_summary_{uf}_{turno}t.csv"
        if hp.exists():
            horas.append(pd.read_csv(hp))
        if sp.exists():
            sums.append(pd.read_csv(sp))
    if not horas:
        return None
    h_out = REPORTS_DIR / f"curva_horaria_MULTI_{turno}t.csv"
    s_out = REPORTS_DIR / f"horario_summary_MULTI_{turno}t.csv"
    pd.concat(horas, ignore_index=True).to_csv(h_out, index=False)
    if sums:
        pd.concat(sums, ignore_index=True).to_csv(s_out, index=False)
    return h_out, s_out


def run_horario_secao(
    ufs: list[str],
    turno: int,
    *,
    force: bool = False,
    workers: int | None = None,
) -> list[Path]:
    """Gera `horario_secao_{UF}_{turno}t.parquet` (pós-17h por join_key)."""
    outputs: list[Path] = []
    for i, uf in enumerate(ufs, start=1):
        uf = uf.upper()
        out = REPORTS_DIR / f"horario_secao_{uf}_{turno}t.parquet"
        if out.exists() and not force:
            console.print(f"[dim]Já existe horário seção {uf} (use --force)[/dim]")
            outputs.append(out)
            continue
        console.print(
            f"\n[bold][{i}/{len(ufs)}] Horário por seção {uf} {turno}º[/bold]"
        )
        try:
            df = compute_horario_secao(uf, turno, workers=workers)
        except FileNotFoundError as exc:
            console.print(f"[red]Pulando {uf}:[/red] {exc}")
            continue
        path = write_horario_secao(df, uf, turno)
        console.print(
            f"[green]Horário seção:[/green] {path} ({len(df):,} seções)"
        )
        outputs.append(path)
    return outputs


def run_horario(
    ufs: list[str],
    turno: int,
    *,
    detalhe: bool = False,
    force: bool = False,
    workers: int | None = None,
    por_secao: bool = False,
) -> list[Path]:
    outputs: list[Path] = []
    done: list[str] = []
    if por_secao:
        outputs.extend(run_horario_secao(ufs, turno, force=force, workers=workers))
        # ainda atualiza curva UF se pedido no mesmo comando
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
            summary_path = REPORTS_DIR / f"horario_summary_{uf}_{turno}t.csv"
            hora_path = REPORTS_DIR / f"curva_horaria_{uf}_{turno}t.csv"
            legacy_hora = REPORTS_DIR / f"horario_por_hora_{uf}_{turno}t.csv"
            if (
                not force
                and summary_path.exists()
                and (hora_path.exists() or legacy_hora.exists())
            ):
                # Reanota pós-17h em BRT sem reparsear o ZIP (contagens locais intactas)
                refreshed = refresh_horario_brt(uf, turno)
                if refreshed:
                    console.print(
                        f"[dim]Já existe — reanotado BRT {uf} (use --force p/ reparse)[/dim]"
                    )
                    outputs.extend(refreshed)
                else:
                    console.print(f"[dim]Já existe — pulando {uf} (use --force)[/dim]")
                done.append(uf)
                progress.advance(task)
                continue

            console.print(
                f"\n[bold]Horário {uf} {turno}º turno[/bold] "
                f"[dim]({'detalhe' if detalhe else 'curva'})[/dim]"
            )
            try:
                if detalhe:
                    df = compute_horario(uf, turno)  # classify já recebe uf
                    por_hora = aggregate_por_hora(df)
                    summary = summarize_horario(df)
                    paths = write_horario_reports(
                        por_hora, summary, uf, turno, detail=df
                    )
                else:

                    def _on_prog(
                        done_logs: int,
                        total_logs: int,
                        hab: int,
                        lote_i: int,
                        n_lotes: int,
                    ) -> None:
                        progress.update(
                            task,
                            description=(
                                f"{uf} {done_logs:,}/{total_logs:,} logs "
                                f"· lote {lote_i}/{n_lotes} · {hab:,} hab"
                            ),
                        )

                    por_hora, summary = compute_horario_curva(
                        uf, turno, workers=workers, on_progress=_on_prog
                    )
                    paths = write_horario_reports(por_hora, summary, uf, turno)
            except FileNotFoundError as exc:
                console.print(f"[red]Pulando {uf}:[/red] {exc}")
                progress.advance(task)
                continue

            print_horario_summary(summary, por_hora, uf, turno)
            outputs.extend(paths)
            console.print(f"[green]Relatório:[/green] {paths[-1]}")
            done.append(uf)
            progress.advance(task)

    # consolida todas as UFs do turno que tenham CSV (não só as desta rodada)
    all_ufs = sorted(
        {
            p.name.replace("curva_horaria_", "")
            .replace("horario_por_hora_", "")
            .replace(f"_{turno}t.csv", "")
            for p in list(REPORTS_DIR.glob(f"curva_horaria_*_{turno}t.csv"))
            + list(REPORTS_DIR.glob(f"horario_por_hora_*_{turno}t.csv"))
            if "MULTI" not in p.name
        }
    )
    if len(all_ufs) > 1:
        cons = consolidate_horario(all_ufs, turno)
        if cons:
            console.print(f"\n[green]Curva multi-UF:[/green] {cons[0]} ({len(all_ufs)} UFs)")
            outputs.extend(cons)
    return outputs
