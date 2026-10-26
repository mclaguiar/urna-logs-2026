"""Agregados por município: votos presidente + habilitação (BU)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.table import Table

from urna_logs.config import REPORTS_DIR, ensure_dirs
from urna_logs.municipios import ensure_municipios

console = Console()


def _audit_csv(uf: str, turno: int) -> Path:
    return REPORTS_DIR / f"audit_presidente_{uf.upper()}_{turno}t.csv"


def load_audit(uf: str, turno: int) -> pd.DataFrame:
    path = _audit_csv(uf, turno)
    if not path.exists():
        raise FileNotFoundError(
            f"CSV de auditoria ausente: {path}. Rode `urna-logs audit --ufs {uf} --turno {turno}`."
        )
    return pd.read_csv(path)


def aggregate_by_municipio(df: pd.DataFrame, nomes: pd.DataFrame) -> pd.DataFrame:
    """Agrega urnas OK por município (fonte BU)."""
    ok = df[df["ok"] == True].copy()  # noqa: E712
    if ok.empty:
        return pd.DataFrame()

    # Exterior (ZZ) e alguns BUs omitem detalhamentoComparecimento → NaN
    has_bio = ok["bio"].notna() | ok["biografia"].notna() | ok["sem_biometria"].notna()
    ok["bio_detalhe_ok"] = has_bio

    g = (
        ok.groupby(["uf", "municipio"], as_index=False)
        .agg(
            urnas=("stem", "count"),
            aptos=("aptos", "sum"),
            comparecimento=("bu_comparecimento", "sum"),
            votos_presidente=("bu_total", "sum"),
            bio=("bio", "sum"),
            biografia=("biografia", "sum"),
            sem_biometria=("sem_biometria", "sum"),
            urnas_com_bio_detalhe=("bio_detalhe_ok", "sum"),
        )
    )
    all_g = (
        df.groupby(["uf", "municipio"], as_index=False)
        .agg(urnas_divergentes=("ok", lambda s: int((~s).sum())))
    )
    g = g.merge(all_g, on=["uf", "municipio"], how="left")

    # Soma de NaNs no pandas vira 0 — distinguir "zero real" de "sem dado"
    sem_dado = g["urnas_com_bio_detalhe"] == 0
    g.loc[sem_dado, ["bio", "biografia", "sem_biometria"]] = pd.NA

    g["sem_digital"] = g["sem_biometria"] + g["biografia"]
    with_comp = g["comparecimento"] > 0
    g["pct_bio"] = pd.NA
    g["pct_biografia"] = pd.NA
    g["pct_sem_biometria"] = pd.NA
    g["pct_sem_digital"] = pd.NA
    mask = with_comp & ~sem_dado
    g.loc[mask, "pct_bio"] = (100 * g.loc[mask, "bio"] / g.loc[mask, "comparecimento"]).astype(float).round(4)
    g.loc[mask, "pct_biografia"] = (
        100 * g.loc[mask, "biografia"] / g.loc[mask, "comparecimento"]
    ).astype(float).round(4)
    g.loc[mask, "pct_sem_biometria"] = (
        100 * g.loc[mask, "sem_biometria"] / g.loc[mask, "comparecimento"]
    ).astype(float).round(4)
    g.loc[mask, "pct_sem_digital"] = (
        100 * g.loc[mask, "sem_digital"] / g.loc[mask, "comparecimento"]
    ).astype(float).round(4)

    g["pct_comparecimento"] = pd.NA
    with_aptos = g["aptos"].notna() & (g["aptos"] > 0)
    g.loc[with_aptos, "pct_comparecimento"] = (
        100 * g.loc[with_aptos, "comparecimento"] / g.loc[with_aptos, "aptos"]
    ).astype(float).round(4)

    nomes_u = nomes[["uf", "municipio", "nome"]].drop_duplicates()
    g = g.merge(nomes_u, on=["uf", "municipio"], how="left")
    g["nome"] = g["nome"].fillna("(desconhecido)")

    cols = [
        "uf",
        "municipio",
        "nome",
        "urnas",
        "urnas_divergentes",
        "urnas_com_bio_detalhe",
        "aptos",
        "comparecimento",
        "pct_comparecimento",
        "votos_presidente",
        "bio",
        "biografia",
        "sem_biometria",
        "sem_digital",
        "pct_bio",
        "pct_biografia",
        "pct_sem_biometria",
        "pct_sem_digital",
    ]
    # Municípios com dado de biometria primeiro (maior % sem digital); sem dado no fim
    g["_sort_sem"] = g["pct_sem_digital"].fillna(-1)
    return g[cols + ["_sort_sem"]].sort_values(
        ["uf", "_sort_sem", "nome"], ascending=[True, False, True]
    ).drop(columns=["_sort_sem"])


def write_municipio_report(agg: pd.DataFrame, uf: str, turno: int) -> tuple[Path, Path]:
    ensure_dirs()
    uf = uf.upper()
    csv_path = REPORTS_DIR / f"by_municipio_{uf}_{turno}t.csv"
    md_path = REPORTS_DIR / f"by_municipio_{uf}_{turno}t.md"
    agg.to_csv(csv_path, index=False)

    total_comp = int(agg["comparecimento"].sum()) if not agg.empty else 0
    com_bio = agg[agg["pct_sem_digital"].notna()]
    total_sem = int(com_bio["sem_digital"].sum()) if not com_bio.empty else 0
    total_comp_bio = int(com_bio["comparecimento"].sum()) if not com_bio.empty else 0
    pct = round(100 * total_sem / total_comp_bio, 4) if total_comp_bio else None
    sem_detalhe = int((agg["urnas_com_bio_detalhe"] == 0).sum()) if not agg.empty else 0

    resumo = f"Municípios: **{len(agg):,}** · Comparecimento: **{total_comp:,}**"
    if pct is not None:
        resumo += f" · % sem digital (UF): **{pct}%**"
    if sem_detalhe:
        resumo += f" · sem detalhe biométrico no BU: **{sem_detalhe}** município(s)"

    def _fmt(v) -> str:
        if pd.isna(v):
            return "—"
        if isinstance(v, float):
            return f"{v}%"
        return f"{int(v):,}"

    lines = [
        f"# Por município — {uf} {turno}º turno (presidente + habilitação BU)",
        "",
        resumo,
        "",
        "## Definições (BU)",
        "",
        "- **bio**: habilitados com reconhecimento biométrico",
        "- **biografia**: tinham biometria cadastrada, liberados por ano de nascimento",
        "- **sem_biometria**: compareceram sem biometria cadastrada",
        "- **sem digital** = biografia + sem_biometria",
        "- Exterior (ZZ) e alguns BUs podem omitir o detalhamento → campos `—`",
        "",
        "## Ranking por % sem digital",
        "",
        "| Município | Urnas | Comparec. | % bio | % biografia | % sem bio | % sem digital | Votos pres. |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for _, row in agg.iterrows():
        lines.append(
            f"| {row['nome']} ({row['municipio']}) | {int(row['urnas']):,} | "
            f"{int(row['comparecimento']):,} | {_fmt(row['pct_bio'])} | {_fmt(row['pct_biografia'])} | "
            f"{_fmt(row['pct_sem_biometria'])} | **{_fmt(row['pct_sem_digital'])}** | "
            f"{int(row['votos_presidente']):,} |"
        )
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path, csv_path


def print_municipio_summary(agg: pd.DataFrame, uf: str, turno: int, *, top: int = 15) -> None:
    console.print(f"\n[bold]Por município — {uf.upper()} {turno}º turno[/bold]")
    if agg.empty:
        console.print("[yellow]Sem dados[/yellow]")
        return
    total_comp = int(agg["comparecimento"].sum())
    com_bio = agg[agg["pct_sem_digital"].notna()]
    table = Table()
    table.add_column("Métrica")
    table.add_column("Valor", justify="right")
    table.add_row("Municípios", f"{len(agg):,}")
    table.add_row("Urnas", f"{int(agg['urnas'].sum()):,}")
    table.add_row("Comparecimento", f"{total_comp:,}")
    if not com_bio.empty:
        total_sem = int(com_bio["sem_digital"].sum())
        total_comp_bio = int(com_bio["comparecimento"].sum())
        table.add_row("% sem digital (UF)", f"{100 * total_sem / total_comp_bio:.4f}%")
    else:
        table.add_row("% sem digital (UF)", "— (BU sem detalhe)")
    console.print(table)

    ranked = com_bio if not com_bio.empty else agg
    top_t = Table(title=f"Top {top} % sem digital" if not com_bio.empty else f"Top {top} municípios")
    top_t.add_column("Município")
    top_t.add_column("Comp.", justify="right")
    top_t.add_column("% bio", justify="right")
    top_t.add_column("% sem dig.", justify="right")
    for _, row in ranked.head(top).iterrows():
        pct_bio = "—" if pd.isna(row["pct_bio"]) else f"{row['pct_bio']}%"
        pct_sd = "—" if pd.isna(row["pct_sem_digital"]) else f"{row['pct_sem_digital']}%"
        top_t.add_row(str(row["nome"]), f"{int(row['comparecimento']):,}", pct_bio, pct_sd)
    console.print(top_t)


def run_by_municipio(ufs: list[str], turno: int) -> list[Path]:
    ensure_dirs()
    nomes = ensure_municipios(ufs)
    outputs: list[Path] = []
    frames: list[pd.DataFrame] = []
    for uf in ufs:
        uf = uf.upper()
        console.print(f"\n[bold]Agregando {uf}[/bold]")
        df = load_audit(uf, turno)
        agg = aggregate_by_municipio(df, nomes)
        md, csv = write_municipio_report(agg, uf, turno)
        print_municipio_summary(agg, uf, turno)
        console.print(f"[green]Relatório:[/green] {md}")
        console.print(f"[green]CSV:[/green] {csv}")
        outputs.extend([md, csv])
        if not agg.empty:
            frames.append(agg)

    if len(frames) > 1:
        all_df = pd.concat(frames, ignore_index=True)
        all_csv = REPORTS_DIR / f"by_municipio_MULTI_{turno}t.csv"
        all_df.to_csv(all_csv, index=False)
        outputs.append(all_csv)
        console.print(f"\n[green]Consolidado multi-UF:[/green] {all_csv}")
    return outputs
