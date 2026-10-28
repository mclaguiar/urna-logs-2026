"""Testes do mapeamento stem → join_key e faixas horárias."""

from urna_logs.fuso import (
    JANELA_FORA,
    JANELA_HISTORICO,
    JANELA_OFICIAL,
    JANELA_POS,
    janela_habilitacao,
)
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
    from datetime import date

    from urna_logs.parse_log import count_habilitado_hours_from_jez_bytes

    raw = (
        b"04/10/2026\t15:00:00\tINFO\t1\tVOTA\tEleitor foi habilitado\tx\n"
        b"04/10/2026\t17:00:00\tINFO\t1\tVOTA\tEleitor foi habilitado\ty\n"
        b"25/10/2026\t21:00:00\tINFO\t1\tVOTA\tEleitor foi habilitado\tz\n"
    )
    counts, urnas, by_day = count_habilitado_hours_from_jez_bytes(raw)
    assert counts[15] == 1
    assert counts[17] == 1
    assert counts[21] == 1
    assert sum(counts) == 3
    assert set(by_day) == {"2026-10-04", "2026-10-25"}

    counts_2t, _, by_day2 = count_habilitado_hours_from_jez_bytes(
        raw, data_filtro=date(2026, 10, 25)
    )
    assert sum(counts_2t) == 1
    assert counts_2t[21] == 1
    assert by_day2["2026-10-04"][15] == 1  # diagnóstico mantém outros dias


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


def test_tipo_habilitacao_por_hora():
    """Curva rápida separa biométrica e biografia (ano de nascimento) por hora."""
    from urna_logs.parse_log import count_habilitado_hours_from_bytes

    raw = (
        b"04/10/2026\t10:00:00\tINFO\t1\tVOTA\t"
        b"Tipo de habilita\xe7\xe3o do eleitor [biom\xe9trica]\ta\n"
        b"04/10/2026\t10:00:01\tINFO\t1\tVOTA\tEleitor foi habilitado\tb\n"
        b"04/10/2026\t11:00:00\tINFO\t1\tVOTA\t"
        b"Ano de nascimento digitado \xe9 igual ao do cadastro\tc\n"
        b"04/10/2026\t11:00:01\tINFO\t1\tVOTA\tEleitor foi habilitado\td\n"
        b"04/10/2026\t12:00:00\tINFO\t1\tVOTA\t"
        b"Solicita\xe7\xe3o de dado pessoal do eleitor para habilita\xe7\xe3o manual\te\n"
        b"04/10/2026\t12:00:05\tINFO\t1\tVOTA\tEleitor foi habilitado\tf\n"
        # manual antigo não pode vazar: a biométrica seguinte ganha
        b"04/10/2026\t13:00:00\tINFO\t1\tVOTA\t"
        b"Solicita\xe7\xe3o de dado pessoal do eleitor para habilita\xe7\xe3o manual\tg\n"
        b"04/10/2026\t13:00:02\tINFO\t1\tVOTA\t"
        b"Tipo de habilita\xe7\xe3o do eleitor [biom\xe9trica]\th\n"
        b"04/10/2026\t13:00:03\tINFO\t1\tVOTA\tEleitor foi habilitado\ti\n"
    )
    by_tipo: dict = {}
    counts = count_habilitado_hours_from_bytes(raw, by_tipo=by_tipo)
    assert counts[10] == 1 and counts[11] == 1 and counts[12] == 1 and counts[13] == 1
    dia = by_tipo["2026-10-04"]
    # índices: 0 biométrica, 1 manual, 2 sem biometria, 3 desconhecido
    assert dia[10] == [1, 0, 0, 0]
    assert dia[11] == [0, 1, 0, 0]
    assert dia[12] == [0, 1, 0, 0]
    assert dia[13] == [1, 0, 0, 0]
    assert sum(sum(row) for row in dia) == sum(counts)


def test_confronto_habilitacoes_votos_bu():
    from urna_logs.horario import _linhas_confronto_bu
    from urna_logs.parse_log import count_eventos_dia_from_bytes

    fecha = "\n".join(
        _linhas_confronto_bu(
            {
                "total_habilitacoes": 100,
                "bu_votos_presidente": 100,
                "bu_nominal": 90,
                "bu_branco": 4,
                "bu_nulo": 6,
                "bu_outros": 0,
                "delta_hab_menos_bu": 0,
                "log_votos_computados": 100,
                "log_suspensos_sem_voto": 0,
            }
        )
    )
    assert "diferença é **0**" in fecha
    assert "nominais **90**" in fecha
    assert "brancos **4**" in fecha
    assert "nulos **6**" in fecha

    gap = "\n".join(
        _linhas_confronto_bu(
            {
                "total_habilitacoes": 488,
                "bu_votos_presidente": 100,
                "bu_nominal": 90,
                "bu_branco": 4,
                "bu_nulo": 6,
                "delta_hab_menos_bu": 388,
                "log_votos_computados": 100,
                "log_suspensos_sem_voto": 361,
            }
        )
    )
    assert "fecham com o BU" in gap
    assert "voto **não foi registrado**" in gap
    assert "**+388**" in gap
    assert "**361**" in gap
    assert "**27**" in gap
    from urna_logs.horario import _nota_hab_sem_voto

    nota = "\n".join(
        _nota_hab_sem_voto(
            {
                "delta_hab_menos_bu": 388,
                "log_suspensos_sem_voto": 361,
            }
        )
    )
    assert "não viraram voto" in nota
    assert "**361**" in nota
    assert "**27**" in nota
    assert _nota_hab_sem_voto({"delta_hab_menos_bu": 0}) == []

    raw = (
        b"04/10/2026\t10:00:00\tINFO\t1\tVOTA\t"
        b"Eleitor foi suspenso e n\xe3o confirmou nenhum voto\ta\n"
        b"04/10/2026\t10:01:00\tINFO\t1\tVOTA\tO voto do eleitor foi computado\tb\n"
        b"25/10/2026\t10:01:00\tINFO\t1\tVOTA\tO voto do eleitor foi computado\tc\n"
    )
    by: dict = {}
    count_eventos_dia_from_bytes(raw, by)
    assert by["2026-10-04"] == [1, 1]
    assert by["2026-10-25"] == [1, 0]


def test_count_habilitado_hours_from_bytes():
    from datetime import date

    from urna_logs.parse_log import count_habilitado_hours_from_bytes

    raw = (
        b"04/10/2026\t10:00:00\tINFO\t1\tVOTA\tOutra mensagem\tabc\n"
        b"04/10/2026\t17:05:01\tINFO\t99\tVOTA\tEleitor foi habilitado\tdef\n"
        b"04/10/2026\t15:01:00\tINFO\t99\tVOTA\tEleitor foi habilitado\tx\n"
        b"25/10/2026\t21:01:00\tINFO\t99\tVOTA\tEleitor foi habilitado\tz\n"
    )
    counts = count_habilitado_hours_from_bytes(raw)
    assert counts[17] == 1
    assert counts[15] == 1
    assert counts[21] == 1
    assert sum(counts) == 3

    only_1t = count_habilitado_hours_from_bytes(raw, data_filtro=date(2026, 10, 4))
    assert sum(only_1t) == 2
    assert only_1t[21] == 0


def test_janela_habilitacao_oficial_pos_fora():
    from datetime import date

    from urna_logs.config import data_pertence_ao_turno

    d1, d2 = date(2026, 10, 4), date(2026, 10, 25)
    assert janela_habilitacao(10, "SP", data_evento=d2, data_oficial=d2, turno=2) == JANELA_OFICIAL
    assert janela_habilitacao(17, "SP", data_evento=d2, data_oficial=d2, turno=2) == JANELA_POS
    assert janela_habilitacao(7, "SP", data_evento=d2, data_oficial=d2, turno=2) == JANELA_FORA
    # 1º turno no .jez do 2º → histórico (fora da tolerância ±3 dias)
    assert janela_habilitacao(21, "SP", data_evento=d1, data_oficial=d2, turno=2) == JANELA_HISTORICO
    assert not data_pertence_ao_turno(d1, 2)
    assert data_pertence_ao_turno(d2, 2)
    # Folga ±3 dias ainda conta como do turno
    assert data_pertence_ao_turno(date(2026, 10, 22), 2)
    assert data_pertence_ao_turno(date(2026, 10, 28), 2)
    assert not data_pertence_ao_turno(date(2026, 10, 21), 2)
    assert janela_habilitacao(
        10, "SP", data_evento=date(2026, 10, 28), data_oficial=d2, turno=2
    ) == JANELA_OFICIAL
    # AC: 15h local = 17h BRT → pós-encerramento
    assert janela_habilitacao(15, "AC", data_evento=d1, data_oficial=d1, turno=1) == JANELA_POS
    assert janela_habilitacao(14, "AC", data_evento=d1, data_oficial=d1, turno=1) == JANELA_OFICIAL
