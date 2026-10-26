"""Métricas: totais, biometria, pós-17h."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.table import Table

from urna_logs.config import REPORTS_DIR, ensure_dirs, zip_path
from urna_logs.parse_log import classify_habilitacoes, iter_events_from_zip

console = Console()


def compute_metrics(uf: str, turno: int) -> pd.DataFrame:
    ensure_dirs()
    zpath = zip_path(uf, turno)
    if not zpath.exists():
        raise FileNotFoundError(f"ZIP não encontrado: {zpath}")

    uf = uf.upper()
    rows = []
    for hab in classify_habilitacoes(iter_events_from_zip(zpath), uf=uf):
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
    if not rows:
        return pd.DataFrame(
            columns=["uf", "turno", "id_ue", "source", "dt", "after_17h", "tipo", "mensagem_tipo"]
        )
    return pd.DataFrame(rows)


def summarize(df: pd.DataFrame) -> dict:
    """
    Agrega métricas do **log**.

    - `pct_sem_digital_log` = sem_biometria + manual_falha
      (proxy; no BU o canônico é biografia + sem_biometria → `pct_sem_digital`)
    - `pct_apos_17h` = critério oficial BRT (já marcado em `after_17h` na classificação)
    """
    if df.empty:
        return {
            "total_habilitacoes": 0,
            "por_tipo": {},
            "pct_sem_digital_log": None,
            "pct_sem_digital": None,  # alias legado = log
            "pct_apos_17h": None,
            "apos_17h_por_tipo": {},
        }
    total = len(df)
    por_tipo = df["tipo"].value_counts().to_dict()
    # Proxy de log (≠ BU: biografia + sem_biometria)
    sem_digital_log = int(
        por_tipo.get("sem_biometria", 0) + por_tipo.get("manual_falha", 0)
    )
    apos = int(df["after_17h"].sum())
    apos_por_tipo = (
        df[df["after_17h"]].groupby("tipo").size().to_dict() if apos else {}
    )
    pct_log = round(100 * sem_digital_log / total, 4) if total else None
    return {
        "total_habilitacoes": total,
        "por_tipo": {str(k): int(v) for k, v in por_tipo.items()},
        "pct_sem_digital_log": pct_log,
        "pct_sem_digital": pct_log,  # compat: nome antigo = métrica do log
        "sem_digital_log_count": sem_digital_log,
        "sem_digital_count": sem_digital_log,
        "pct_apos_17h": round(100 * apos / total, 4) if total else None,
        "apos_17h_count": apos,
        "apos_17h_por_tipo": {str(k): int(v) for k, v in apos_por_tipo.items()},
        "urnas": int(df["id_ue"].nunique()),
    }


def save_metrics(df: pd.DataFrame, summary: dict, uf: str, turno: int) -> tuple[Path, Path]:
    ensure_dirs()
    detail = REPORTS_DIR / f"metrics_{uf.upper()}_{turno}t.parquet"
    summary_path = REPORTS_DIR / f"metrics_summary_{uf.upper()}_{turno}t.csv"
    df.to_parquet(detail, index=False)
    # summary as single-row csv + por_tipo expanded
    flat = {
        "uf": uf.upper(),
        "turno": turno,
        "total_habilitacoes": summary["total_habilitacoes"],
        "urnas": summary.get("urnas", 0),
        "pct_sem_digital_log": summary.get(
            "pct_sem_digital_log", summary.get("pct_sem_digital")
        ),
        "pct_sem_digital": summary.get("pct_sem_digital"),  # alias legado
        "sem_digital_log_count": summary.get(
            "sem_digital_log_count", summary.get("sem_digital_count", 0)
        ),
        "sem_digital_count": summary.get("sem_digital_count", 0),
        "pct_apos_17h": summary["pct_apos_17h"],
        "apos_17h_count": summary.get("apos_17h_count", 0),
    }
    for tipo, count in summary.get("por_tipo", {}).items():
        flat[f"tipo_{tipo}"] = count
    pd.DataFrame([flat]).to_csv(summary_path, index=False)
    return detail, summary_path


def print_summary(summary: dict, uf: str, turno: int) -> None:
    console.print(f"\n[bold]Métricas {uf.upper()} {turno}º turno[/bold]")
    table = Table()
    table.add_column("Métrica")
    table.add_column("Valor", justify="right")
    table.add_row("Habilitações", f"{summary['total_habilitacoes']:,}")
    table.add_row("Urnas", f"{summary.get('urnas', 0):,}")
    pct_log = summary.get("pct_sem_digital_log", summary.get("pct_sem_digital"))
    table.add_row(
        "% sem digital (log)",
        f"{pct_log}%" if pct_log is not None else "—",
    )
    table.add_row(
        "% após 17h (BRT)",
        f"{summary['pct_apos_17h']}%" if summary["pct_apos_17h"] is not None else "—",
    )
    console.print(table)

    tipos = Table(title="Por tipo de habilitação")
    tipos.add_column("Tipo")
    tipos.add_column("Count", justify="right")
    for k, v in summary.get("por_tipo", {}).items():
        tipos.add_row(k, f"{v:,}")
    console.print(tipos)
