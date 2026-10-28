"""
Validação go/no-go do algoritmo de fluxo ecológico (piloto → país).

Roda asserts de identidade, IPF⊂Duncan–Davis, taxas, estabilidade e resíduos.
Não prova preferência eleitoral — só sanidade do pipeline antes de escalar.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
from rich.console import Console
from rich.table import Table

from urna_logs.config import REPORTS_DIR, ensure_dirs
from urna_logs.fluxo_ecologico import (
    BOOTSTRAP_SEED,
    DESTINOS,
    ORIGENS,
    ORIGENS_FOCO,
    attach_ipf_flows,
    bootstrap_rates,
    compute_bounds_frame,
    duncan_davis_bounds,
    load_compare,
    predictive_residuals,
    _weighted_rates,
)

console = Console()

# Tolerâncias
TOL_MARGEM = 2.0  # votos (IPF vs margem; folga numérica)
TOL_BOUNDS = 2.0  # IPF pode ficar ligeiramente fora por arredondamento
TOL_RATE_SUM = 0.02  # |sum_d p(o→d) − 1|
TOL_RESID_REL = 0.35  # média |resid|/média destino (UF rates ≠ seção)
TOL_STABILITY = 1e-9
MIN_SECOES = 50
IDENTIDADE_MIN_PCT = 0.995  # fração mínima de seções com margens OK
# Se |Fa2−Fb2|/N > este valor, p(Elim→Fa) e p(Elim→Fb) não devem ser ~iguais
DEST_IMBALANCE = 0.05
RATE_SEP_MIN = 0.02


@dataclass
class Check:
    id: str
    ok: bool
    detail: str
    severity: str = "hard"  # hard → bloqueia go; soft → aviso


@dataclass
class UfValidation:
    uf: str
    go: bool
    checks: list[Check] = field(default_factory=list)
    n_secoes: int = 0

    def hard_failures(self) -> list[Check]:
        return [c for c in self.checks if not c.ok and c.severity == "hard"]

    def soft_failures(self) -> list[Check]:
        return [c for c in self.checks if not c.ok and c.severity == "soft"]


def _load_or_build(uf: str, turno_a: int, turno_b: int) -> tuple[pd.DataFrame, dict[str, float], pd.DataFrame] | None:
    """Retorna (bounds+ipf, rates, compare) ou None se faltar comparar."""
    compare = load_compare(uf, turno_a, turno_b)
    if compare is None or not (compare["status"] == "ambos").any():
        return None
    bounds = attach_ipf_flows(compute_bounds_frame(compare))
    rates = _weighted_rates(bounds)
    return bounds, rates, compare


def validate_uf(uf: str, turno_a: int = 1, turno_b: int = 2) -> UfValidation:
    uf = uf.upper()
    result = UfValidation(uf=uf, go=False)
    packed = _load_or_build(uf, turno_a, turno_b)
    if packed is None:
        result.checks.append(
            Check(
                "prereq_comparar",
                False,
                f"Falta comparar_turnos_{uf}_{turno_a}t_{turno_b}t.parquet com seções em ambos",
                "hard",
            )
        )
        return result

    bounds, rates, compare = packed
    n = len(bounds)
    result.n_secoes = n

    # --- 1. volume mínimo ---
    result.checks.append(
        Check(
            "min_secoes",
            n >= MIN_SECOES,
            f"{n} seções (mínimo {MIN_SECOES})",
            "hard",
        )
    )

    # --- 2. identidade contábil ---
    id_ok = int(bounds["identidade_ok"].sum()) if "identidade_ok" in bounds.columns else 0
    id_pct = id_ok / n if n else 0.0
    result.checks.append(
        Check(
            "identidade",
            id_pct >= IDENTIDADE_MIN_PCT,
            f"{id_ok}/{n} seções com margens coerentes ({100 * id_pct:.2f}%; "
            f"mín {100 * IDENTIDADE_MIN_PCT:.1f}%)",
            "hard",
        )
    )

    # --- 3. IPF fecha margens (após absorver Δ aptos em abst) ---
    row_err = []
    col_err = []
    for _, row in bounds.iterrows():
        origins = {o: float(row.get(f"o_{o}", 0) or 0) for o in ORIGENS}
        dests = {d: float(row.get(f"d_{d}", 0) or 0) for d in DESTINOS}
        so, sd = sum(origins.values()), sum(dests.values())
        if not np.isfinite(so) or not np.isfinite(sd):
            continue
        n_sec = max(so, sd)
        if so < n_sec - 1e-9:
            origins["abst"] += n_sec - so
        if sd < n_sec - 1e-9:
            dests["abst"] += n_sec - sd
        for o in ORIGENS:
            got = sum(float(row.get(f"{o}_to_{d}_ipf", 0) or 0) for d in DESTINOS)
            row_err.append(abs(got - origins[o]))
        for d in DESTINOS:
            got = sum(float(row.get(f"{o}_to_{d}_ipf", 0) or 0) for o in ORIGENS)
            col_err.append(abs(got - dests[d]))
    max_row = float(np.nanmax(row_err)) if row_err else 0.0
    max_col = float(np.nanmax(col_err)) if col_err else 0.0
    if not np.isfinite(max_row):
        max_row = float("inf")
    if not np.isfinite(max_col):
        max_col = float("inf")
    result.checks.append(
        Check(
            "ipf_margens",
            max_row <= TOL_MARGEM and max_col <= TOL_MARGEM,
            f"max |IPF−origem|={max_row:.3f} · max |IPF−destino|={max_col:.3f} "
            f"(tol {TOL_MARGEM})",
            "hard",
        )
    )

    # --- 4. IPF ⊆ Duncan–Davis nas *mesmas* margens ajustadas do IPF ---
    viol = 0
    checked = 0
    max_out = 0.0
    for _, row in bounds.iterrows():
        origins = {o: float(row.get(f"o_{o}", 0) or 0) for o in ORIGENS}
        dests = {d: float(row.get(f"d_{d}", 0) or 0) for d in DESTINOS}
        so, sd = sum(origins.values()), sum(dests.values())
        if not np.isfinite(so) or not np.isfinite(sd):
            continue
        n_sec = max(so, sd)
        if so < n_sec - 1e-9:
            origins["abst"] += n_sec - so
        if sd < n_sec - 1e-9:
            dests["abst"] += n_sec - sd
        for o in ORIGENS_FOCO:
            for d in DESTINOS:
                lo, hi = duncan_davis_bounds(origins[o], dests[d], n_sec)
                ipf = float(row.get(f"{o}_to_{d}_ipf", 0) or 0)
                checked += 1
                if ipf < lo - TOL_BOUNDS or ipf > hi + TOL_BOUNDS:
                    viol += 1
                    max_out = max(max_out, lo - ipf, ipf - hi)
    result.checks.append(
        Check(
            "ipf_dentro_bounds",
            viol == 0,
            f"{viol} violações em {checked} células (max fora={max_out:.3f}, tol={TOL_BOUNDS})",
            "hard",
        )
    )

    # --- 5. taxas em [0,1] e somam ~1 ---
    rate_ok = True
    rate_details = []
    for o in ORIGENS_FOCO:
        ps = [rates.get(f"p_{o}_to_{d}", float("nan")) for d in DESTINOS]
        if any(not np.isfinite(p) or p < -1e-9 or p > 1 + 1e-9 for p in ps):
            rate_ok = False
            rate_details.append(f"{o}: fora de [0,1]")
            continue
        s = float(np.nansum(ps))
        if abs(s - 1.0) > TOL_RATE_SUM:
            rate_ok = False
            rate_details.append(f"{o}: soma={s:.4f}")
    result.checks.append(
        Check(
            "taxas_validas",
            rate_ok,
            "; ".join(rate_details) if rate_details else "todas as origens-foco OK",
            "hard",
        )
    )

    # --- 6. não colapsar 50/50 se destinos desbalanceados ---
    fa2 = float(bounds["d_fa"].sum())
    fb2 = float(bounds["d_fb"].sum())
    n_tot = float(bounds["n_total"].sum()) or 1.0
    imb = abs(fa2 - fb2) / n_tot
    p_fa = rates.get("p_elim_to_fa", float("nan"))
    p_fb = rates.get("p_elim_to_fb", float("nan"))
    sep = abs(p_fa - p_fb) if np.isfinite(p_fa) and np.isfinite(p_fb) else 0.0
    collapse_ok = True
    collapse_detail = f"|Fa2−Fb2|/N={imb:.3f} · |pElimFa−pElimFb|={sep:.3f}"
    if imb >= DEST_IMBALANCE:
        collapse_ok = sep >= RATE_SEP_MIN
        if not collapse_ok:
            collapse_detail += " — taxas Elim quase iguais com destinos desbalanceados"
    result.checks.append(
        Check("sem_colapso_5050", collapse_ok, collapse_detail, "hard")
    )

    # --- 7. estabilidade (mesmo seed → mesmas taxas) ---
    rates2 = _weighted_rates(bounds)
    stable = all(
        abs(rates.get(k, 0) - rates2.get(k, 0)) <= TOL_STABILITY
        for k in rates
        if np.isfinite(rates.get(k, float("nan")))
    )
    # bootstrap determinístico
    boot1 = bootstrap_rates(bounds, n_boot=40, seed=BOOTSTRAP_SEED)
    boot2 = bootstrap_rates(bounds, n_boot=40, seed=BOOTSTRAP_SEED)
    boot_stable = boot1.equals(boot2) if len(boot1) == len(boot2) else False
    result.checks.append(
        Check(
            "estabilidade",
            stable and boot_stable,
            f"taxas IPF idênticas={stable} · bootstrap seed={boot_stable}",
            "hard",
        )
    )

    # --- 8. resíduo preditivo UF ---
    resid = predictive_residuals(bounds, rates)
    resid_ok = True
    resid_parts = []
    for d in ("fa", "fb", "abst"):
        obs = float(bounds[f"d_{d}"].sum())
        if obs <= 0:
            continue
        mean_abs = float(resid[f"resid_{d}"].abs().mean())
        rel = mean_abs / (obs / n) if n else 999.0
        # mean_abs is mean over sections; compare to mean section dest
        mean_dest = obs / n
        rel = mean_abs / mean_dest if mean_dest > 0 else 0.0
        resid_parts.append(f"{d}:{rel:.3f}")
        if rel > TOL_RESID_REL:
            resid_ok = False
    result.checks.append(
        Check(
            "residuo_preditivo",
            resid_ok,
            f"mean|resid|/mean(dest) → {', '.join(resid_parts)} (tol {TOL_RESID_REL})",
            "soft",  # soft: IPF UF rates won't perfectly fit every section
        )
    )

    # --- 9. compatibilidade agregada: taxa × massa ≈ destino (só foco → parcial) ---
    # Verifica que Elim*p_elim_to_fa + ... não explode vs Fa2
    elim = float(bounds["o_elim"].sum())
    pred_fa_from_elim = elim * float(p_fa) if np.isfinite(p_fa) else 0.0
    compat = pred_fa_from_elim <= fa2 + TOL_MARGEM
    result.checks.append(
        Check(
            "compat_elim_fa",
            compat,
            f"Elim×p(Elim→Fa)={pred_fa_from_elim:,.1f} ≤ Fa2={fa2:,.1f}",
            "hard",
        )
    )

    # --- 10. artefatos gravados (soft se só validar em memória) ---
    tag = f"{uf}_{turno_a}t_{turno_b}t"
    arts = [
        REPORTS_DIR / f"fluxo_bounds_{tag}.parquet",
        REPORTS_DIR / f"fluxo_ecologico_{tag}.md",
        REPORTS_DIR / f"fluxo_ecologico_summary_{tag}.csv",
    ]
    missing = [p.name for p in arts if not p.exists()]
    result.checks.append(
        Check(
            "artefatos",
            len(missing) == 0,
            "OK" if not missing else f"faltam: {', '.join(missing)} — rode fluxo-ecologico",
            "soft",
        )
    )

    # --- 11. cruzar oficial 2t (soft) ---
    cruz = REPORTS_DIR / f"cruzar_oficial_summary_{uf}_{turno_b}t.csv"
    if cruz.exists():
        row = pd.read_csv(cruz).iloc[0]
        div = int(row.get("secoes_divergentes", 0) or 0)
        result.checks.append(
            Check(
                "cruzar_oficial_2t",
                div == 0,
                f"seções divergentes BU×oficial={div}",
                "soft",
            )
        )
    else:
        result.checks.append(
            Check(
                "cruzar_oficial_2t",
                False,
                "summary cruzar 2t ausente",
                "soft",
            )
        )

    result.go = len(result.hard_failures()) == 0
    return result


def write_validation_report(
    results: list[UfValidation], turno_a: int, turno_b: int
) -> tuple[Path, Path]:
    ensure_dirs()
    ufs = [r.uf for r in results]
    tag = (
        f"MULTI_{turno_a}t_{turno_b}t"
        if len(ufs) != 1
        else f"{ufs[0]}_{turno_a}t_{turno_b}t"
    )
    md = REPORTS_DIR / f"validar_fluxo_{tag}.md"
    csv = REPORTS_DIR / f"validar_fluxo_{tag}.csv"

    all_go = all(r.go for r in results)
    lines = [
        f"# Validação fluxo ecológico — {turno_a}º→{turno_b}º",
        "",
        f"Verdict global: **{'GO' if all_go else 'NO-GO'}** "
        f"({sum(r.go for r in results)}/{len(results)} UFs passaram nos checks hard)",
        "",
        "Objetivo: sanidade do algoritmo no piloto antes de escalar ao país. "
        "Não valida preferência eleitoral nem ausência de anomalia política.",
        "",
        "## Por UF",
        "",
    ]
    rows_csv = []
    for r in results:
        lines.append(f"### {r.uf} — {'GO' if r.go else 'NO-GO'} ({r.n_secoes} seções)")
        lines.append("")
        lines.append("| Check | Sev | OK | Detalhe |")
        lines.append("|---|---|:---:|---|")
        for c in r.checks:
            mark = "sim" if c.ok else "**não**"
            lines.append(f"| `{c.id}` | {c.severity} | {mark} | {c.detail} |")
            rows_csv.append(
                {
                    "uf": r.uf,
                    "go": r.go,
                    "n_secoes": r.n_secoes,
                    "check": c.id,
                    "severity": c.severity,
                    "ok": c.ok,
                    "detail": c.detail,
                }
            )
        lines.append("")

    lines += [
        "## Critérios hard (bloqueiam GO)",
        "",
        f"- Mínimo {MIN_SECOES} seções em ambos os turnos",
        f"- Identidade das margens em ≥{100 * IDENTIDADE_MIN_PCT:.1f}% das seções",
        f"- IPF fecha origens/destinos (tol {TOL_MARGEM}; Δ aptos absorvido em abst)",
        f"- IPF cabe nos bounds Duncan–Davis (tol {TOL_BOUNDS})",
        f"- Taxas ∈ [0,1] e somam ~1 (tol {TOL_RATE_SUM})",
        "- Sem colapso 50/50 artificial quando destinos 2º são desbalanceados",
        "- Estabilidade determinística (mesmo input → mesmo output)",
        "- Elim×p(Elim→Fa) ≤ Fa2 agregado",
        "",
        "## Soft (aviso, não bloqueia)",
        "",
        f"- Resíduo preditivo médio relativo (tol {TOL_RESID_REL}) — taxas UF não "
        "reproduzem cada seção",
        "- Artefatos `fluxo_*` gravados",
        "- Cruzar oficial 2º sem divergências",
        "",
        "## Próximo passo se GO",
        "",
        "1. Regravar `fluxo-ecologico` no piloto (IPF atualizado) se os Parquets forem antigos",
        "2. Validar 1–2 UFs médias (`RO` / `SE`) após `audit --turno 2`",
        "3. Só então `fluxo-ecologico --ufs ALL` (e comparar-turnos nacional)",
        "",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")
    pd.DataFrame(rows_csv).to_csv(csv, index=False)
    return md, csv


def print_validation(results: list[UfValidation]) -> None:
    table = Table(title="Validar fluxo")
    table.add_column("UF")
    table.add_column("Verdict")
    table.add_column("Seções", justify="right")
    table.add_column("Hard fail", justify="right")
    table.add_column("Soft fail", justify="right")
    for r in results:
        table.add_row(
            r.uf,
            "[green]GO[/green]" if r.go else "[red]NO-GO[/red]",
            f"{r.n_secoes:,}",
            str(len(r.hard_failures())),
            str(len(r.soft_failures())),
        )
    console.print(table)


def run_validar_fluxo(
    ufs: list[str], turno_a: int = 1, turno_b: int = 2
) -> tuple[list[Path], bool]:
    results: list[UfValidation] = []
    for i, uf in enumerate(ufs, start=1):
        console.print(f"\n[bold][{i}/{len(ufs)}] Validar fluxo {uf.upper()}[/bold]")
        r = validate_uf(uf, turno_a, turno_b)
        results.append(r)
        for c in r.hard_failures():
            console.print(f"  [red]FAIL hard[/red] {c.id}: {c.detail}")
        for c in r.soft_failures():
            console.print(f"  [yellow]WARN soft[/yellow] {c.id}: {c.detail}")
        if r.go and not r.soft_failures():
            console.print("  [green]todos os checks OK[/green]")
        elif r.go:
            console.print("  [green]GO[/green] (com avisos soft)")

    print_validation(results)
    md, csv = write_validation_report(results, turno_a, turno_b)
    all_go = all(r.go for r in results)
    console.print(
        f"\n[bold]{'[green]GO[/green]' if all_go else '[red]NO-GO[/red]'}[/bold] · {md}"
    )
    return [md, csv], all_go
