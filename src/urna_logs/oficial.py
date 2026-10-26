"""Cruzamento BU/RDV (audit) × resultado oficial divulgado (CSV TSE)."""

from __future__ import annotations

import zipfile
from pathlib import Path

import httpx
import pandas as pd
from rich.console import Console
from rich.table import Table

from urna_logs.audit import join_key
from urna_logs.config import ANO, DATA_DIR, REPORTS_DIR, ensure_dirs

console = Console()

REF_DIR = DATA_DIR / "ref"

# Presidente — votação por seção (todas as UFs, cargo 1)
VOTACAO_PRESIDENTE_URL = (
    f"https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/"
    f"votacao_secao_{ANO}_BR.zip"
)
VOTACAO_PRESIDENTE_ZIP = REF_DIR / f"votacao_secao_{ANO}_BR.zip"

# Códigos TSE de votável especial (votação por seção)
VOTAVEL_BRANCO = "95"
VOTAVEL_NULO = "96"

_USECOLS = [
    "SG_UF",
    "CD_MUNICIPIO",
    "NR_ZONA",
    "NR_SECAO",
    "CD_CARGO",
    "NR_VOTAVEL",
    "NM_VOTAVEL",
    "QT_VOTOS",
    "NR_TURNO",
]


def _ensure_ref() -> None:
    ensure_dirs()
    REF_DIR.mkdir(parents=True, exist_ok=True)


def cache_path(uf: str, turno: int) -> Path:
    return REF_DIR / f"oficial_presidente_votos_{uf.upper()}_{turno}t.parquet"


def ensure_votacao_presidente_zip(*, force: bool = False) -> Path:
    """Baixa (com cache) o ZIP nacional de votação por seção — presidente."""
    _ensure_ref()
    if VOTACAO_PRESIDENTE_ZIP.exists() and not force:
        size = VOTACAO_PRESIDENTE_ZIP.stat().st_size
        if size > 1_000_000:
            console.print(
                f"[dim]Oficial já em cache:[/dim] {VOTACAO_PRESIDENTE_ZIP.name} "
                f"({size / 1e6:.0f} MB)"
            )
            return VOTACAO_PRESIDENTE_ZIP

    console.print(f"[cyan]Baixando resultado oficial (presidente × seção)…[/cyan]")
    console.print(f"[dim]{VOTACAO_PRESIDENTE_URL}[/dim]")
    tmp = VOTACAO_PRESIDENTE_ZIP.with_suffix(".zip.part")
    with httpx.Client(timeout=600.0, follow_redirects=True) as client:
        with client.stream("GET", VOTACAO_PRESIDENTE_URL) as resp:
            resp.raise_for_status()
            with open(tmp, "wb") as fh:
                for chunk in resp.iter_bytes():
                    fh.write(chunk)
    tmp.replace(VOTACAO_PRESIDENTE_ZIP)
    console.print(
        f"[green]Salvo:[/green] {VOTACAO_PRESIDENTE_ZIP} "
        f"({VOTACAO_PRESIDENTE_ZIP.stat().st_size / 1e6:.0f} MB)"
    )
    return VOTACAO_PRESIDENTE_ZIP


def _mun_int(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lstrip("0").replace("", "0").astype(int)


_EMPTY_OFICIAL = pd.DataFrame(
    columns=[
        "uf",
        "turno",
        "join_key",
        "municipio",
        "zona",
        "secao",
        "votavel",
        "nome_votavel",
        "votos_oficial",
    ]
)


def _normalize_oficial_chunk(raw: pd.DataFrame, turno: int) -> pd.DataFrame:
    if raw.empty:
        return _EMPTY_OFICIAL.copy()
    uf_series = raw["SG_UF"].str.upper()
    municipio = _mun_int(raw["CD_MUNICIPIO"])
    zona = raw["NR_ZONA"].astype(int)
    secao = raw["NR_SECAO"].astype(int)
    frame = pd.DataFrame(
        {
            "uf": uf_series,
            "turno": turno,
            "join_key": [
                join_key(u, m, z, s)
                for u, m, z, s in zip(uf_series, municipio, zona, secao)
            ],
            "municipio": municipio,
            "zona": zona,
            "secao": secao,
            "votavel": raw["NR_VOTAVEL"].astype(str).str.lstrip("0").replace("", "0"),
            "nome_votavel": raw["NM_VOTAVEL"],
            "votos_oficial": raw["QT_VOTOS"].astype(int),
        }
    )
    return (
        frame.groupby(
            ["uf", "turno", "join_key", "municipio", "zona", "secao", "votavel"],
            as_index=False,
        ).agg(
            votos_oficial=("votos_oficial", "sum"),
            nome_votavel=("nome_votavel", "first"),
        )
    )


def warm_oficial_cache(
    ufs: list[str], turno: int, *, force_rebuild: bool = False
) -> None:
    """Uma passagem no ZIP nacional → Parquets por UF (só as que faltam)."""
    wanted = [u.upper() for u in ufs]
    missing = [
        u
        for u in wanted
        if force_rebuild or not cache_path(u, turno).exists()
    ]
    if not missing:
        return

    zpath = ensure_votacao_presidente_zip()
    missing_set = set(missing)
    console.print(
        f"[cyan]Extraindo oficial[/cyan] {turno}º turno · "
        f"{len(missing)} UF(s) do ZIP nacional…"
    )
    buckets: dict[str, list[pd.DataFrame]] = {u: [] for u in missing}
    with zipfile.ZipFile(zpath) as zf:
        csv_name = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
        with zf.open(csv_name) as fh:
            for chunk in pd.read_csv(
                fh,
                sep=";",
                encoding="latin-1",
                dtype=str,
                usecols=_USECOLS,
                chunksize=400_000,
            ):
                m = chunk[
                    (chunk["SG_UF"].str.upper().isin(missing_set))
                    & (chunk["NR_TURNO"] == str(turno))
                    & (chunk["CD_CARGO"] == "1")
                ]
                if m.empty:
                    continue
                for uf, part in m.groupby(m["SG_UF"].str.upper()):
                    buckets[str(uf)].append(part)

    for uf in missing:
        parts = buckets.get(uf, [])
        if not parts:
            out = _EMPTY_OFICIAL.copy()
        else:
            out = _normalize_oficial_chunk(pd.concat(parts, ignore_index=True), turno)
        path = cache_path(uf, turno)
        out.to_parquet(path, index=False)
        console.print(f"[green]Cache oficial:[/green] {path.name} ({len(out):,} linhas)")


def load_oficial_votos(
    uf: str, turno: int, *, force_rebuild: bool = False
) -> pd.DataFrame:
    """Votos oficiais de presidente por seção (uma linha por join_key × votável)."""
    uf = uf.upper()
    warm_oficial_cache([uf], turno, force_rebuild=force_rebuild)
    cached = cache_path(uf, turno)
    if cached.exists():
        return pd.read_parquet(cached)
    return _EMPTY_OFICIAL.copy()


def audit_votavel(tipo: str, numero) -> str | None:
    """Mapeia tipo/número do Parquet da audit → NR_VOTAVEL do TSE."""
    if tipo == "branco":
        return VOTAVEL_BRANCO
    if tipo == "nulo":
        return VOTAVEL_NULO
    if tipo != "nominal":
        return None
    if numero is None or (isinstance(numero, float) and pd.isna(numero)):
        return None
    return str(int(numero))


def load_audit_votos(uf: str, turno: int) -> pd.DataFrame:
    path = REPORTS_DIR / f"audit_presidente_votos_{uf.upper()}_{turno}t.parquet"
    if not path.exists():
        raise FileNotFoundError(
            f"Parquet da audit ausente: {path}. Rode `urna-logs audit --ufs {uf}` antes."
        )
    df = pd.read_parquet(path)
    df = df.copy()
    df["votavel"] = [
        audit_votavel(t, n) for t, n in zip(df["tipo"], df["numero"], strict=False)
    ]
    df = df[df["votavel"].notna()]
    return (
        df.groupby(["uf", "turno", "join_key", "municipio", "zona", "secao", "votavel"], as_index=False)[
            "votos_bu"
        ]
        .sum()
        .rename(columns={"votos_bu": "votos_bu"})
    )


def cruzar_uf(uf: str, turno: int, *, force_rebuild: bool = False) -> pd.DataFrame:
    """Outer join audit × oficial; coluna ok / diff por (seção, votável)."""
    uf = uf.upper()
    audit = load_audit_votos(uf, turno)
    oficial = load_oficial_votos(uf, turno, force_rebuild=force_rebuild)
    merged = audit.merge(
        oficial[
            ["join_key", "votavel", "votos_oficial", "nome_votavel"]
        ],
        on=["join_key", "votavel"],
        how="outer",
        indicator=True,
    )
    merged["uf"] = merged["uf"].fillna(uf)
    merged["turno"] = merged["turno"].fillna(turno).astype(int)
    for col in ("municipio", "zona", "secao"):
        if col in merged.columns:
            merged[col] = merged[col]
    merged["votos_bu"] = merged["votos_bu"].fillna(0).astype(int)
    merged["votos_oficial"] = merged["votos_oficial"].fillna(0).astype(int)
    merged["diff"] = merged["votos_bu"] - merged["votos_oficial"]
    merged["ok"] = (
        (merged["diff"] == 0)
        & (merged["_merge"] == "both")
    )
    merged["lado"] = merged["_merge"].map(
        {
            "both": "ambos",
            "left_only": "só_audit",
            "right_only": "só_oficial",
        }
    )
    return merged.drop(columns=["_merge"])


def summarize_cruzamento(df: pd.DataFrame) -> dict:
    secoes = df.groupby("join_key", dropna=False)
    secao_ok = secoes["ok"].all()
    return {
        "linhas": int(len(df)),
        "linhas_ok": int(df["ok"].sum()),
        "linhas_divergentes": int((~df["ok"]).sum()),
        "secoes": int(secao_ok.shape[0]),
        "secoes_ok": int(secao_ok.sum()),
        "secoes_divergentes": int((~secao_ok).sum()),
        "votos_bu": int(df["votos_bu"].sum()),
        "votos_oficial": int(df["votos_oficial"].sum()),
        "so_audit": int((df["lado"] == "só_audit").sum()),
        "so_oficial": int((df["lado"] == "só_oficial").sum()),
    }


def write_cruzamento_report(
    df: pd.DataFrame, summary: dict, uf: str, turno: int
) -> tuple[Path, Path, Path]:
    ensure_dirs()
    uf = uf.upper()
    md = REPORTS_DIR / f"cruzar_oficial_{uf}_{turno}t.md"
    pq = REPORTS_DIR / f"cruzar_oficial_{uf}_{turno}t.parquet"
    csv = REPORTS_DIR / f"cruzar_oficial_summary_{uf}_{turno}t.csv"

    diverg = df[~df["ok"]].sort_values(["join_key", "votavel"])
    lines = [
        f"# Cruzamento oficial — presidente — {uf} {turno}º turno",
        "",
        "Camada: **BU (audit)** × **CSV oficial** (`votacao_secao_*_BR`, cargo presidente).",
        "",
        "## Resumo",
        "",
        f"- Seções: **{summary['secoes']:,}** · OK: **{summary['secoes_ok']:,}** · "
        f"divergentes: **{summary['secoes_divergentes']:,}**",
        f"- Linhas (seção × votável): **{summary['linhas']:,}** · OK: **{summary['linhas_ok']:,}** · "
        f"divergentes: **{summary['linhas_divergentes']:,}**",
        f"- Votos BU: **{summary['votos_bu']:,}** · oficial: **{summary['votos_oficial']:,}**",
        f"- Só na audit: **{summary['so_audit']:,}** · só no oficial: **{summary['so_oficial']:,}**",
        "",
        "## Divergências",
        "",
    ]
    if diverg.empty:
        lines.append("Nenhuma divergência encontrada.")
    else:
        lines.append(f"{len(diverg):,} linha(s) com diferença (até 40):")
        lines.append("")
        lines.append("| join_key | votável | BU | oficial | diff | lado |")
        lines.append("|---|---:|---:|---:|---:|---|")
        for _, row in diverg.head(40).iterrows():
            lines.append(
                f"| `{row['join_key']}` | {row['votavel']} | {int(row['votos_bu']):,} | "
                f"{int(row['votos_oficial']):,} | {int(row['diff']):,} | {row['lado']} |"
            )
        if len(diverg) > 40:
            lines.append(f"| … | | | | | +{len(diverg) - 40} |")

    lines += [
        "",
        "## Método",
        "",
        "- Chave: `join_key` = UF:municipio:zona:secao",
        "- Votável: número do candidato; branco=`95`; nulo=`96` (padrão TSE)",
        "- Fonte oficial: "
        f"[Resultados 2026 — presidente por seção]({VOTACAO_PRESIDENTE_URL})",
        "",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")
    df.to_parquet(pq, index=False)
    pd.DataFrame([{**summary, "uf": uf, "turno": turno}]).to_csv(csv, index=False)
    return md, pq, csv


def print_cruzamento_summary(summary: dict, uf: str, turno: int) -> None:
    console.print(f"\n[bold]Cruzamento oficial — {uf.upper()} {turno}º turno[/bold]")
    table = Table()
    table.add_column("Métrica")
    table.add_column("Valor", justify="right")
    table.add_row("Seções OK", f"{summary['secoes_ok']:,} / {summary['secoes']:,}")
    table.add_row(
        "Linhas OK", f"{summary['linhas_ok']:,} / {summary['linhas']:,}"
    )
    table.add_row("Votos BU", f"{summary['votos_bu']:,}")
    table.add_row("Votos oficial", f"{summary['votos_oficial']:,}")
    table.add_row("Divergentes", f"{summary['linhas_divergentes']:,}")
    console.print(table)


def consolidate_cruzamento(ufs: list[str], turno: int) -> Path | None:
    frames: list[pd.DataFrame] = []
    for uf in ufs:
        p = REPORTS_DIR / f"cruzar_oficial_summary_{uf.upper()}_{turno}t.csv"
        if p.exists():
            frames.append(pd.read_csv(p))
    if not frames:
        return None
    out = REPORTS_DIR / f"cruzar_oficial_summary_MULTI_{turno}t.csv"
    pd.concat(frames, ignore_index=True).to_csv(out, index=False)
    return out


def run_cruzar_oficial(
    ufs: list[str],
    turno: int,
    *,
    force_download: bool = False,
    force_rebuild: bool = False,
) -> list[Path]:
    ensure_votacao_presidente_zip(force=force_download)
    uf_list = [u.upper() for u in ufs]
    # Só aquece cache das UFs que já têm audit (evita extrair SP cedo demais)
    ready = [
        u
        for u in uf_list
        if (REPORTS_DIR / f"audit_presidente_votos_{u}_{turno}t.parquet").exists()
    ]
    if ready:
        warm_oficial_cache(ready, turno, force_rebuild=force_rebuild)

    outputs: list[Path] = []
    done: list[str] = []
    for i, uf in enumerate(uf_list, start=1):
        console.print(f"\n[bold][{i}/{len(uf_list)}] Cruzando {uf}[/bold]")
        try:
            df = cruzar_uf(uf, turno, force_rebuild=False)
        except FileNotFoundError as exc:
            console.print(f"[red]Pulando {uf}:[/red] {exc}")
            continue
        summary = summarize_cruzamento(df)
        print_cruzamento_summary(summary, uf, turno)
        md, pq, csv = write_cruzamento_report(df, summary, uf, turno)
        console.print(f"[green]Relatório:[/green] {md}")
        console.print(f"[green]Parquet:[/green] {pq}")
        outputs.extend([md, pq, csv])
        done.append(uf)
    if len(done) > 1:
        multi = consolidate_cruzamento(done, turno)
        if multi:
            console.print(f"\n[green]Resumo multi-UF:[/green] {multi}")
            outputs.append(multi)
    return outputs
