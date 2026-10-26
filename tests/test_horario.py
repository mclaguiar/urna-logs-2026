"""Testes do mapeamento stem → join_key e faixas horárias."""

from urna_logs.horario import (
    apos_encerramento_oficial,
    delta_local_para_brt,
    faixa_hora,
    hora_brasilia,
    join_key_from_stem,
    stem_from_source,
)
from urna_logs.parse_log import _habilitado_hours_from_text, parse_line


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


def test_brt_exceto_exterior():
    from urna_logs.fuso import (
        apos_encerramento_oficial as apos_fuso,
        delta_local_para_brt as delta_fuso,
        hora_brasilia as hb_fuso,
    )

    # AC UTC−5 → local +2h = BRT; 15h local = 17h BRT
    assert delta_local_para_brt("AC") == 2 == delta_fuso("AC")
    assert hora_brasilia(15, "AC") == 17 == hb_fuso(15, "AC")
    assert apos_encerramento_oficial(15, "AC") is True
    assert apos_fuso(14, "AC") is False
    assert faixa_hora(15, uf="AC") == "17_18h"

    # AM UTC−4 → +1h; 16h local = 17h BRT
    assert delta_local_para_brt("AM") == 1
    assert apos_encerramento_oficial(16, "AM") is True
    assert apos_encerramento_oficial(15, "AM") is False

    # SP já é BRT
    assert delta_local_para_brt("SP") == 0
    assert hora_brasilia(17, "SP") == 17

    # Exterior: sem conversão; 17h local conta
    assert delta_local_para_brt("ZZ") is None
    assert hora_brasilia(15, "ZZ") == 15
    assert apos_encerramento_oficial(15, "ZZ") is False
    assert apos_encerramento_oficial(17, "ZZ") is True
    assert faixa_hora(15, uf="ZZ") == "12_17h"


def test_count_habilitado_hours_from_jez_bytes_plain():
    """Caminho rápido: .log solto (não-ZIP) dentro do walk."""
    from urna_logs.parse_log import count_habilitado_hours_from_jez_bytes

    raw = (
        b"04/10/2026\t15:00:00\tINFO\t1\tVOTA\tEleitor foi habilitado\tx\n"
        b"04/10/2026\t17:00:00\tINFO\t1\tVOTA\tEleitor foi habilitado\ty\n"
    )
    counts, urnas = count_habilitado_hours_from_jez_bytes(raw)
    assert counts[15] == 1
    assert counts[17] == 1
    assert sum(counts) == 2


def test_filtro_rapido_habilitado():
    text = "\n".join(
        [
            "04/10/2026\t10:00:00\tINFO\t1\tVOTA\tOutra mensagem\tabc",
            "04/10/2026\t17:05:01\tINFO\t1\tVOTA\tEleitor foi habilitado\tdef",
        ]
    )
    evs = list(_habilitado_hours_from_text(text, "t"))
    assert len(evs) == 1
    assert evs[0].after_17h is True
    assert parse_line(text.splitlines()[0]) is not None


def test_count_habilitado_hours_from_bytes():
    from urna_logs.parse_log import count_habilitado_hours_from_bytes

    raw = (
        b"04/10/2026\t10:00:00\tINFO\t1\tVOTA\tOutra mensagem\tabc\n"
        b"04/10/2026\t17:05:01\tINFO\t99\tVOTA\tEleitor foi habilitado\tdef\n"
        b"04/10/2026\t15:01:00\tINFO\t99\tVOTA\tEleitor foi habilitado\tx\n"
    )
    counts = count_habilitado_hours_from_bytes(raw)
    assert counts[17] == 1
    assert counts[15] == 1
    assert sum(counts) == 2
