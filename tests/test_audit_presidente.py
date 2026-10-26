"""Testes de recontagem presidente (BU × RDV)."""

from pathlib import Path

from urna_logs.audit import (
    compare_presidente,
    join_key,
    results_to_frame,
    results_to_votos_frame,
)
from urna_logs.bu_rdv import parse_bu_bytes, parse_rdv_bytes

FIXTURES = Path(__file__).parent / "fixtures"


def test_presidente_bu_rdv_match():
    bu = parse_bu_bytes((FIXTURES / "sample-bu.dat").read_bytes(), source="sample-bu")
    rdv = parse_rdv_bytes((FIXTURES / "sample-rdv.dat").read_bytes(), source="sample-rdv")
    assert bu is not None
    assert rdv is not None
    assert bu.total == rdv.total == 141
    assert bu.votos == rdv.votos

    result = compare_presidente(bu, rdv, stem="sample")
    assert result.ok
    assert result.mismatches == []


def test_presidente_bu_rdv_mismatch():
    bu = parse_bu_bytes((FIXTURES / "sample-bu.dat").read_bytes(), source="sample-bu")
    rdv = parse_rdv_bytes((FIXTURES / "sample-rdv.dat").read_bytes(), source="sample-rdv")
    assert bu is not None and rdv is not None
    # altera um votável do RDV → deve falhar
    key = next(iter(rdv.votos))
    rdv.votos[key] = rdv.votos[key] + 1
    result = compare_presidente(bu, rdv, stem="sample-bad")
    assert result.ok is False
    assert result.mismatches


def test_presidente_only_keys():
    bu = parse_bu_bytes((FIXTURES / "sample-bu.dat").read_bytes())
    assert bu is not None
    # amostra AC seção 88: candidatos 13,14,22,30,55 + branco + nulo
    assert ("nominal", "22") in bu.votos
    assert ("branco", None) in bu.votos
    assert ("nulo", None) in bu.votos


def test_parquet_frames_and_join_key():
    bu = parse_bu_bytes((FIXTURES / "sample-bu.dat").read_bytes())
    rdv = parse_rdv_bytes((FIXTURES / "sample-rdv.dat").read_bytes())
    item = compare_presidente(bu, rdv, stem="sample")
    secoes = results_to_frame([item], "AC", 1)
    votos = results_to_votos_frame([item], "AC", 1)
    assert secoes.loc[0, "join_key"] == join_key("AC", item.municipio, item.zona, item.secao)
    assert secoes.loc[0, "abstencao"] == item.aptos - item.bu_comparecimento
    assert votos["votos_bu"].sum() == 141
    assert set(votos["tipo"]) >= {"nominal", "branco", "nulo"}
