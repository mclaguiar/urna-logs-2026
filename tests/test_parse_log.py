from urna_logs.parse_log import classify_habilitacoes, parse_line


def test_parse_line_slash_date():
    line = (
        "04/10/2026\t17:05:01\tINFO\t2246399\tVOTA\tEleitor foi habilitado\t378630A6868F0AD4"
    )
    ev = parse_line(line, source="t")
    assert ev is not None
    assert ev.aplicativo == "VOTA"
    assert ev.after_17h is True
    assert "habilitado" in ev.mensagem.lower()


def test_parse_line_compact_date():
    line = "20261004\t165101\tINFO\t2246399\tVOTA\tO eleitor não possui biometria\t81CC3374D4BC42F7"
    ev = parse_line(line)
    assert ev is not None
    assert ev.after_17h is False


def test_classify_sem_biometria():
    lines = [
        "04/10/2026\t16:51:58\tALERTA\t2246399\tVOTA\tO eleitor não possui biometria\t81CC3374D4BC42F7",
        "04/10/2026\t16:52:03\tINFO\t2246399\tVOTA\tEleitor foi habilitado\t0E9B9BD09EDA3A65",
    ]
    events = [parse_line(l, source="x") for l in lines]
    habs = list(classify_habilitacoes(e for e in events if e))
    assert len(habs) == 1
    assert habs[0].tipo == "sem_biometria"
    assert habs[0].after_17h is False


def test_classify_biometrica():
    lines = [
        "04/10/2026\t17:15:44\tINFO\t2246399\tVOTA\tTipo de habilitação do eleitor [biométrica]\t4B39DE347EA16795",
        "04/10/2026\t17:15:44\tINFO\t2246399\tVOTA\tEleitor foi habilitado\t378630A6868F0AD4",
    ]
    events = [parse_line(l) for l in lines]
    habs = list(classify_habilitacoes(e for e in events if e))
    assert habs[0].tipo == "biometrica"
    assert habs[0].after_17h is True


def test_classify_manual_falha():
    lines = [
        "04/10/2026\t17:28:08\tINFO\t2246399\tVOTA\tSolicitação de dado pessoal do eleitor para habilitação manual\tF71B29106B67AEE0",
        "04/10/2026\t17:28:17\tINFO\t2246399\tVOTA\tSolicita digital do mesário\tD9E7E6D8CB507B95",
        "04/10/2026\t17:28:26\tINFO\t2246399\tVOTA\tEleitor foi habilitado\tF5A367BD7738C487",
    ]
    events = [parse_line(l) for l in lines]
    habs = list(classify_habilitacoes(e for e in events if e))
    assert habs[0].tipo == "manual_falha"
    assert habs[0].after_17h is True
