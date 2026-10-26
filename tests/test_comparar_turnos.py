"""Esqueleto do comparativo 1º×2º sem dados do 2º turno."""

from urna_logs.comparar_turnos import build_compare, empty_compare_frame


def test_empty_schema():
    df = empty_compare_frame("AC")
    assert "delta_comparecimento" in df.columns
    assert "status" in df.columns


def test_build_pendente_when_no_2t(tmp_path, monkeypatch):
    # Usa AC real se audit 1t existir; senão só valida mensagem de falta
    df, meta = build_compare("AC", 1, 2)
    assert meta["uf"] == "AC"
    if meta["turno_a_disponivel"] and not meta["turno_b_disponivel"]:
        assert meta["pronto"] is False
        assert (df["status"] == "pendente_2t").all()
        assert "ainda não disponível" in meta["mensagem"]
    elif not meta["turno_a_disponivel"]:
        assert df.empty
        assert "Falta audit" in meta["mensagem"]
