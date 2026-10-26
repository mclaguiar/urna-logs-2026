"""Testes do mapeamento stem → join_key e faixas horárias."""

from urna_logs.horario import faixa_hora, join_key_from_stem, stem_from_source


def test_stem_from_log_source():
    src = "o03220ac0101500020088-log.jez:d000000.log"
    assert stem_from_source(src) == "o03220ac0101500020088"
    assert join_key_from_stem("o03220ac0101500020088") == "AC:01015:0002:0088"


def test_faixa_hora():
    assert faixa_hora(7) == "antes_08h"
    assert faixa_hora(10) == "08_12h"
    assert faixa_hora(15) == "12_17h"
    assert faixa_hora(17) == "17_18h"
    assert faixa_hora(18) == "18_19h"
    assert faixa_hora(20) == "19h_mais"
    assert faixa_hora(None) == "sem_hora"
