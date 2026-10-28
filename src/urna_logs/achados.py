"""
Achados de auditoria — hierarquia de evidência A / B / C.

Nível A — inconsistência documental (cadeia pública).
Nível B — anomalia operacional (confluência de sinais).
Nível C — padrão ecológico / contexto (não sustenta fraude sozinho).

Gera fichas reproduzíveis por seção (`join_key`) + resumo UF.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.table import Table

from urna_logs import __version__ as PKG_VERSION
from urna_logs.config import REPORTS_DIR, ensure_dirs
from urna_logs.thresholds import (
    CONFLUENCIA_FLAGS,
    CONFLUENCIA_MIN,
    PROTOCOLO_NOTA,
    PROTOCOLO_VERSAO,
)

console = Console()


NIVEL_A = "A"
NIVEL_B = "B"
NIVEL_C = "C"

NIVEL_DESC = {
    NIVEL_A: "Inconsistência documental (cadeia pública)",
    NIVEL_B: "Anomalia operacional (confluência de sinais)",
    NIVEL_C: "Padrão ecológico / contexto (não é indício de fraude sozinho)",
}


def _load_compare(uf: str) -> pd.DataFrame | None:
    p = REPORTS_DIR / f"comparar_turnos_{uf.upper()}_1t_2t.parquet"
    if not p.exists():
        return None
    return pd.read_parquet(p)


def _load_audit_fails(uf: str, turno: int) -> set[str]:
    p = REPORTS_DIR / f"audit_presidente_{uf.upper()}_{turno}t.parquet"
    if not p.exists():
        return set()
    df = pd.read_parquet(p, columns=["join_key", "ok"])
    return set(df.loc[df["ok"] == False, "join_key"].astype(str))  # noqa: E712


def _load_cruzar_divergent(uf: str, turno: int) -> set[str]:
    p = REPORTS_DIR / f"cruzar_oficial_{uf.upper()}_{turno}t.parquet"
    if not p.exists():
        return set()
    df = pd.read_parquet(p)
    if "ok" not in df.columns or "join_key" not in df.columns:
        return set()
    return set(df.loc[df["ok"] == False, "join_key"].astype(str).unique())  # noqa: E712


def _load_elim_forced(uf: str) -> pd.DataFrame:
    p = REPORTS_DIR / f"fluxo_bounds_{uf.upper()}_1t_2t.parquet"
    if not p.exists():
        return pd.DataFrame(columns=["join_key", "elim_forced_fa", "elim_forced_fb"])
    cols = [c for c in ("join_key", "elim_forced_fa", "elim_forced_fb") if True]
    df = pd.read_parquet(p)
    keep = [c for c in cols if c in df.columns]
    return df[keep] if keep else pd.DataFrame(columns=["join_key"])


def classify_row(
    row: pd.Series,
    *,
    audit_fail_1t: set[str],
    audit_fail_2t: set[str],
    cruzar_1t: set[str],
    cruzar_2t: set[str],
) -> tuple[str, list[str], str]:
    """
    Retorna (nivel, codigos, conclusao_permitida).
    """
    jk = str(row.get("join_key", ""))
    codes: list[str] = []

    # --- Nível A ---
    if jk in audit_fail_1t:
        codes.append("A_audit_rdv_bu_1t")
    if jk in audit_fail_2t:
        codes.append("A_audit_rdv_bu_2t")
    if jk in cruzar_1t:
        codes.append("A_cruzar_bu_oficial_1t")
    if jk in cruzar_2t:
        codes.append("A_cruzar_bu_oficial_2t")
    status = str(row.get("status", ""))
    if status in ("so_1t", "so_2t"):
        codes.append(f"A_secao_{status}")

    if any(c.startswith("A_") for c in codes):
        return (
            NIVEL_A,
            codes,
            "Indício documental de inconsistência entre arquivos públicos "
            "ou cobertura incompleta da seção entre turnos. "
            "Não prova fraude no hardware; justifica checagem da cadeia.",
        )

    # --- Nível B: confluência ou regra composta pré-registrada ---
    n_conf = sum(1 for f in CONFLUENCIA_FLAGS if bool(row.get(f)))
    if bool(row.get("flag_sem_digital_x_margem")):
        codes.append("B_sem_digital_x_margem")
    if bool(row.get("flag_margem")) and bool(row.get("flag_pos17")):
        codes.append("B_margem_x_pos17")
    if bool(row.get("flag_margem")) and bool(row.get("flag_abstencao")):
        codes.append("B_margem_x_abstencao")
    if n_conf >= CONFLUENCIA_MIN:
        codes.append(f"B_confluencia_{n_conf}")

    if any(c.startswith("B_") for c in codes):
        return (
            NIVEL_B,
            codes,
            "Anomalia operacional agregada (confluência de sinais). "
            "Priorizar para revisão; não equivale a fraude comprovada.",
        )

    # --- Nível C: flags isoladas / ecológico ---
    if bool(row.get("flag_margem")):
        codes.append("C_margem_isolada")
    if bool(row.get("flag_abstencao")):
        codes.append("C_abstencao_isolada")
    if bool(row.get("flag_pos17")):
        codes.append("C_pos17_isolada")
    if bool(row.get("elim_forced_fa")):
        codes.append("C_elim_forcado_fa")
    if bool(row.get("elim_forced_fb")):
        codes.append("C_elim_forcado_fb")

    if codes:
        return (
            NIVEL_C,
            codes,
            "Padrão agregado / contexto ecológico. "
            "Útil para narrativa de saldos; não sustenta indício de fraude sozinho.",
        )

    return "", [], ""


def build_achados_uf(uf: str) -> pd.DataFrame:
    uf = uf.upper()
    compare = _load_compare(uf)
    if compare is None or compare.empty:
        return pd.DataFrame()

    audit_fail_1t = _load_audit_fails(uf, 1)
    audit_fail_2t = _load_audit_fails(uf, 2)
    cruzar_1t = _load_cruzar_divergent(uf, 1)
    cruzar_2t = _load_cruzar_divergent(uf, 2)
    forced = _load_elim_forced(uf)
    df = compare.copy()
    if not forced.empty and "join_key" in forced.columns:
        df = df.merge(forced, on="join_key", how="left")
    for col in ("elim_forced_fa", "elim_forced_fb"):
        if col not in df.columns:
            df[col] = False
        else:
            df[col] = df[col].fillna(False).astype(bool)

    rows = []
    for _, row in df.iterrows():
        nivel, codes, conclusao = classify_row(
            row,
            audit_fail_1t=audit_fail_1t,
            audit_fail_2t=audit_fail_2t,
            cruzar_1t=cruzar_1t,
            cruzar_2t=cruzar_2t,
        )
        if not nivel:
            continue
        rows.append(
            {
                "uf": uf,
                "join_key": row.get("join_key"),
                "municipio": row.get("municipio"),
                "zona": row.get("zona"),
                "secao": row.get("secao"),
                "nivel": nivel,
                "nivel_desc": NIVEL_DESC[nivel],
                "codigos": "|".join(codes),
                "conclusao_permitida": conclusao,
                "status": row.get("status"),
                "delta_margem": row.get("delta_margem"),
                "delta_abstencao": row.get("delta_abstencao"),
                "pct_sem_digital_1t": row.get("pct_sem_digital_1t"),
                "pct_apos_17h_2t": row.get("pct_apos_17h_2t"),
                "flags_comparar": row.get("flags"),
                "protocolo_versao": PROTOCOLO_VERSAO,
                "pkg_version": PKG_VERSION,
            }
        )
    if not rows:
        return pd.DataFrame(
            columns=[
                "uf",
                "join_key",
                "nivel",
                "codigos",
                "conclusao_permitida",
                "protocolo_versao",
            ]
        )
    out = pd.DataFrame(rows)
    # ordenar: A, B, C; dentro por |delta_margem|
    order = {NIVEL_A: 0, NIVEL_B: 1, NIVEL_C: 2}
    out["_ord"] = out["nivel"].map(order)
    out["_abs_m"] = pd.to_numeric(out["delta_margem"], errors="coerce").abs().fillna(0)
    out = out.sort_values(["_ord", "_abs_m"], ascending=[True, False]).drop(
        columns=["_ord", "_abs_m"]
    )
    return out.reset_index(drop=True)


def summarize_achados(df: pd.DataFrame, uf: str) -> dict:
    if df.empty:
        return {
            "uf": uf.upper(),
            "n_achados": 0,
            "n_A": 0,
            "n_B": 0,
            "n_C": 0,
            "protocolo_versao": PROTOCOLO_VERSAO,
            "go_auditoria": True,
            "mensagem": "Nenhum achado classificado (sem flags / divergências).",
        }
    n_a = int((df["nivel"] == NIVEL_A).sum())
    n_b = int((df["nivel"] == NIVEL_B).sum())
    n_c = int((df["nivel"] == NIVEL_C).sum())
    return {
        "uf": uf.upper(),
        "n_achados": len(df),
        "n_A": n_a,
        "n_B": n_b,
        "n_C": n_c,
        "protocolo_versao": PROTOCOLO_VERSAO,
        # go_auditoria aqui = pipeline ok; achados A não são “falha do software”
        "go_auditoria": True,
        "mensagem": PROTOCOLO_NOTA,
    }


def write_fichas(
    df: pd.DataFrame, meta: dict, uf: str, *, max_fichas: int = 40
) -> tuple[Path, Path, Path]:
    ensure_dirs()
    uf = uf.upper()
    pq = REPORTS_DIR / f"achados_{uf}_1t_2t.parquet"
    csv = REPORTS_DIR / f"achados_summary_{uf}_1t_2t.csv"
    md = REPORTS_DIR / f"achados_{uf}_1t_2t.md"

    df.to_parquet(pq, index=False)
    pd.DataFrame([meta]).to_csv(csv, index=False)

    lines = [
        f"# Achados de auditoria — {uf} (1º×2º)",
        "",
        f"Protocolo **{PROTOCOLO_VERSAO}** · pacote `{PKG_VERSION}`",
        "",
        PROTOCOLO_NOTA,
        "",
        "## Resumo",
        "",
        f"- Total classificado: **{meta['n_achados']:,}**",
        f"- Nível A (documental): **{meta['n_A']:,}**",
        f"- Nível B (operacional): **{meta['n_B']:,}**",
        f"- Nível C (contexto): **{meta['n_C']:,}**",
        "",
        "## Hierarquia",
        "",
        "| Nível | Significado | Uso em auditoria |",
        "|---|---|---|",
        "| **A** | Inconsistência entre arquivos públicos / cobertura | "
        "Indício documental — listar e checar cadeia |",
        "| **B** | Confluência de sinais operacionais | "
        "Priorizar revisão; não = fraude comprovada |",
        "| **C** | Flag isolada ou padrão ecológico | "
        "Contexto / saldos; **não** sustenta fraude sozinho |",
        "",
        "## Fichas (até {} por UF, A→B→C)".format(max_fichas),
        "",
    ]

    show = df.head(max_fichas)
    if show.empty:
        lines.append("_Nenhuma ficha._")
    else:
        for i, row in enumerate(show.itertuples(index=False), start=1):
            lines += [
                f"### Ficha {i} — Nível {row.nivel} — `{row.join_key}`",
                "",
                f"- **Códigos:** `{row.codigos}`",
                f"- **Status turno:** {row.status}",
                f"- Δ margem: **{row.delta_margem}** · Δ abstenção: **{row.delta_abstencao}**",
                f"- % sem digital 1º: **{row.pct_sem_digital_1t}** · "
                f"% ≥17h 2º: **{row.pct_apos_17h_2t}**",
                f"- Flags comparar: `{row.flags_comparar or '—'}`",
                f"- **Conclusão permitida:** {row.conclusao_permitida}",
                f"- **Não concluir:** fraude de hardware; migração eleitor a eleitor; "
                f"intenção a partir só de Nível C.",
                "",
            ]
        if len(df) > max_fichas:
            lines.append(f"_… e mais {len(df) - max_fichas} no Parquet `{pq.name}`_")
            lines.append("")

    lines += [
        "## Reprodução",
        "",
        "```bash",
        f"urna-logs comparar-turnos --ufs {uf}",
        f"urna-logs achados --ufs {uf}",
        "```",
        "",
        f"Artefatos: `{pq.name}`, `{csv.name}`",
        "",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")
    return md, pq, csv


def print_achados_meta(meta: dict) -> None:
    console.print(f"\n[bold]Achados — {meta['uf']}[/bold] · protocolo {meta['protocolo_versao']}")
    table = Table()
    table.add_column("Nível")
    table.add_column("N", justify="right")
    table.add_row("A documental", f"{meta['n_A']:,}")
    table.add_row("B operacional", f"{meta['n_B']:,}")
    table.add_row("C contexto", f"{meta['n_C']:,}")
    table.add_row("Total", f"{meta['n_achados']:,}")
    console.print(table)


def consolidate_achados(ufs: list[str]) -> tuple[Path | None, Path | None]:
    frames = []
    sums = []
    for uf in ufs:
        pq = REPORTS_DIR / f"achados_{uf.upper()}_1t_2t.parquet"
        sm = REPORTS_DIR / f"achados_summary_{uf.upper()}_1t_2t.csv"
        if pq.exists():
            frames.append(pd.read_parquet(pq))
        if sm.exists():
            sums.append(pd.read_csv(sm))
    if not frames:
        return None, None
    out_pq = REPORTS_DIR / "achados_MULTI_1t_2t.parquet"
    out_csv = REPORTS_DIR / "achados_summary_MULTI_1t_2t.csv"
    pd.concat(frames, ignore_index=True).to_parquet(out_pq, index=False)
    if sums:
        pd.concat(sums, ignore_index=True).to_csv(out_csv, index=False)
    return out_pq, out_csv


def run_achados(ufs: list[str]) -> list[Path]:
    outputs: list[Path] = []
    done: list[str] = []
    for i, uf in enumerate(ufs, start=1):
        uf = uf.upper()
        console.print(f"\n[bold][{i}/{len(ufs)}] Achados {uf}[/bold]")
        if _load_compare(uf) is None:
            console.print(
                f"[red]Falta comparar_turnos_{uf}_1t_2t.parquet — "
                f"rode comparar-turnos[/red]"
            )
            continue
        df = build_achados_uf(uf)
        meta = summarize_achados(df, uf)
        print_achados_meta(meta)
        md, pq, csv = write_fichas(df, meta, uf)
        console.print(f"[green]Fichas:[/green] {md}")
        outputs.extend([md, pq, csv])
        done.append(uf)
    if len(done) > 1:
        multi_pq, multi_csv = consolidate_achados(done)
        if multi_pq:
            console.print(f"\n[green]Achados multi-UF:[/green] {multi_pq}")
            outputs.append(multi_pq)
        if multi_csv:
            outputs.append(multi_csv)
    return outputs
