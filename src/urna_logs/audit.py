"""Auditoria independente: recontagem RDV × BU (cargo presidente)."""

from __future__ import annotations

import zipfile
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn, TimeElapsedColumn
from rich.table import Table

from urna_logs.bu_rdv import TotaisPresidente, parse_bu_bytes, parse_rdv_bytes
from urna_logs.config import REPORTS_DIR, ensure_dirs, zip_path

console = Console()


@dataclass
class UrnaAudit:
    stem: str
    secao_key: str
    municipio: int
    zona: int
    local: int
    secao: int
    ok: bool
    bu_total: int | None = None
    rdv_total: int | None = None
    bu_comparecimento: int | None = None
    aptos: int | None = None
    mismatches: list[str] = field(default_factory=list)
    bu_votos: dict[str, int] = field(default_factory=dict)
    rdv_votos: dict[str, int] = field(default_factory=dict)
    error: str | None = None
    sem_biometria: int | None = None
    bio: int | None = None
    biografia: int | None = None


def _votos_key(tipo: str, numero: str | None) -> str:
    return f"{tipo}:{numero if numero is not None else '-'}"


def _flat_votos(t: TotaisPresidente) -> dict[str, int]:
    return {_votos_key(tipo, num): int(qtd) for (tipo, num), qtd in t.votos.items()}


def compare_presidente(
    bu: TotaisPresidente | None,
    rdv: TotaisPresidente | None,
    *,
    stem: str,
) -> UrnaAudit:
    if bu is None and rdv is None:
        return UrnaAudit(
            stem=stem,
            secao_key="?",
            municipio=0,
            zona=0,
            local=0,
            secao=0,
            ok=False,
            error="BU e RDV sem cargo presidente",
        )
    base = bu or rdv
    assert base is not None
    s = base.secao
    audit = UrnaAudit(
        stem=stem,
        secao_key=s.key(),
        municipio=s.municipio,
        zona=s.zona,
        local=s.local,
        secao=s.secao,
        ok=True,
    )
    if bu is None:
        audit.ok = False
        audit.error = "BU ausente ou sem presidente"
        audit.rdv_total = rdv.total if rdv else None
        if rdv is not None:
            audit.rdv_votos = _flat_votos(rdv)
        return audit

    audit.bu_total = bu.total
    audit.bu_comparecimento = bu.comparecimento
    audit.aptos = bu.aptos
    audit.sem_biometria = bu.sem_biometria
    audit.bio = bu.bio
    audit.biografia = bu.biografia
    audit.bu_votos = _flat_votos(bu)

    if rdv is None:
        audit.ok = False
        audit.error = "RDV ausente ou sem presidente"
        return audit

    audit.rdv_total = rdv.total
    audit.rdv_votos = _flat_votos(rdv)

    mismatches: list[str] = []
    if bu.total != rdv.total:
        mismatches.append(f"total BU={bu.total} RDV={rdv.total}")
    if bu.comparecimento is not None and bu.comparecimento != rdv.total:
        mismatches.append(
            f"comparecimento BU={bu.comparecimento} ≠ RDV={rdv.total}"
        )

    keys = set(bu.votos) | set(rdv.votos)
    for key in sorted(keys, key=lambda k: (k[0], k[1] or "")):
        b = bu.votos.get(key, 0)
        r = rdv.votos.get(key, 0)
        if b != r:
            mismatches.append(f"{_votos_key(*key)} BU={b} RDV={r}")

    if bu.secao.key() != rdv.secao.key():
        mismatches.append(f"seção BU={bu.secao.key()} RDV={rdv.secao.key()}")

    audit.mismatches = mismatches
    audit.ok = not mismatches
    return audit


def _index_zip_pairs(zf: zipfile.ZipFile) -> dict[str, dict[str, str]]:
    """stem -> {bu: name, rdv: name}."""
    pairs: dict[str, dict[str, str]] = {}
    for name in zf.namelist():
        base = Path(name).name.lower()
        if base.endswith("-imgbu.dat") or base.endswith("-imgbusa.dat"):
            continue
        if base.endswith("-bu.dat") or base.endswith("-busa.dat"):
            stem = base[: base.rfind("-")]
            pairs.setdefault(stem, {})["bu"] = name
        elif base.endswith("-rdv.dat") or base.endswith("-rdvred.dat"):
            stem = base[: base.rfind("-")]
            pairs.setdefault(stem, {})["rdv"] = name
    return pairs


def audit_zip(zpath: Path, *, verbose: bool = False) -> list[UrnaAudit]:
    results: list[UrnaAudit] = []
    console.print(f"[cyan]Abrindo ZIP[/cyan] {zpath.name} ({zpath.stat().st_size / 1e6:.1f} MB)…")
    with zipfile.ZipFile(zpath) as zf:
        console.print("[cyan]Indexando[/cyan] pares BU/RDV…")
        pairs = _index_zip_pairs(zf)
        stems = sorted(pairs)
        console.print(f"Urnas encontradas: [bold]{len(stems):,}[/bold]")
        ok_n = fail_n = 0
        progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("· OK {task.fields[ok]} · fail {task.fields[fail]}"),
            TimeElapsedColumn(),
            console=console,
            transient=False,
        )
        with progress:
            task = progress.add_task("presidente", total=len(stems), ok=0, fail=0)
            for stem in stems:
                files = pairs[stem]
                bu_name = files.get("bu")
                rdv_name = files.get("rdv")
                try:
                    bu_tot = (
                        parse_bu_bytes(zf.read(bu_name), source=bu_name)
                        if bu_name
                        else None
                    )
                    rdv_tot = (
                        parse_rdv_bytes(zf.read(rdv_name), source=rdv_name)
                        if rdv_name
                        else None
                    )
                    item = compare_presidente(bu_tot, rdv_tot, stem=stem)
                except Exception as exc:  # noqa: BLE001 — registrar e seguir
                    item = UrnaAudit(
                        stem=stem,
                        secao_key="?",
                        municipio=0,
                        zona=0,
                        local=0,
                        secao=0,
                        ok=False,
                        error=f"{type(exc).__name__}: {exc}",
                    )
                results.append(item)
                if item.ok:
                    ok_n += 1
                else:
                    fail_n += 1
                    if verbose:
                        detail = item.error or "; ".join(item.mismatches)
                        progress.console.print(
                            f"  [red]divergência[/red] {stem}: {detail}"
                        )
                progress.update(task, advance=1, ok=ok_n, fail=fail_n)
    return results


def join_key(uf: str, municipio: int, zona: int, secao: int) -> str:
    """Chave estável entre 1º e 2º turno (sem local — pode mudar em contingência)."""
    return f"{uf.upper()}:{municipio:05d}:{zona:04d}:{secao:04d}"


def _parse_voto_key(key: str) -> tuple[str, str | None]:
    tipo, _, numero = key.partition(":")
    if numero == "-" or numero == "":
        return tipo, None
    return tipo, numero


def results_to_frame(results: list[UrnaAudit], uf: str, turno: int) -> pd.DataFrame:
    """Uma linha por seção/urna — base para cruzar 1º×2º turno e somar totais."""
    uf = uf.upper()
    rows = []
    for r in results:
        aptos = r.aptos
        comp = r.bu_comparecimento
        abst = None
        if aptos is not None and comp is not None:
            abst = int(aptos) - int(comp)
        rows.append(
            {
                "uf": uf,
                "turno": turno,
                "join_key": join_key(uf, r.municipio, r.zona, r.secao),
                "stem": r.stem,
                "secao_key": r.secao_key,
                "municipio": r.municipio,
                "zona": r.zona,
                "local": r.local,
                "secao": r.secao,
                "ok": r.ok,
                "bu_total": r.bu_total,
                "rdv_total": r.rdv_total,
                "bu_comparecimento": comp,
                "aptos": aptos,
                "abstencao": abst,
                "pct_abstencao": (
                    round(100 * abst / aptos, 4) if aptos and abst is not None else None
                ),
                "sem_biometria": r.sem_biometria,
                "bio": r.bio,
                "biografia": r.biografia,
                "n_mismatches": len(r.mismatches),
                "mismatches": "; ".join(r.mismatches) if r.mismatches else "",
                "error": r.error or "",
            }
        )
    return pd.DataFrame(rows)


def results_to_votos_frame(results: list[UrnaAudit], uf: str, turno: int) -> pd.DataFrame:
    """Uma linha por (seção, tipo, número do candidato) — base para comparar turnos."""
    uf = uf.upper()
    rows: list[dict] = []
    for r in results:
        # Inclui BU mesmo se RDV faltou — necessário para cruzar com o CSV oficial
        if not r.bu_votos and not r.rdv_votos:
            continue
        jk = join_key(uf, r.municipio, r.zona, r.secao)
        keys = set(r.bu_votos) | set(r.rdv_votos)
        for key in keys:
            tipo, numero = _parse_voto_key(key)
            rows.append(
                {
                    "uf": uf,
                    "turno": turno,
                    "join_key": jk,
                    "municipio": r.municipio,
                    "zona": r.zona,
                    "local": r.local,
                    "secao": r.secao,
                    "tipo": tipo,
                    "numero": numero,
                    "votos_bu": int(r.bu_votos.get(key, 0)),
                    "votos_rdv": int(r.rdv_votos.get(key, 0)),
                }
            )
    if not rows:
        return pd.DataFrame(
            columns=[
                "uf",
                "turno",
                "join_key",
                "municipio",
                "zona",
                "local",
                "secao",
                "tipo",
                "numero",
                "votos_bu",
                "votos_rdv",
            ]
        )
    return pd.DataFrame(rows)


def aggregate_presidente(results: list[UrnaAudit]) -> Counter:
    """Soma votos BU (fonte oficial por urna) quando ok; ignora falhas."""
    agg: Counter = Counter()
    for r in results:
        if not r.ok:
            continue
        for k, v in r.bu_votos.items():
            agg[k] += v
    return agg


def write_audit_report(
    results: list[UrnaAudit], uf: str, turno: int, zpath: Path
) -> Path:
    ensure_dirs()
    path = REPORTS_DIR / f"audit_presidente_{uf.upper()}_{turno}t.md"
    ok = sum(1 for r in results if r.ok)
    fail = len(results) - ok
    agg = aggregate_presidente(results)
    total_votos = sum(agg.values())

    lines = [
        f"# Auditoria presidente — {uf.upper()} {turno}º turno",
        "",
        f"ZIP: `{zpath}`",
        f"Urnas auditadas: **{len(results):,}** · OK: **{ok:,}** · divergentes/erro: **{fail:,}**",
        "",
        "## Escopo",
        "",
        "- Cargo: **presidente** apenas",
        "- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)",
        "",
        "## Totais agregados (BU das urnas OK)",
        "",
        f"Votos contabilizados: **{total_votos:,}**",
        "",
        "| Tipo:número | Votos |",
        "|---|---:|",
    ]
    for k, v in sorted(agg.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"| `{k}` | {v:,} |")

    fails = [r for r in results if not r.ok]
    lines += ["", "## Divergências / erros", ""]
    if not fails:
        lines.append("Nenhuma divergência encontrada.")
    else:
        lines.append(f"{len(fails)} urna(s):")
        lines.append("")
        for r in fails[:50]:
            detail = r.error or "; ".join(r.mismatches)
            lines.append(f"- `{r.stem}` seção `{r.secao_key}`: {detail}")
        if len(fails) > 50:
            lines.append(f"- … e mais {len(fails) - 50}")

    lines += [
        "",
        "## Método",
        "",
        "- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)",
        "- RDV: cada `Voto` do cargo presidente é contado",
        "- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU",
        "- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def print_audit_summary(results: list[UrnaAudit], uf: str, turno: int) -> None:
    ok = sum(1 for r in results if r.ok)
    fail = len(results) - ok
    agg = aggregate_presidente(results)

    console.print(f"\n[bold]Auditoria presidente — {uf.upper()} {turno}º turno[/bold]")
    table = Table()
    table.add_column("Métrica")
    table.add_column("Valor", justify="right")
    table.add_row("Urnas", f"{len(results):,}")
    table.add_row("OK (RDV ≡ BU)", f"{ok:,}")
    table.add_row("Divergentes/erro", f"{fail:,}")
    table.add_row("Votos agregados (BU OK)", f"{sum(agg.values()):,}")
    console.print(table)

    top = Table(title="Presidente — totais (BU OK)")
    top.add_column("Tipo:número")
    top.add_column("Votos", justify="right")
    for k, v in sorted(agg.items(), key=lambda kv: (-kv[1], kv[0]))[:20]:
        top.add_row(k, f"{v:,}")
    console.print(top)

    fails = [r for r in results if not r.ok]
    if fails:
        ft = Table(title="Problemas (até 15)")
        ft.add_column("Stem")
        ft.add_column("Seção")
        ft.add_column("Detalhe")
        for r in fails[:15]:
            ft.add_row(r.stem, r.secao_key, (r.error or "; ".join(r.mismatches))[:80])
        console.print(ft)


def consolidate_audit_parquets(ufs: list[str], turno: int) -> tuple[Path, Path] | None:
    """Junta os Parquets de várias UFs num arquivo só do turno."""
    ensure_dirs()
    secoes_frames: list[pd.DataFrame] = []
    votos_frames: list[pd.DataFrame] = []
    for uf in ufs:
        uf = uf.upper()
        sp = REPORTS_DIR / f"audit_presidente_{uf}_{turno}t.parquet"
        vp = REPORTS_DIR / f"audit_presidente_votos_{uf}_{turno}t.parquet"
        if sp.exists():
            secoes_frames.append(pd.read_parquet(sp))
        if vp.exists():
            votos_frames.append(pd.read_parquet(vp))
    if not secoes_frames:
        return None
    secoes_out = REPORTS_DIR / f"audit_presidente_MULTI_{turno}t.parquet"
    votos_out = REPORTS_DIR / f"audit_presidente_votos_MULTI_{turno}t.parquet"
    pd.concat(secoes_frames, ignore_index=True).to_parquet(secoes_out, index=False)
    if votos_frames:
        pd.concat(votos_frames, ignore_index=True).to_parquet(votos_out, index=False)
    return secoes_out, votos_out


def run_audit(
    uf: str, turno: int, *, verbose: bool = False
) -> tuple[Path, Path, Path, Path]:
    ensure_dirs()
    uf = uf.upper()
    zpath = zip_path(uf, turno)
    if not zpath.exists():
        raise FileNotFoundError(f"ZIP não encontrado: {zpath}. Rode o download antes.")

    console.print(
        f"[bold]Auditoria presidente[/bold] — {uf} {turno}º turno → {zpath.name}"
    )
    results = audit_zip(zpath, verbose=verbose)
    console.print("[cyan]Gravando[/cyan] CSV e Parquets (seções e votos)…")
    df = results_to_frame(results, uf, turno)
    votos = results_to_votos_frame(results, uf, turno)
    csv_path = REPORTS_DIR / f"audit_presidente_{uf}_{turno}t.csv"
    secoes_pq = REPORTS_DIR / f"audit_presidente_{uf}_{turno}t.parquet"
    votos_pq = REPORTS_DIR / f"audit_presidente_votos_{uf}_{turno}t.parquet"
    df.to_csv(csv_path, index=False)
    df.to_parquet(secoes_pq, index=False)
    votos.to_parquet(votos_pq, index=False)
    console.print(
        f"  seções={len(df):,} · linhas de voto={len(votos):,} · "
        f"join_key pronta para cruzar 1º e 2º turno"
    )
    report = write_audit_report(results, uf, turno, zpath)
    print_audit_summary(results, uf, turno)
    return report, csv_path, secoes_pq, votos_pq
