"""CLI urna-logs."""

from __future__ import annotations

from typing import Optional

import httpx
import typer
from rich.console import Console

from urna_logs import __version__
from urna_logs.audit import consolidate_audit_parquets, run_audit
from urna_logs.catalog import build_catalog, print_catalog_summary, save_catalog
from urna_logs.config import UFS, ensure_dirs
from urna_logs.download import download_many, extract_logjez, list_zip_members
from urna_logs.metrics import compute_metrics, print_summary, save_metrics, summarize
from urna_logs.comparar_turnos import run_comparar_turnos
from urna_logs.horario import run_horario
from urna_logs.oficial import run_cruzar_oficial
from urna_logs.report_geo import run_by_municipio
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
    console.print("[dim]Destino:[/dim] data/raw/ · se interromper, rode de novo para retomar")
    try:
        paths = download_many(uf_list, turno, force=force)
    except FileNotFoundError as exc:
        console.print(f"[red]Indisponível:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    if extract:
        for i, (path, uf) in enumerate(zip(paths, uf_list), start=1):
            console.print(f"\n[bold]Extraindo logs [{i}/{len(paths)}] {uf}[/bold]")
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


@app.command("audit")
def audit_cmd(
    ufs: Optional[str] = typer.Option("AC", "--ufs"),
    turno: int = typer.Option(1, "--turno", min=1, max=2),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Mostra cada urna com divergência durante o processamento"
    ),
) -> None:
    """Reconta votos de presidente (RDV) e compara com o BU."""
    uf_list = _parse_ufs(ufs)
    console.print(
        f"[bold]Auditoria[/bold] — presidente · {turno}º turno · "
        f"{len(uf_list)} UF(s): {', '.join(uf_list)}"
    )
    done: list[str] = []
    for i, uf in enumerate(uf_list, start=1):
        console.print(f"\n[bold][{i}/{len(uf_list)}] {uf}[/bold]")
        try:
            report, csv_path, secoes_pq, votos_pq = run_audit(uf, turno, verbose=verbose)
        except (FileNotFoundError, OSError, ValueError) as exc:
            console.print(f"[red]Pulando {uf}:[/red] {exc}")
            continue
        except Exception as exc:  # noqa: BLE001 — não abortar o lote inteiro
            console.print(f"[red]Erro em {uf}:[/red] {type(exc).__name__}: {exc}")
            continue
        done.append(uf)
        console.print(f"[green]Relatório:[/green] {report}")
        console.print(f"[green]CSV:[/green] {csv_path}")
        console.print(f"[green]Parquet (seções):[/green] {secoes_pq}")
        console.print(f"[green]Parquet (votos):[/green] {votos_pq}")
    if len(done) > 1:
        cons = consolidate_audit_parquets(done, turno)
        if cons:
            console.print(f"\n[green]Arquivo único (seções):[/green] {cons[0]}")
            console.print(f"[green]Arquivo único (votos):[/green] {cons[1]}")


@app.command("by-municipio")
def by_municipio_cmd(
    ufs: Optional[str] = typer.Option("AC", "--ufs"),
    turno: int = typer.Option(1, "--turno", min=1, max=2),
) -> None:
    """Totais por município (votos de presidente + % sem digital do BU)."""
    uf_list = _parse_ufs(ufs)
    try:
        run_by_municipio(uf_list, turno)
    except FileNotFoundError as exc:
        console.print(f"[red]Faltam dados:[/red] {exc}")
        raise typer.Exit(code=1) from exc


@app.command("cruzar-oficial")
def cruzar_oficial_cmd(
    ufs: Optional[str] = typer.Option("AC", "--ufs"),
    turno: int = typer.Option(1, "--turno", min=1, max=2),
    force_download: bool = typer.Option(
        False, "--force-download", help="Baixa de novo o ZIP nacional do TSE"
    ),
    force_rebuild: bool = typer.Option(
        False, "--force-rebuild", help="Reextrai o Parquet oficial da UF a partir do ZIP"
    ),
) -> None:
    """Cruza votos de presidente (BU da audit) com o CSV oficial por seção."""
    uf_list = _parse_ufs(ufs)
    console.print(
        f"[bold]Cruzamento oficial[/bold] — presidente · {turno}º turno · "
        f"{len(uf_list)} UF(s): {', '.join(uf_list)}"
    )
    try:
        run_cruzar_oficial(
            uf_list,
            turno,
            force_download=force_download,
            force_rebuild=force_rebuild,
        )
    except httpx.HTTPError as exc:
        console.print(f"[red]Falha no download oficial:[/red] {exc}")
        raise typer.Exit(code=1) from exc


@app.command("horario")
def horario_cmd(
    ufs: Optional[str] = typer.Option("AC", "--ufs"),
    turno: int = typer.Option(1, "--turno", min=1, max=2),
    detalhe: bool = typer.Option(
        False,
        "--detalhe",
        help="Parquet 1 linha/habilitação (lento). Padrão: só curva agregada.",
    ),
    force: bool = typer.Option(
        False, "--force", help="Refaz mesmo se já existir summary/CSV da UF"
    ),
    workers: int = typer.Option(
        0, "--workers", help="Processos paralelos no modo curva (0=auto)"
    ),
) -> None:
    """Curva de habilitações por hora (log) + % pós-17h."""
    uf_list = _parse_ufs(ufs)
    console.print(
        f"[bold]Horário[/bold] — {turno}º turno · "
        f"{'detalhe' if detalhe else 'curva'} · "
        f"{len(uf_list)} UF(s): {', '.join(uf_list)}"
    )
    run_horario(
        uf_list,
        turno,
        detalhe=detalhe,
        force=force,
        workers=workers or None,
    )


@app.command("comparar-turnos")
def comparar_turnos_cmd(
    ufs: Optional[str] = typer.Option("AC", "--ufs"),
    turno_a: int = typer.Option(1, "--turno-a", min=1, max=2),
    turno_b: int = typer.Option(2, "--turno-b", min=1, max=2),
) -> None:
    """Compara seções entre turnos (esqueleto se o 2º ainda não existir)."""
    uf_list = _parse_ufs(ufs)
    console.print(
        f"[bold]Comparar turnos[/bold] — {turno_a}º × {turno_b}º · "
        f"{len(uf_list)} UF(s): {', '.join(uf_list)}"
    )
    run_comparar_turnos(uf_list, turno_a, turno_b)


if __name__ == "__main__":
    app()
