"""Validação go/no-go do fluxo (sintético + piloto se existir)."""

import pandas as pd

from urna_logs.fluxo_ecologico import (
    attach_ipf_flows,
    compute_bounds_frame,
    _weighted_rates,
)
from urna_logs.validar_fluxo import Check, UfValidation, validate_uf


def test_validate_uf_ac_if_present():
    r = validate_uf("AC")
    if r.n_secoes == 0:
        assert any(c.id == "prereq_comparar" for c in r.checks)
        return
    assert r.n_secoes >= 50
    hard = r.hard_failures()
    assert hard == [], f"hard failures: {[(c.id, c.detail) for c in hard]}"
    assert r.go is True


def test_uf_validation_dataclass():
    v = UfValidation(uf="XX", go=False, checks=[Check("a", False, "x", "hard")])
    assert len(v.hard_failures()) == 1
