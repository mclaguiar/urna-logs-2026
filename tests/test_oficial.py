"""Testes do mapeamento e resumo do cruzamento oficial."""

import pandas as pd

from urna_logs.oficial import audit_votavel, summarize_cruzamento


def test_audit_votavel_mapping():
    assert audit_votavel("branco", None) == "95"
    assert audit_votavel("nulo", None) == "96"
    assert audit_votavel("nominal", 13) == "13"
    assert audit_votavel("nominal", 22.0) == "22"
    assert audit_votavel("nominal", None) is None
    assert audit_votavel("legenda", 13) is None


def test_summarize_all_ok():
    df = pd.DataFrame(
        {
            "join_key": ["AC:01007:0009:0001", "AC:01007:0009:0001", "AC:01007:0009:0002"],
            "votavel": ["13", "95", "13"],
            "votos_bu": [10, 2, 5],
            "votos_oficial": [10, 2, 5],
            "ok": [True, True, True],
            "lado": ["ambos", "ambos", "ambos"],
        }
    )
    s = summarize_cruzamento(df)
    assert s["secoes"] == 2
    assert s["secoes_ok"] == 2
    assert s["linhas_divergentes"] == 0
    assert s["votos_bu"] == 17
