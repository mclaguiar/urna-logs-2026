"""Hierarquia A/B/C de achados de auditoria."""

import pandas as pd

from urna_logs.achados import NIVEL_A, NIVEL_B, NIVEL_C, classify_row


def _row(**kwargs):
    base = {
        "join_key": "AC:1:1:1",
        "status": "ambos",
        "flag_margem": False,
        "flag_abstencao": False,
        "flag_pos17": False,
        "flag_sem_digital_x_margem": False,
    }
    base.update(kwargs)
    return pd.Series(base)


def test_nivel_a_so_turno():
    nivel, codes, _ = classify_row(
        _row(status="so_1t"),
        audit_fail_1t=set(),
        audit_fail_2t=set(),
        cruzar_1t=set(),
        cruzar_2t=set(),
    )
    assert nivel == NIVEL_A
    assert any(c.startswith("A_") for c in codes)


def test_nivel_a_cruzar():
    nivel, codes, _ = classify_row(
        _row(),
        audit_fail_1t=set(),
        audit_fail_2t=set(),
        cruzar_1t=set(),
        cruzar_2t={"AC:1:1:1"},
    )
    assert nivel == NIVEL_A
    assert "A_cruzar_bu_oficial_2t" in codes


def test_nivel_b_confluencia():
    nivel, codes, _ = classify_row(
        _row(flag_margem=True, flag_abstencao=True),
        audit_fail_1t=set(),
        audit_fail_2t=set(),
        cruzar_1t=set(),
        cruzar_2t=set(),
    )
    assert nivel == NIVEL_B
    assert any(c.startswith("B_") for c in codes)


def test_nivel_c_isolada():
    nivel, codes, conclusao = classify_row(
        _row(flag_margem=True),
        audit_fail_1t=set(),
        audit_fail_2t=set(),
        cruzar_1t=set(),
        cruzar_2t=set(),
    )
    assert nivel == NIVEL_C
    assert "C_margem_isolada" in codes
    assert "sinal isolado" in conclusao.lower()
