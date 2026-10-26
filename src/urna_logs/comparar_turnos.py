"""Comparativo 1º × 2º turno (seção a seção) — esqueleto até o 2º existir."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.table import Table

from urna_logs.config import REPORTS_DIR, ensure_dirs

console = Console()

# Colunas do comparativo (preenchidas quando ambos os turnos existem)
COMPARE_COLS = [
    "uf",
    "join_key",
    "municipio",
    "zona",
    "secao",
    "aptos_1t",
    "aptos_2t",
    "comparecimento_1t",
    "comparecimento_2t",
    "abstencao_1t",
    "abstencao_2t",
    "delta_comparecimento",
    "delta_abstencao",
    "pct_abstencao_1t",
    "pct_abstencao_2t",
    "bu_total_1t",
    "bu_total_2t",
    "status",  # ambos | so_1t | so_2t | pendente_2t
]


def audit_secoes_path(uf: str, turno: int) -> Path:
    return REPORTS_DIR / f"audit_presidente_{uf.upper()}_{turno}t.parquet"


def horario_summary_path(uf: str, turno: int) -> Path:
    return REPORTS_DIR / f"horario_summary_{uf.upper()}_{turno}t.csv"


def load_secoes(uf: str, turno: int) -> pd.DataFrame | None:
    path = audit_secoes_path(uf, turno)
    if not path.exists():
        return None
    cols = [
        "join_key",
        "municipio",
        "zona",
        "secao",
        "aptos",
        "bu_comparecimento",
        "abstencao",
        "pct_abstencao",
        "bu_total",
        "ok",
    ]
    df = pd.read_parquet(path)
    keep = [c for c in cols if c in df.columns]
    return df[keep].copy()


def empty_compare_frame(uf: str) -> pd.DataFrame:
    return pd.DataFrame(columns=COMPARE_COLS)


def build_compare(uf: str, turno_a: int, turno_b: int) -> tuple[pd.DataFrame, dict]:
    """Monta frame seção a seção. Se turno_b ausente, status=pendente_2t."""
    uf = uf.upper()
    a = load_secoes(uf, turno_a)
    b = load_secoes(uf, turno_b)

    meta = {
        "uf": uf,
        "turno_a": turno_a,
        "turno_b": turno_b,
        "turno_a_disponivel": a is not None,
        "turno_b_disponivel": b is not None,
        "secoes_1t": int(len(a)) if a is not None else 0,
        "secoes_2t": int(len(b)) if b is not None else 0,
        "secoes_ambos": 0,
        "secoes_so_1t": 0,
        "secoes_so_2t": 0,
        "horario_1t_pct_apos_17h": None,
        "horario_2t_pct_apos_17h": None,
        "delta_pct_apos_17h": None,
        "pronto": False,
        "mensagem": "",
    }

    for label, turno in (("1t", turno_a), ("2t", turno_b)):
        hp = horario_summary_path(uf, turno)
        if hp.exists():
            row = pd.read_csv(hp).iloc[0]
            meta[f"horario_{label}_pct_apos_17h"] = (
                float(row["pct_apos_17h"]) if pd.notna(row.get("pct_apos_17h")) else None
            )

    if meta["horario_1t_pct_apos_17h"] is not None and meta["horario_2t_pct_apos_17h"] is not None:
        meta["delta_pct_apos_17h"] = round(
            meta["horario_2t_pct_apos_17h"] - meta["horario_1t_pct_apos_17h"], 4
        )

    if a is None:
        meta["mensagem"] = f"Falta audit do {turno_a}º turno. Rode `urna-logs audit`."
        return empty_compare_frame(uf), meta

    if b is None:
        meta["mensagem"] = (
            f"{turno_b}º turno ainda não disponível "
            f"(sem `{audit_secoes_path(uf, turno_b).name}`). "
            "Esqueleto gravado; rode de novo quando o CDN publicar."
        )
        # Baseline 1t com colunas do 2t vazias — pronto para merge futuro
        out = pd.DataFrame(
            {
                "uf": uf,
                "join_key": a["join_key"],
                "municipio": a["municipio"],
                "zona": a["zona"],
                "secao": a["secao"],
                "aptos_1t": a.get("aptos"),
                "aptos_2t": pd.NA,
                "comparecimento_1t": a.get("bu_comparecimento"),
                "comparecimento_2t": pd.NA,
                "abstencao_1t": a.get("abstencao"),
                "abstencao_2t": pd.NA,
                "delta_comparecimento": pd.NA,
                "delta_abstencao": pd.NA,
                "pct_abstencao_1t": a.get("pct_abstencao"),
                "pct_abstencao_2t": pd.NA,
                "bu_total_1t": a.get("bu_total"),
                "bu_total_2t": pd.NA,
                "status": "pendente_2t",
            }
        )
        meta["secoes_so_1t"] = int(len(out))
        return out, meta

    left = a.rename(
        columns={
            "aptos": "aptos_1t",
            "bu_comparecimento": "comparecimento_1t",
            "abstencao": "abstencao_1t",
            "pct_abstencao": "pct_abstencao_1t",
            "bu_total": "bu_total_1t",
        }
    )
    right = b.rename(
        columns={
            "aptos": "aptos_2t",
            "bu_comparecimento": "comparecimento_2t",
            "abstencao": "abstencao_2t",
            "pct_abstencao": "pct_abstencao_2t",
            "bu_total": "bu_total_2t",
        }
    )
    merged = left.merge(
        right[
            [
                "join_key",
                "aptos_2t",
                "comparecimento_2t",
                "abstencao_2t",
                "pct_abstencao_2t",
                "bu_total_2t",
            ]
        ],
        on="join_key",
        how="outer",
        indicator=True,
    )
    merged["uf"] = uf
    merged["status"] = merged["_merge"].map(
        {"both": "ambos", "left_only": "so_1t", "right_only": "so_2t"}
    )
    merged["delta_comparecimento"] = (
        merged["comparecimento_2t"] - merged["comparecimento_1t"]
    )
    merged["delta_abstencao"] = merged["abstencao_2t"] - merged["abstencao_1t"]
    meta["secoes_ambos"] = int((merged["status"] == "ambos").sum())
    meta["secoes_so_1t"] = int((merged["status"] == "so_1t").sum())
    meta["secoes_so_2t"] = int((merged["status"] == "so_2t").sum())
    meta["pronto"] = True
    meta["mensagem"] = "Comparativo 1º×2º preenchido."
    out = merged.reindex(columns=COMPARE_COLS)
    return out, meta


def write_compare_report(
    df: pd.DataFrame, meta: dict, uf: str, turno_a: int, turno_b: int
) -> tuple[Path, Path, Path]:
    ensure_dirs()
    uf = uf.upper()
    pq = REPORTS_DIR / f"comparar_turnos_{uf}_{turno_a}t_{turno_b}t.parquet"
    csv = REPORTS_DIR / f"comparar_turnos_summary_{uf}_{turno_a}t_{turno_b}t.csv"
    md = REPORTS_DIR / f"comparar_turnos_{uf}_{turno_a}t_{turno_b}t.md"

    df.to_parquet(pq, index=False)
    pd.DataFrame([meta]).to_csv(csv, index=False)

    lines = [
        f"# Comparativo {turno_a}º × {turno_b}º turno — {uf}",
        "",
        f"Status: **{'pronto' if meta['pronto'] else 'esqueleto (aguardando 2º)'}**",
        "",
        meta["mensagem"],
        "",
        "## Disponibilidade",
        "",
        f"- {turno_a}º turno (audit): "
        f"{'sim' if meta['turno_a_disponivel'] else 'não'} · "
        f"{meta['secoes_1t']:,} seções",
        f"- {turno_b}º turno (audit): "
        f"{'sim' if meta['turno_b_disponivel'] else 'não'} · "
        f"{meta['secoes_2t']:,} seções",
        "",
        "## Métricas (quando ambos existirem)",
        "",
        f"- Seções em ambos: **{meta['secoes_ambos']:,}**",
        f"- Só no {turno_a}º: **{meta['secoes_so_1t']:,}** · "
        f"só no {turno_b}º: **{meta['secoes_so_2t']:,}**",
        "",
        "## Pós-17h (quando `horario` existir nos dois turnos)",
        "",
        f"- % ≥17h no {turno_a}º: **{meta['horario_1t_pct_apos_17h']}**",
        f"- % ≥17h no {turno_b}º: **{meta['horario_2t_pct_apos_17h']}**",
        f"- Δ (2º − 1º): **{meta['delta_pct_apos_17h']}**",
        "",
        "## Limites",
        "",
        "- Comparação é **agregada por seção** (`join_key`).",
        "- Não dá para saber *quem* mudou de candidato entre turnos (sigilo do voto).",
        "- “Migração” = mudança dos totais da seção (finalistas, eliminados, abstenção).",
        "",
        "## Próximos campos (quando 2º existir)",
        "",
        "- Votos dos finalistas 1º→2º e margem",
        "- Saldo aparente dos votos de quem ficou fora no 1º",
        "- Brancos/nulos 1º→2º",
        "- Cruzar seções com alto % pós-17h × Δ de resultado",
        "",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")
    return md, pq, csv


def print_compare_meta(meta: dict) -> None:
    console.print(f"\n[bold]Comparativo turnos — {meta['uf']}[/bold]")
    table = Table()
    table.add_column("Campo")
    table.add_column("Valor")
    table.add_row("Pronto", "sim" if meta["pronto"] else "não (esqueleto)")
    table.add_row("Mensagem", meta["mensagem"][:80])
    table.add_row("Seções 1º", f"{meta['secoes_1t']:,}")
    table.add_row("Seções 2º", f"{meta['secoes_2t']:,}")
    table.add_row("% ≥17h 1º", str(meta["horario_1t_pct_apos_17h"]))
    table.add_row("% ≥17h 2º", str(meta["horario_2t_pct_apos_17h"]))
    console.print(table)


def consolidate_compare(
    ufs: list[str], turno_a: int, turno_b: int
) -> Path | None:
    frames: list[pd.DataFrame] = []
    for uf in ufs:
        p = REPORTS_DIR / f"comparar_turnos_summary_{uf.upper()}_{turno_a}t_{turno_b}t.csv"
        if p.exists():
            frames.append(pd.read_csv(p))
    if not frames:
        return None
    out = REPORTS_DIR / f"comparar_turnos_summary_MULTI_{turno_a}t_{turno_b}t.csv"
    pd.concat(frames, ignore_index=True).to_csv(out, index=False)
    return out


def run_comparar_turnos(
    ufs: list[str], turno_a: int = 1, turno_b: int = 2
) -> list[Path]:
    outputs: list[Path] = []
    done: list[str] = []
    for i, uf in enumerate(ufs, start=1):
        uf = uf.upper()
        console.print(f"\n[bold][{i}/{len(ufs)}] Comparar turnos {uf}[/bold]")
        df, meta = build_compare(uf, turno_a, turno_b)
        print_compare_meta(meta)
        md, pq, csv = write_compare_report(df, meta, uf, turno_a, turno_b)
        console.print(f"[green]Relatório:[/green] {md}")
        outputs.extend([md, pq, csv])
        done.append(uf)
    if len(done) > 1:
        multi = consolidate_compare(done, turno_a, turno_b)
        if multi:
            console.print(f"\n[green]Resumo multi-UF:[/green] {multi}")
            outputs.append(multi)
    return outputs
