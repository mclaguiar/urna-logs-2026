"""
Inferência ecológica de fluxo 1º→2º por seção.

Camada A: limites Duncan–Davis (factíveis sem modelo).
Camada B: taxas médias UF via ponto médio ponderado + bootstrap de seções.
Camada C: resíduos preditivos e correlatos (abstenção seletiva).

Não recupera voto individual — só conjuntos factíveis e taxas agregadas com IC.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from rich.console import Console
from rich.table import Table

from urna_logs.config import REPORTS_DIR, ensure_dirs

console = Console()

ORIGENS = ("fa", "fb", "elim", "branco", "nulo", "abst")
DESTINOS = ("fa", "fb", "branco", "nulo", "abst")

# Origens de interesse para relatório (além de fa/fb que “permanecem”)
ORIGENS_FOCO = ("elim", "branco", "nulo", "abst")

# Intervalo estreito: (max-min)/origem ≤ este valor
NARROW_WIDTH = 0.25

BOOTSTRAP_N = 400
BOOTSTRAP_SEED = 20261028


def duncan_davis_bounds(n_origin: float, n_dest: float, n_total: float) -> tuple[float, float]:
    """
    Limites factíveis do fluxo origem→destino numa tabela 2×2 implícita.

    min = max(0, n_o + n_d − N)
    max = min(n_o, n_d)
    """
    n_o = float(max(0.0, n_origin))
    n_d = float(max(0.0, n_dest))
    n = float(max(n_total, n_o, n_d, 1e-12))
    lo = max(0.0, n_o + n_d - n)
    hi = min(n_o, n_d)
    if hi < lo:
        # inconsistência numérica leve — colapsa no ponto médio factível
        mid = max(0.0, min(n_o, n_d, (lo + hi) / 2 if hi >= 0 else 0.0))
        return mid, mid
    return lo, hi


def build_margins(row: pd.Series) -> tuple[dict[str, float], dict[str, float], float, float]:
    """
    Monta margens origem (1º) e destino (2º).

    Se aptos diferem, preenche com origem `aptos_in` ou destino `aptos_out`
    para que ambas somem N = max(aptos_1t, aptos_2t).
    """
    apt1 = float(pd.to_numeric(row.get("aptos_1t"), errors="coerce") or 0)
    apt2 = float(pd.to_numeric(row.get("aptos_2t"), errors="coerce") or 0)
    # fallback: comparecimento + abstenção
    if apt1 <= 0:
        apt1 = float(row.get("comparecimento_1t") or 0) + float(row.get("abstencao_1t") or 0)
    if apt2 <= 0:
        apt2 = float(row.get("comparecimento_2t") or 0) + float(row.get("abstencao_2t") or 0)

    origins = {
        "fa": float(row.get("votos_fa_1t") or 0),
        "fb": float(row.get("votos_fb_1t") or 0),
        "elim": float(row.get("votos_eliminados_1t") or 0),
        "branco": float(row.get("branco_1t") or 0),
        "nulo": float(row.get("nulo_1t") or 0),
        "abst": float(row.get("abstencao_1t") or 0),
    }
    dests = {
        "fa": float(row.get("votos_fa_2t") or 0),
        "fb": float(row.get("votos_fb_2t") or 0),
        "branco": float(row.get("branco_2t") or 0),
        "nulo": float(row.get("nulo_2t") or 0),
        "abst": float(row.get("abstencao_2t") or 0),
    }

    sum_o = sum(origins.values())
    sum_d = sum(dests.values())
    # corrige leve discrepância BU vs aptos (arredondamento / votos ≠ comparecimento)
    if apt1 > 0 and abs(sum_o - apt1) > 1:
        # escala origens nominais+BN para bater comparecimento; abst já é residual
        vot_o = sum_o - origins["abst"]
        comp1 = float(row.get("comparecimento_1t") or vot_o)
        if vot_o > 0 and comp1 >= 0:
            scale = comp1 / vot_o if vot_o else 1.0
            for k in ("fa", "fb", "elim", "branco", "nulo"):
                origins[k] *= scale
            origins["abst"] = max(0.0, apt1 - sum(origins[k] for k in ("fa", "fb", "elim", "branco", "nulo")))
        sum_o = sum(origins.values())
    if apt2 > 0 and abs(sum_d - apt2) > 1:
        vot_d = sum_d - dests["abst"]
        comp2 = float(row.get("comparecimento_2t") or vot_d)
        if vot_d > 0 and comp2 >= 0:
            scale = comp2 / vot_d if vot_d else 1.0
            for k in ("fa", "fb", "branco", "nulo"):
                dests[k] *= scale
            dests["abst"] = max(0.0, apt2 - sum(dests[k] for k in ("fa", "fb", "branco", "nulo")))
        sum_d = sum(dests.values())

    n = max(sum_o, sum_d, apt1, apt2)
    delta_aptos = apt2 - apt1
    if sum_o < n - 1e-6:
        origins["aptos_in"] = n - sum_o
    else:
        origins["aptos_in"] = 0.0
    if sum_d < n - 1e-6:
        dests["aptos_out"] = n - sum_d
    else:
        dests["aptos_out"] = 0.0

    return origins, dests, n, delta_aptos


def bounds_for_section(row: pd.Series) -> dict:
    """Calcula limites Duncan–Davis para cada origem-foco × destino."""
    origins, dests, n, delta_aptos = build_margins(row)
    out: dict = {
        "join_key": row.get("join_key"),
        "uf": row.get("uf"),
        "n_total": n,
        "delta_aptos": delta_aptos,
        "identidade_ok": abs(sum(origins.values()) - n) < 1.5
        and abs(sum(dests.values()) - n) < 1.5,
    }
    for o in ORIGENS:
        out[f"o_{o}"] = origins.get(o, 0.0)
    for d in DESTINOS:
        out[f"d_{d}"] = dests.get(d, 0.0)

    narrow_count = 0
    focus_cells = 0
    for o in ORIGENS_FOCO:
        n_o = origins.get(o, 0.0)
        for d in DESTINOS:
            lo, hi = duncan_davis_bounds(n_o, dests.get(d, 0.0), n)
            out[f"{o}_to_{d}_lo"] = lo
            out[f"{o}_to_{d}_hi"] = hi
            out[f"{o}_to_{d}_mid"] = (lo + hi) / 2.0
            width = (hi - lo) / n_o if n_o > 0 else 0.0
            out[f"{o}_to_{d}_width"] = width
            focus_cells += 1
            if n_o > 0 and width <= NARROW_WIDTH:
                narrow_count += 1
                out[f"{o}_to_{d}_narrow"] = True
            else:
                out[f"{o}_to_{d}_narrow"] = False

    out["pct_cells_narrow"] = (
        round(100 * narrow_count / focus_cells, 4) if focus_cells else None
    )
    # Força maioria Elim→Fa ou Elim→Fb pelo limite inferior
    elim = origins.get("elim", 0.0)
    if elim > 0:
        out["elim_forced_fa"] = out["elim_to_fa_lo"] > elim / 2
        out["elim_forced_fb"] = out["elim_to_fb_lo"] > elim / 2
    else:
        out["elim_forced_fa"] = False
        out["elim_forced_fb"] = False
    return out


def compute_bounds_frame(compare_df: pd.DataFrame) -> pd.DataFrame:
    """Aplica bounds a todas as seções status=ambos."""
    ambos = compare_df[compare_df["status"] == "ambos"].copy()
    if ambos.empty:
        return pd.DataFrame()
    rows = [bounds_for_section(r) for _, r in ambos.iterrows()]
    return pd.DataFrame(rows)


def ipf_transition(
    origins: dict[str, float],
    dests: dict[str, float],
    *,
    max_iter: int = 80,
    tol: float = 1e-7,
) -> dict[tuple[str, str], float]:
    """
    Matriz de transição factível por IPF (RAS): casa totais de linha e coluna.

    Semente = produto externo (independência). Resultado soma às margens.
    """
    o_keys = [k for k, v in origins.items() if v > 0 or k in ORIGENS]
    d_keys = [k for k, v in dests.items() if v > 0 or k in DESTINOS]
    # restringe às chaves canônicas (+ padding aptos_*)
    o_keys = [k for k in list(origins.keys()) if origins.get(k, 0) >= 0]
    d_keys = [k for k in list(dests.keys()) if dests.get(k, 0) >= 0]
    O = np.array([float(origins[k]) for k in o_keys], dtype=float)
    D = np.array([float(dests[k]) for k in d_keys], dtype=float)
    n = float(O.sum())
    if n <= 0 or D.sum() <= 0:
        return {(o, d): 0.0 for o in o_keys for d in d_keys}
    # alinha escalas
    if abs(D.sum() - n) > 1e-6:
        D = D * (n / D.sum())
    M = np.outer(O, D) / n
    M = np.maximum(M, 0.0)
    for _ in range(max_iter):
        row = M.sum(axis=1)
        row[row == 0] = 1.0
        M = M * (O / row)[:, None]
        col = M.sum(axis=0)
        col[col == 0] = 1.0
        M = M * (D / col)[None, :]
        if np.max(np.abs(M.sum(axis=1) - O)) < tol and np.max(np.abs(M.sum(axis=0) - D)) < tol:
            break
    return {(o_keys[i], d_keys[j]): float(M[i, j]) for i in range(len(o_keys)) for j in range(len(d_keys))}


def attach_ipf_flows(bounds: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona colunas `{o}_to_{d}_ipf` por seção (matriz coerente 6×5).

    Diferença de aptos entre turnos é absorvida em `abst` (origem ou destino)
    para o IPF fechar só no conjunto canônico — sem células aptos_in/out
    descartadas.
    """
    out = bounds.copy()
    for o in ORIGENS:
        for d in DESTINOS:
            out[f"{o}_to_{d}_ipf"] = 0.0

    for i, row in out.iterrows():
        origins = {o: float(row.get(f"o_{o}", 0) or 0) for o in ORIGENS}
        dests = {d: float(row.get(f"d_{d}", 0) or 0) for d in DESTINOS}
        so, sd = sum(origins.values()), sum(dests.values())
        if not np.isfinite(so) or not np.isfinite(sd) or so < 0 or sd < 0:
            continue
        n = max(so, sd)
        if so < n - 1e-9:
            origins["abst"] = origins.get("abst", 0.0) + (n - so)
        if sd < n - 1e-9:
            dests["abst"] = dests.get("abst", 0.0) + (n - sd)
        flows = ipf_transition(origins, dests)
        for o in ORIGENS:
            for d in DESTINOS:
                out.at[i, f"{o}_to_{d}_ipf"] = flows.get((o, d), 0.0)
    return out


def _weighted_rates(
    bounds: pd.DataFrame, *, origins: tuple[str, ...] = ORIGENS_FOCO
) -> dict[str, float]:
    """Taxas UF = soma(fluxo IPF) / soma(origem)."""
    probe = f"{origins[0]}_to_{DESTINOS[0]}_ipf"
    df = bounds if probe in bounds.columns else attach_ipf_flows(bounds)
    rates: dict[str, float] = {}
    for o in origins:
        w = df[f"o_{o}"].astype(float)
        wsum = float(w.sum())
        for d in DESTINOS:
            flow = df[f"{o}_to_{d}_ipf"].astype(float)
            rates[f"p_{o}_to_{d}"] = float(flow.sum() / wsum) if wsum > 0 else float("nan")
    return rates


def bootstrap_rates(
    bounds: pd.DataFrame, *, n_boot: int = BOOTSTRAP_N, seed: int = BOOTSTRAP_SEED
) -> pd.DataFrame:
    """Bootstrap de seções → percentis das taxas UF (origens-foco)."""
    if bounds.empty:
        return pd.DataFrame()
    df = bounds if f"elim_to_fa_ipf" in bounds.columns else attach_ipf_flows(bounds)
    rng = np.random.default_rng(seed)
    n = len(df)
    keys = [f"p_{o}_to_{d}" for o in ORIGENS_FOCO for d in DESTINOS]
    samples = {k: [] for k in keys}

    idx = np.arange(n)
    for _ in range(n_boot):
        draw = rng.choice(idx, size=n, replace=True)
        sub = df.iloc[draw]
        rates = _weighted_rates(sub, origins=ORIGENS_FOCO)
        for k in keys:
            v = rates.get(k)
            if v is not None and np.isfinite(v):
                samples[k].append(v)

    point = _weighted_rates(df, origins=ORIGENS_FOCO)
    rows = []
    for k in keys:
        arr = np.asarray(samples[k], dtype=float)
        if arr.size == 0:
            rows.append(
                {
                    "taxa": k,
                    "estimate": point.get(k),
                    "p05": None,
                    "p50": None,
                    "p95": None,
                }
            )
            continue
        rows.append(
            {
                "taxa": k,
                "estimate": point.get(k),
                "p05": float(np.percentile(arr, 5)),
                "p50": float(np.percentile(arr, 50)),
                "p95": float(np.percentile(arr, 95)),
            }
        )
    return pd.DataFrame(rows)


def predictive_residuals(
    bounds: pd.DataFrame, rates: dict[str, float]
) -> pd.DataFrame:
    """
    Reconstitui destinos 2º a partir de taxas UF × origens 1º.
    Residual = observado − predito (por destino).
    """
    if bounds.empty:
        return bounds.copy()
    out = bounds if "elim_to_fa_ipf" in bounds.columns else attach_ipf_flows(bounds)
    all_rates = dict(rates)
    all_rates.update(_weighted_rates(out, origins=("fa", "fb")))

    for d in DESTINOS:
        pred = np.zeros(len(out), dtype=float)
        for o in ORIGENS:
            p = all_rates.get(f"p_{o}_to_{d}", 0.0)
            if not np.isfinite(p):
                p = 0.0
            pred += out[f"o_{o}"].astype(float).to_numpy() * float(p)
        obs = out[f"d_{d}"].astype(float).to_numpy()
        out[f"pred_{d}"] = pred
        out[f"resid_{d}"] = obs - pred

    out["resid_fa_abs"] = out["resid_fa"].abs()
    out["resid_fb_abs"] = out["resid_fb"].abs()
    out["resid_abst_abs"] = out["resid_abst"].abs()
    out["resid_margem"] = out["resid_fa"] - out["resid_fb"]
    return out


def abstention_selectivity(compare_df: pd.DataFrame) -> dict:
    """Correlação seção: % eliminados 1º e margem 1º × delta_abstencao."""
    ambos = compare_df[compare_df["status"] == "ambos"].copy()
    if ambos.empty:
        return {
            "corr_pct_elim_delta_abst": None,
            "corr_margem1_delta_abst": None,
            "n": 0,
        }
    comp = pd.to_numeric(ambos["comparecimento_1t"], errors="coerce")
    elim = pd.to_numeric(ambos["votos_eliminados_1t"], errors="coerce")
    margem = pd.to_numeric(ambos["margem_1t"], errors="coerce")
    dab = pd.to_numeric(ambos["delta_abstencao"], errors="coerce")
    pct_elim = elim / comp.replace(0, np.nan)
    mask = pct_elim.notna() & dab.notna()
    corr_e = (
        float(pct_elim[mask].corr(dab[mask])) if mask.sum() > 5 else None
    )
    mask2 = margem.notna() & dab.notna()
    corr_m = (
        float(margem[mask2].corr(dab[mask2])) if mask2.sum() > 5 else None
    )
    return {
        "corr_pct_elim_delta_abst": corr_e,
        "corr_margem1_delta_abst": corr_m,
        "n": int(mask.sum()),
    }


def load_compare(uf: str, turno_a: int = 1, turno_b: int = 2) -> pd.DataFrame | None:
    path = REPORTS_DIR / f"comparar_turnos_{uf.upper()}_{turno_a}t_{turno_b}t.parquet"
    if not path.exists():
        return None
    return pd.read_parquet(path)


def summarize_fluxo(
    bounds: pd.DataFrame,
    rates_boot: pd.DataFrame,
    selectivity: dict,
    uf: str,
) -> dict:
    n = len(bounds)
    narrow = 0
    if n and "pct_cells_narrow" in bounds.columns:
        # seção “estreita” se >50% das células foco são narrow
        narrow = int((bounds["pct_cells_narrow"].fillna(0) >= 50).sum())
    forced_fa = int(bounds["elim_forced_fa"].sum()) if n else 0
    forced_fb = int(bounds["elim_forced_fb"].sum()) if n else 0
    id_ok = int(bounds["identidade_ok"].sum()) if n else 0

    def _rate(name: str) -> dict:
        if rates_boot.empty:
            return {"estimate": None, "p05": None, "p95": None}
        row = rates_boot.loc[rates_boot["taxa"] == name]
        if row.empty:
            return {"estimate": None, "p05": None, "p95": None}
        r = row.iloc[0]
        return {
            "estimate": r["estimate"],
            "p05": r["p05"],
            "p95": r["p95"],
        }

    meta = {
        "uf": uf.upper(),
        "secoes": n,
        "secoes_identidade_ok": id_ok,
        "secoes_narrow_majority": narrow,
        "elim_forced_fa": forced_fa,
        "elim_forced_fb": forced_fb,
        "corr_pct_elim_delta_abst": selectivity.get("corr_pct_elim_delta_abst"),
        "corr_margem1_delta_abst": selectivity.get("corr_margem1_delta_abst"),
        "narrow_width_threshold": NARROW_WIDTH,
        "bootstrap_n": BOOTSTRAP_N,
    }
    for o in ORIGENS_FOCO:
        for d in DESTINOS:
            key = f"p_{o}_to_{d}"
            info = _rate(key)
            meta[f"{key}"] = info["estimate"]
            meta[f"{key}_p05"] = info["p05"]
            meta[f"{key}_p95"] = info["p95"]
    return meta


def write_fluxo_reports(
    bounds: pd.DataFrame,
    rates_boot: pd.DataFrame,
    resid: pd.DataFrame,
    meta: dict,
    uf: str,
    turno_a: int = 1,
    turno_b: int = 2,
) -> tuple[Path, Path, Path, Path]:
    ensure_dirs()
    uf = uf.upper()
    tag = f"{uf}_{turno_a}t_{turno_b}t"
    pq_b = REPORTS_DIR / f"fluxo_bounds_{tag}.parquet"
    pq_r = REPORTS_DIR / f"fluxo_taxas_{tag}.csv"
    pq_res = REPORTS_DIR / f"fluxo_residuos_{tag}.parquet"
    md = REPORTS_DIR / f"fluxo_ecologico_{tag}.md"
    csv_meta = REPORTS_DIR / f"fluxo_ecologico_summary_{tag}.csv"

    bounds.to_parquet(pq_b, index=False)
    rates_boot.to_csv(pq_r, index=False)
    # resíduos: colunas leves
    keep = [
        c
        for c in resid.columns
        if c
        in (
            "join_key",
            "uf",
            "n_total",
            "delta_aptos",
            "identidade_ok",
            "pct_cells_narrow",
            "elim_forced_fa",
            "elim_forced_fb",
            "o_elim",
            "o_branco",
            "o_nulo",
            "o_abst",
            "d_fa",
            "d_fb",
            "d_branco",
            "d_nulo",
            "d_abst",
            "resid_fa",
            "resid_fb",
            "resid_branco",
            "resid_nulo",
            "resid_abst",
            "resid_margem",
            "elim_to_fa_lo",
            "elim_to_fa_hi",
            "elim_to_fb_lo",
            "elim_to_fb_hi",
            "elim_to_abst_lo",
            "elim_to_abst_hi",
        )
        or c.startswith("o_")
        or c.startswith("d_")
        or c.startswith("resid_")
        or "elim_to_" in c
    ]
    # dedupe keep
    keep = list(dict.fromkeys(keep))
    resid[[c for c in keep if c in resid.columns]].to_parquet(pq_res, index=False)
    pd.DataFrame([meta]).to_csv(csv_meta, index=False)

    def _fmt_rate(key: str) -> str:
        est = meta.get(key)
        lo = meta.get(f"{key}_p05")
        hi = meta.get(f"{key}_p95")
        if est is None or (isinstance(est, float) and not np.isfinite(est)):
            return "—"
        if lo is None or hi is None:
            return f"{100 * est:.2f}%"
        return f"{100 * est:.2f}% [{100 * lo:.2f}–{100 * hi:.2f}]"

    lines = [
        f"# Fluxo ecológico 1º→2º — {uf}",
        "",
        "Inferência **agregada por seção** (Duncan–Davis + taxas médias com bootstrap).",
        "Não identifica eleitor a eleitor. Intervalos factíveis ≠ certeza individual.",
        "",
        "## Resumo",
        "",
        f"- Seções (ambos): **{meta['secoes']:,}** · identidade OK: **{meta['secoes_identidade_ok']:,}**",
        f"- Seções com maioria de células “estreitas” "
        f"(largura ≤ {NARROW_WIDTH:.0%}): **{meta['secoes_narrow_majority']:,}**",
        f"- Eliminados *forçados* (limite inf. > 50%) → Fa: **{meta['elim_forced_fa']:,}** · "
        f"→ Fb: **{meta['elim_forced_fb']:,}**",
        "",
        "## Taxas médias UF (Elim / Branco / Nulo / Abst → destinos)",
        "",
        "Estimativa = média ponderada das células de uma matriz IPF por seção "
        "(casa totais de origem e destino; semente = independência); "
        f"IC = percentis 5–95 do bootstrap ({BOOTSTRAP_N} reamostragens de seções). "
        "Duncan–Davis (Parquet de bounds) continua sendo o intervalo factível sem modelo.",
        "",
        "| Origem 1º | → Fa | → Fb | → Branco | → Nulo | → Abst |",
        "|---|---|---|---|---|---|",
    ]
    labels = {"elim": "Eliminados", "branco": "Branco", "nulo": "Nulo", "abst": "Abstenção"}
    for o in ORIGENS_FOCO:
        lines.append(
            f"| {labels[o]} | {_fmt_rate(f'p_{o}_to_fa')} | {_fmt_rate(f'p_{o}_to_fb')} | "
            f"{_fmt_rate(f'p_{o}_to_branco')} | {_fmt_rate(f'p_{o}_to_nulo')} | "
            f"{_fmt_rate(f'p_{o}_to_abst')} |"
        )

    corr_e = meta.get("corr_pct_elim_delta_abst")
    corr_m = meta.get("corr_margem1_delta_abst")
    lines += [
        "",
        "## Abstenção seletiva (correlação seção)",
        "",
        f"- corr(% eliminados 1º, Δ abstenção): "
        f"**{corr_e if corr_e is None else round(corr_e, 4)}**",
        f"- corr(margem 1º, Δ abstenção): "
        f"**{corr_m if corr_m is None else round(corr_m, 4)}**",
        "",
        "## Hipóteses (evidência agregada, não prova)",
        "",
        "| Hipótese | Leitura neste UF |",
        "|---|---|",
        f"| Eliminados → sobretudo Fa | taxa Elim→Fa {_fmt_rate('p_elim_to_fa')}; "
        f"seções forçadas Fa={meta['elim_forced_fa']} |",
        f"| Eliminados → sobretudo Fb | taxa Elim→Fb {_fmt_rate('p_elim_to_fb')}; "
        f"seções forçadas Fb={meta['elim_forced_fb']} |",
        f"| Branco 1º permanece / migra | →Branco {_fmt_rate('p_branco_to_branco')}; "
        f"→Fa {_fmt_rate('p_branco_to_fa')}; →Fb {_fmt_rate('p_branco_to_fb')} |",
        f"| Nulo 1º | →Nulo {_fmt_rate('p_nulo_to_nulo')}; "
        f"→Fa {_fmt_rate('p_nulo_to_fa')}; →Fb {_fmt_rate('p_nulo_to_fb')} |",
        f"| Abstenção seletiva | correlações acima; residual `resid_abst` no Parquet |",
        "",
        "## Limites metodológicos",
        "",
        "- Duncan–Davis: o que é **matematicamente possível** dados só os totais da seção.",
        "- Taxa média + IC: estimativa sob a hipótese de que o ponto médio do intervalo "
        "é um resumo útil e que as seções são trocáveis no bootstrap (troca ecológica).",
        "- Correlação ≠ fraude; RDV≡BU≡CSV só validam integridade entre arquivos públicos.",
        "",
        "## Arquivos",
        "",
        f"- Limites por seção: `{pq_b.name}`",
        f"- Taxas bootstrap: `{pq_r.name}`",
        f"- Resíduos preditivos: `{pq_res.name}`",
        "",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")
    return md, pq_b, pq_r, csv_meta


def print_fluxo_meta(meta: dict) -> None:
    console.print(f"\n[bold]Fluxo ecológico — {meta['uf']}[/bold]")
    table = Table()
    table.add_column("Campo")
    table.add_column("Valor", justify="right")
    table.add_row("Seções", f"{meta['secoes']:,}")
    table.add_row("Narrow (maioria células)", f"{meta['secoes_narrow_majority']:,}")
    table.add_row("Elim forçado → Fa", f"{meta['elim_forced_fa']:,}")
    table.add_row("Elim forçado → Fb", f"{meta['elim_forced_fb']:,}")
    est = meta.get("p_elim_to_fa")
    if est is not None and np.isfinite(est):
        table.add_row(
            "p(Elim→Fa) [IC]",
            f"{100 * est:.2f}% "
            f"[{100 * meta['p_elim_to_fa_p05']:.2f}–{100 * meta['p_elim_to_fa_p95']:.2f}]",
        )
    estb = meta.get("p_elim_to_fb")
    if estb is not None and np.isfinite(estb):
        table.add_row(
            "p(Elim→Fb) [IC]",
            f"{100 * estb:.2f}% "
            f"[{100 * meta['p_elim_to_fb_p05']:.2f}–{100 * meta['p_elim_to_fb_p95']:.2f}]",
        )
    console.print(table)


def run_fluxo_uf(uf: str, turno_a: int = 1, turno_b: int = 2) -> list[Path]:
    uf = uf.upper()
    compare = load_compare(uf, turno_a, turno_b)
    if compare is None:
        console.print(
            f"[red]Falta comparar_turnos_{uf}_{turno_a}t_{turno_b}t.parquet — "
            f"rode `urna-logs comparar-turnos --ufs {uf}`[/red]"
        )
        return []
    if not (compare["status"] == "ambos").any():
        console.print(f"[yellow]{uf}: nenhuma seção em ambos os turnos.[/yellow]")
        return []

    bounds = compute_bounds_frame(compare)
    bounds = attach_ipf_flows(bounds)
    rates = _weighted_rates(bounds)
    rates_boot = bootstrap_rates(bounds)
    resid = predictive_residuals(bounds, rates)
    selectivity = abstention_selectivity(compare)
    meta = summarize_fluxo(bounds, rates_boot, selectivity, uf)
    print_fluxo_meta(meta)
    md, pq_b, pq_r, csv_meta = write_fluxo_reports(
        bounds, rates_boot, resid, meta, uf, turno_a, turno_b
    )
    console.print(f"[green]Relatório:[/green] {md}")
    return [md, pq_b, pq_r, csv_meta]


def consolidate_fluxo_summaries(
    ufs: list[str], turno_a: int = 1, turno_b: int = 2
) -> Path | None:
    frames = []
    for uf in ufs:
        p = REPORTS_DIR / f"fluxo_ecologico_summary_{uf.upper()}_{turno_a}t_{turno_b}t.csv"
        if p.exists():
            frames.append(pd.read_csv(p))
    if not frames:
        return None
    out = REPORTS_DIR / f"fluxo_ecologico_summary_MULTI_{turno_a}t_{turno_b}t.csv"
    pd.concat(frames, ignore_index=True).to_csv(out, index=False)
    return out


def run_fluxo_ecologico(
    ufs: list[str], turno_a: int = 1, turno_b: int = 2
) -> list[Path]:
    outputs: list[Path] = []
    done: list[str] = []
    for i, uf in enumerate(ufs, start=1):
        console.print(f"\n[bold][{i}/{len(ufs)}] Fluxo ecológico {uf.upper()}[/bold]")
        paths = run_fluxo_uf(uf, turno_a, turno_b)
        outputs.extend(paths)
        if paths:
            done.append(uf.upper())
    if len(done) > 1:
        multi = consolidate_fluxo_summaries(done, turno_a, turno_b)
        if multi:
            console.print(f"\n[green]Resumo multi-UF:[/green] {multi}")
            outputs.append(multi)
    return outputs
