"""Ano no download e no calendário, sem rede."""

from urna_logs.config import data_turno, zip_url
from urna_logs.download import state_key
from urna_logs.oficial import cache_path, votacao_zip_path


def test_zip_url_2022_ac():
    assert zip_url("AC", 1, 2022) == (
        "https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2022/arqurnatot/"
        "bu_imgbu_logjez_rdv_vscmr_2022_1t_AC.zip"
    )
    assert zip_url("ac", 2, 2022).endswith("bu_imgbu_logjez_rdv_vscmr_2022_2t_AC.zip")


def test_state_key_2026_permanece():
    assert state_key("AC", 1, 2026) == "AC_1"
    assert state_key("AC", 1, 2022) == "2022_AC_1"


def test_calendario():
    assert data_turno(1) is not None and data_turno(1).isoformat() == "2026-10-04"
    assert data_turno(2, 2022).isoformat() == "2022-10-30"
    assert data_turno(1, 2022).isoformat() == "2022-10-02"


def test_cache_oficial_nao_colide():
    assert cache_path("AC", 1).name == "oficial_presidente_votos_AC_1t.parquet"
    assert "anomalias" in str(cache_path("AC", 1, 2022)).replace("\\", "/")
    assert votacao_zip_path(2026).name == "votacao_secao_2026_BR.zip"
    assert "anomalias" in str(votacao_zip_path(2022)).replace("\\", "/")
