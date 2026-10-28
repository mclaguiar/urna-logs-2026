"""Testes: Duncan–Davis, identidade e taxas sintéticas."""

import pandas as pd

from urna_logs.fluxo_ecologico import (
    attach_ipf_flows,
    bootstrap_rates,
    compute_bounds_frame,
    duncan_davis_bounds,
    ipf_transition,
    predictive_residuals,
    _weighted_rates,
)


def test_duncan_davis_basic():
    # N=100, origem=40, destino=30 → max=30, min=max(0,40+30-100)=0
    lo, hi = duncan_davis_bounds(40, 30, 100)
    assert lo == 0
    assert hi == 30

    # N=100, origem=80, destino=70 → min=50, max=70
    lo, hi = duncan_davis_bounds(80, 70, 100)
    assert lo == 50
    assert hi == 70


def test_duncan_davis_narrow_identifies_flow():
    # Quase determinado: origem=10, destino=95, N=100 → min=5, max=10
    lo, hi = duncan_davis_bounds(10, 95, 100)
    assert lo == 5
    assert hi == 10
    assert (hi - lo) / 10 <= 0.5


def test_bounds_frame_synthetic():
    """Seção sintética: eliminados e ganho de Fa forçam fluxo Elim→Fa."""
    df = pd.DataFrame(
        [
            {
                "uf": "XX",
                "join_key": "XX:1:1:1",
                "status": "ambos",
                "aptos_1t": 100,
                "aptos_2t": 100,
                "comparecimento_1t": 90,
                "comparecimento_2t": 90,
                "abstencao_1t": 10,
                "abstencao_2t": 10,
                "votos_fa_1t": 20,
                "votos_fb_1t": 20,
                "votos_eliminados_1t": 40,
                "branco_1t": 5,
                "nulo_1t": 5,
                "votos_fa_2t": 55,
                "votos_fb_2t": 25,
                "branco_2t": 5,
                "nulo_2t": 5,
                "delta_abstencao": 0,
                "margem_1t": 0,
            }
        ]
    )
    bounds = compute_bounds_frame(df)
    assert len(bounds) == 1
    assert bool(bounds.iloc[0]["identidade_ok"])
    # Elim=40, Fa2=55, N=100 → Elim→Fa min=max(0,40+55-100)=0, max=40
    assert bounds.iloc[0]["elim_to_fa_lo"] == 0
    assert bounds.iloc[0]["elim_to_fa_hi"] == 40
    # Caso forçado: Fa2=90, Elim=40 → min=30 > 20 (metade)
    df2 = df.copy()
    df2.loc[0, "votos_fa_2t"] = 90
    df2.loc[0, "votos_fb_2t"] = 0
    df2.loc[0, "branco_2t"] = 0
    df2.loc[0, "nulo_2t"] = 0
    df2.loc[0, "comparecimento_2t"] = 90
    df2.loc[0, "abstencao_2t"] = 10
    b2 = compute_bounds_frame(df2)
    assert b2.iloc[0]["elim_to_fa_lo"] == 30
    assert bool(b2.iloc[0]["elim_forced_fa"])


def test_ipf_matches_margins():
    origins = {"fa": 20.0, "fb": 20.0, "elim": 40.0, "branco": 5.0, "nulo": 5.0, "abst": 10.0}
    dests = {"fa": 55.0, "fb": 25.0, "branco": 5.0, "nulo": 5.0, "abst": 10.0}
    flows = ipf_transition(origins, dests)
    for o, n_o in origins.items():
        assert abs(sum(flows[(o, d)] for d in dests) - n_o) < 1e-4
    for d, n_d in dests.items():
        assert abs(sum(flows[(o, d)] for o in origins) - n_d) < 1e-4
    # eliminados devem alimentar sobretudo Fa (destino maior no 2º)
    assert flows[("elim", "fa")] > flows[("elim", "fb")]


def test_weighted_rates_and_bootstrap():
    rows = []
    for i in range(30):
        rows.append(
            {
                "uf": "XX",
                "join_key": f"XX:1:1:{i}",
                "status": "ambos",
                "aptos_1t": 100,
                "aptos_2t": 100,
                "comparecimento_1t": 80,
                "comparecimento_2t": 80,
                "abstencao_1t": 20,
                "abstencao_2t": 20,
                "votos_fa_1t": 30,
                "votos_fb_1t": 20,
                "votos_eliminados_1t": 20,
                "branco_1t": 5,
                "nulo_1t": 5,
                "votos_fa_2t": 40,
                "votos_fb_2t": 25,
                "branco_2t": 5,
                "nulo_2t": 10,
                "delta_abstencao": 0,
                "margem_1t": 10,
            }
        )
    bounds = attach_ipf_flows(compute_bounds_frame(pd.DataFrame(rows)))
    rates = _weighted_rates(bounds)
    assert "p_elim_to_fa" in rates
    assert 0 <= rates["p_elim_to_fa"] <= 1
    # IPF não deve colapsar em 50/50 quando Fa2 > Fb2
    assert rates["p_elim_to_fa"] > rates["p_elim_to_fb"]
    boot = bootstrap_rates(bounds, n_boot=50, seed=1)
    assert not boot.empty
    row = boot.loc[boot["taxa"] == "p_elim_to_fa"].iloc[0]
    assert row["p05"] <= row["estimate"] <= row["p95"]
    resid = predictive_residuals(bounds, rates)
    assert "resid_fa" in resid.columns
    assert resid["resid_fa"].notna().all()
