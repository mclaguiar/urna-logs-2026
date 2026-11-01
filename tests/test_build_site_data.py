"""Soma de sem digital no painel: recorte com detalhe no boletim."""

import importlib.util
from pathlib import Path

import pandas as pd

_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build_site_data.py"
_spec = importlib.util.spec_from_file_location("build_site_data", _PATH)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def test_agregar_sem_digital_ignora_municipio_sem_detalhe():
    df = pd.DataFrame(
        [
            {
                "uf": "ES",
                "municipio": 1,
                "urnas": 10,
                "comparecimento": 1000,
                "biografia": 60,
                "sem_biometria": 200,
                "sem_digital": 260,
                "pct_sem_digital": 26.0,
            },
            {
                "uf": "ES",
                "municipio": 2,
                "urnas": 5,
                "comparecimento": 500,
                "biografia": None,
                "sem_biometria": None,
                "sem_digital": None,
                "pct_sem_digital": None,
            },
        ]
    )
    row = _mod._agregar_sem_digital(df, 1)
    assert row["comparecimento_1t"] == 1000
    assert row["municipios_1t"] == 1
    assert row["biografia_1t"] == 60
    assert row["sem_biometria_1t"] == 200
    assert row["sem_digital_1t"] == 260
    assert row["biografia_1t"] + row["sem_biometria_1t"] == row["sem_digital_1t"]
    assert row["pct_biografia_1t"] == 6.0
    assert row["pct_sem_biometria_1t"] == 20.0
    assert row["pct_sem_digital_1t"] == 26.0
    assert row["com_detalhe_bio_1t"] is True


def test_agregar_sem_digital_uf_sem_detalhe_fica_vazia():
    df = pd.DataFrame(
        [
            {
                "uf": "ZZ",
                "municipio": 1,
                "urnas": 3,
                "comparecimento": 400,
                "biografia": None,
                "sem_biometria": None,
                "sem_digital": None,
                "pct_sem_digital": None,
            }
        ]
    )
    row = _mod._agregar_sem_digital(df, 2)
    assert row["com_detalhe_bio_2t"] is False
    assert row["biografia_2t"] is None
    assert row["sem_biometria_2t"] is None
    assert row["sem_digital_2t"] is None
    assert row["pct_biografia_2t"] is None
    assert row["pct_sem_biometria_2t"] is None
    assert row["comparecimento_2t"] == 400
