"""Testes de parse/hash do .vsc (precisa do ZIP AC 1º em data/raw)."""

from pathlib import Path

import pytest

from urna_logs.config import zip_path
from urna_logs.verificar_vsc import join_key_from_stem, run_verificar_vsc


def test_join_key_from_stem():
    assert join_key_from_stem("o03220ac0101500020088") == "AC:01015:0002:0088"
    assert join_key_from_stem("x") is None


@pytest.mark.skipif(
    not zip_path("AC", 1).exists(),
    reason="ZIP AC 1º não presente",
)
def test_verificar_vsc_ac_limit():
    paths = run_verificar_vsc(["AC"], 1, nivel=1, limit=5)
    assert paths
    pq = Path("reports/verificar_vsc_AC_1t.parquet")
    assert pq.exists()
    import pandas as pd

    df = pd.read_parquet(pq)
    assert len(df) == 5
    assert df["tem_vsc"].all()
    assert df["parse_ok"].all()
    assert (df["nivel_ok"] >= 1).all()
    assert df["n_hash_fail"].sum() == 0
