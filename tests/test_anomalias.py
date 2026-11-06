"""Limiares, parsers de amostra e as duas caudas. Sem rede e sem ZIP."""

from pathlib import Path

import numpy as np
import pandas as pd

from urna_logs.anomalias.bh import benjamini_hochberg, z_robusto
from urna_logs.anomalias.estatistica import residuos_padronizados
from urna_logs.anomalias.integridade import escolher_amostra, tipos_audit, tipos_vsc
from urna_logs.anomalias.logs import alerta_intervalo, sequencia_curta
from urna_logs.bu_rdv import parse_bu_bytes, parse_rdv_bytes
from urna_logs.parse_log import parse_line

FIXTURES = Path(__file__).parent / "fixtures"


def test_escolhe_nome_2022_e_2026():
    novo = escolher_amostra(
        [
            "o00406-0111200060046.imgbu",
            "o00406-0111200060046.bu",
            "o00406-0111200060046.rdv",
            "o00406-0111200060046.vscmr",
            "o00406-0111200060046.logjez",
        ]
    )
    assert novo["bu"].endswith(".bu") and not novo["bu"].endswith(".imgbu")
    assert novo["vsc"].endswith(".vscmr")
    velho = escolher_amostra(["o03220ac0101500020088-bu.dat", "o03220ac0101500020088-vota.vsc"])
    assert velho["bu"].endswith("-bu.dat")
    assert velho["vsc"].endswith("-vota.vsc")


def test_bu_rdv_amostra():
    bu = parse_bu_bytes((FIXTURES / "sample-bu.dat").read_bytes())
    rdv = parse_rdv_bytes((FIXTURES / "sample-rdv.dat").read_bytes())
    assert bu is not None and rdv is not None
    assert bu.total == rdv.total
    assert hasattr(bu, "encerramento")


def test_log_amostra_tem_voto_computado():
    texto = (FIXTURES / "sample-log.txt").read_text(encoding="latin-1")
    eventos = [parse_line(linha) for linha in texto.splitlines()]
    mensagens = [ev.mensagem for ev in eventos if ev]
    assert "O voto do eleitor foi computado" in mensagens
    assert any(ev.dt is not None for ev in eventos if ev)


def test_intervalo_19_nao_alerta_20_alerta():
    assert sequencia_curta([1.0] * 19) == 19
    assert alerta_intervalo([1.0] * 19) is False
    assert alerta_intervalo([1.0] * 20) is True
    assert alerta_intervalo([1.0] * 19 + [5.0] + [1.0] * 19) is False


def test_mad_zero_nao_gera_z():
    z = z_robusto(pd.Series([3, 3, 3, 3]))
    assert z.isna().all()


def test_bh_rejeita_so_o_menor():
    rejeita, q = benjamini_hochberg(np.array([0.001, 0.04, 0.2]), alpha=0.05)
    assert rejeita[0]
    assert not rejeita[2]
    assert q[0] < q[2]


def test_residuo_tem_as_duas_caudas():
    mun = np.repeat([1, 2], 12)
    base = np.tile(np.linspace(0.2, 0.8, 12), 2)
    y = base.copy()
    y[0] = 0.99
    y[1] = 0.01
    df = pd.DataFrame({"municipio": mun, "y": y, "x": base})
    z = residuos_padronizados(df, "y", ["x"], ["municipio"])
    assert z.iloc[0] > 0
    assert z.iloc[1] < 0


def test_vsc_separa_arquivo_de_assinatura():
    assert tipos_vsc({"tem_vsc": False, "parse_ok": False, "erro": "sem_vota.vsc"}) == ["arquivo_ausente"]
    assert tipos_vsc({"tem_vsc": True, "parse_ok": False, "erro": "parse: boom"}) == ["arquivo_corrompido"]
    assert "assinatura_invalida" not in tipos_vsc(
        {"tem_vsc": True, "parse_ok": True, "hw_sig_ok": False, "hw_cadeia": "pendente", "n_hash_fail": 0}
    )
    assert tipos_vsc(
        {"tem_vsc": True, "parse_ok": True, "hw_sig_ok": False, "hw_cadeia": "falha", "n_hash_fail": 0}
    ) == ["assinatura_invalida"]
    assert tipos_audit({"ok": False, "error": "", "mismatches": "total"}) == ["bu_rdv"]
    assert tipos_audit({"ok": False, "error": "RDV ausente ou sem presidente"}) == ["arquivo_ausente"]
