"""CLI urna-logs."""

from __future__ import annotations

from typing import Optional

import typer
from rich.console import Console

from urna_logs import __version__
from urna_logs.catalog import build_catalog, print_catalog_summary, save_catalog
from urna_logs.config import UFS, ensure_dirs
from urna_logs.download import download_many, extract_logjez, list_zip_members
from urna_logs.metrics import compute_metrics, print_summary, save_metrics, summarize
from urna_logs.viability import run_viability

app = typer.Typer(help="Validação de logs das urnas — Eleições 2026", no_args_is_help=True)
console = Console()


def _parse_ufs(ufs: Optional[str]) -> list[str]:
    if not ufs:
        return ["AC"]
    if ufs.strip().upper() == "ALL":
        return list(UFS)
    return [u.strip().upper() for u in ufs.replace(",", " ").split() if u.strip()]


@app.callback()
def main() -> None:
    ensure_dirs()


@app.command()
def version() -> None:
    """Mostra a versão."""
    console.print(__version__)


@app.command("download")
def download_cmd(
    ufs: Optional[str] = typer.Option("AC", "--ufs", help="UFs separadas por espaço/vírgula, ou ALL"),
    turno: int = typer.Option(1, "--turno", min=1, max=2),
    force: bool = typer.Option(False, "--force", help="Baixa de novo mesmo se completo"),
    extract: bool = typer.Option(False, "--extract", help="Extrai .logjez após o download"),
) -> None:
    """Baixa ZIPs do TSE com retomada incremental (HTTP Range)."""
    uf_list = _parse_ufs(ufs)
    paths = download_many(uf_list, turno, force=force)
    if extract:
        for path, uf in zip(paths, uf_list):
            extract_logjez(path, uf, turno, only_logs=True)


@app.command("inspect")
def inspect_cmd(
    ufs: Optional[str] = typer.Option("AC", "--ufs"),
    turno: int = typer.Option(1, "--turno", min=1, max=2),
    limit: int = typer.Option(40, "--limit"),
) -> None:
    """Lista extensões/arquivos dentro do ZIP."""
    from urna_logs.config import zip_path

    for uf in _parse_ufs(ufs):
        zpath = zip_path(uf, turno)
        if not zpath.exists():
            console.print(f"[red]ZIP ausente:[/red] {zpath}")
            continue
        names, total = list_zip_members(zpath, limit=limit)
        console.print(f"[bold]{zpath.name}[/bold] — {total:,} entradas (mostrando {len(names)})")
        for n in names:
            console.print(f"  {n}")


@app.command("catalog")
def catalog_cmd(
    ufs: Optional[str] = typer.Option("AC", "--ufs"),
    turno: int = typer.Option(1, "--turno", min=1, max=2),
) -> None:
    """Gera catálogo de mensagens e sinais de viabilidade."""
    for uf in _parse_ufs(ufs):
        result = build_catalog(uf, turno)
        out = save_catalog(result, uf, turno)
        print_catalog_summary(result)
        console.print(f"[green]Salvo:[/green] {out}")


@app.command("metrics")
def metrics_cmd(
    ufs: Optional[str] = typer.Option("AC", "--ufs"),
    turno: int = typer.Option(1, "--turno", min=1, max=2),
) -> None:
    """Calcula métricas de biometria e pós-17h."""
    for uf in _parse_ufs(ufs):
        df = compute_metrics(uf, turno)
        summary = summarize(df)
        detail, summary_path = save_metrics(df, summary, uf, turno)
        print_summary(summary, uf, turno)
        console.print(f"[green]Parquet:[/green] {detail}")
        console.print(f"[green]Summary:[/green] {summary_path}")


@app.command("viability")
def viability_cmd(
    ufs: Optional[str] = typer.Option("AC", "--ufs"),
    turno: int = typer.Option(1, "--turno", min=1, max=2),
) -> None:
    """Roda catálogo + métricas e grava relatório go/no-go."""
    for uf in _parse_ufs(ufs):
        report = run_viability(uf, turno)
        console.print(f"[green]Relatório:[/green] {report}")


if __name__ == "__main__":
    app()
