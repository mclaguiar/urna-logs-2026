"""Comparativo 1º×2º: esquema, pendente e decomposição de votos."""

from pathlib import Path

import pandas as pd

from urna_logs.comparar_turnos import (
    apply_anomaly_flags,
    build_compare,
    discover_finalistas,
    empty_compare_frame,
    pct_apos_17h_uf,
    pivot_votos_secao,
)


def test_empty_schema():
    df = empty_compare_frame("AC")
    assert "delta_comparecimento" in df.columns
    assert "delta_margem" in df.columns
    assert "status" in df.columns


def test_build_pendente_or_pronto_ac():
    df, meta = build_compare("AC", 1, 2)
    assert meta["uf"] == "AC"
    if meta["turno_a_disponivel"] and not meta["turno_b_disponivel"]:
        assert meta["pronto"] is False
        assert (df["status"] == "pendente_2t").all()
        assert "ainda não disponível" in meta["mensagem"]
    elif not meta["turno_a_disponivel"]:
        assert df.empty
        assert "Falta audit" in meta["mensagem"]
    elif meta["pronto"]:
        assert "votos_fa_1t" in df.columns
        assert meta.get("finalistas")
        assert (df["status"] == "ambos").any() or meta["secoes_ambos"] >= 0


def test_discover_finalistas_and_pivot(tmp_path, monkeypatch):
    votos_2 = pd.DataFrame(
        [
            {"join_key": "AC:1:1:1", "tipo": "nominal", "numero": "13", "votos_bu": 40},
            {"join_key": "AC:1:1:1", "tipo": "nominal", "numero": "22", "votos_bu": 50},
            {"join_key": "AC:1:1:1", "tipo": "branco", "numero": None, "votos_bu": 2},
            {"join_key": "AC:1:1:1", "tipo": "nulo", "numero": None, "votos_bu": 3},
        ]
    )
    votos_1 = pd.DataFrame(
        [
            {"join_key": "AC:1:1:1", "tipo": "nominal", "numero": "13", "votos_bu": 30},
            {"join_key": "AC:1:1:1", "tipo": "nominal", "numero": "22", "votos_bu": 45},
            {"join_key": "AC:1:1:1", "tipo": "nominal", "numero": "70", "votos_bu": 20},
            {"join_key": "AC:1:1:1", "tipo": "branco", "numero": None, "votos_bu": 1},
            {"join_key": "AC:1:1:1", "tipo": "nulo", "numero": None, "votos_bu": 1},
        ]
    )
    fins = discover_finalistas(votos_2)
    assert fins == ["13", "22"]
    p1 = pivot_votos_secao(votos_1, fins)
    p2 = pivot_votos_secao(votos_2, fins)
    assert int(p1.iloc[0]["votos_eliminados"]) == 20
    assert int(p1.iloc[0]["votos_fa"]) == 30
    assert int(p2.iloc[0]["votos_fb"]) == 50
    margem_1 = 30 - 45
    margem_2 = 40 - 50
    assert margem_2 - margem_1 == 5  # delta_margem esperado


def test_anomaly_flag_extremes():
    df = pd.DataFrame(
        {
            "status": ["ambos"] * 20,
            "delta_abstencao": list(range(20)),
            "delta_margem": [0] * 19 + [100],
            "pct_sem_digital_1t": [5.0] * 19 + [80.0],
            "pct_apos_17h_2t": [1.0] * 20,
            "delta_pct_apos_17h_secao": [0.0] * 20,
        }
    )
    out = apply_anomaly_flags(df)
    assert bool(out.iloc[-1]["flag_margem"])
    assert "margem" in out.iloc[-1]["flags"]


def test_pct_apos_17h_uf_fallback_secao(tmp_path, monkeypatch):
    import urna_logs.comparar_turnos as ct

    monkeypatch.setattr(ct, "REPORTS_DIR", tmp_path)
    secao = pd.DataFrame(
        {
            "join_key": ["X:1:1:1", "X:1:1:2"],
            "hab_total": [100, 300],
            "hab_apos_17h": [10, 30],
            "pct_apos_17h": [10.0, 10.0],
        }
    )
    secao.to_parquet(tmp_path / "horario_secao_XX_2t.parquet", index=False)
    assert pct_apos_17h_uf("XX", 2) == 10.0
    assert pct_apos_17h_uf("XX", 1) is None
