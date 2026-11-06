"""A frase da urna sai do boletim e do log, não do nome do município."""

from pathlib import Path

import pytest

from urna_logs.config import zip_path
from urna_logs.identidade_bu import (
    complemento_pacote,
    identidade_boletim,
    motivo_trio,
)
from urna_logs.verificar_vsc import pacote_das_falhas

FIXTURES = Path(__file__).parent / "fixtures"


def test_boletim_de_secao_e_geracao_do_rdv_no_log():
    frase = complemento_pacote(
        ["rdv.dat"],
        {
            "tipo_urna": "secao",
            "tipo_arquivo": "votacaoUE",
            "bloco": "dadosSecao",
            "fase": "oficial",
            "motivo": None,
        },
        [
            "Gerando arquivo de resultado [rdv.dat] + [Início]",
            "Gerando arquivo de resultado [rdv.dat] + [Término]",
            "Solicitação ao INIT para executar o aplicativo - SISTEMA DE AUTOTESTE",
        ],
    )
    assert "urna de seção" in frase
    assert "votação da urna" in frase
    assert "bloco de seção" in frase
    assert "fase oficial" in frase
    assert "até o término" in frase
    assert "não contém as frases de procedimento de contingência" in frase
    assert "Lagoa" not in frase
    assert "Guarulhos" not in frase


def test_boletim_de_contingencia_quando_o_arquivo_declara():
    frase = complemento_pacote(
        ["log.jez"],
        {
            "tipo_urna": "contingencia",
            "tipo_arquivo": "votacaoUE",
            "bloco": "dadosSecao",
            "fase": "oficial",
            "motivo": None,
        },
        None,
    )
    assert "urna de contingência" in frase
    assert "até o término" not in frase
    assert "não contém as frases" not in frase


def test_motivo_de_apuracao_entra_quando_o_boletim_traz():
    frase = complemento_pacote(
        [],
        {
            "tipo_urna": "contingencia",
            "tipo_arquivo": "saMistaBUImpressoCedula",
            "bloco": "dadosSA",
            "fase": "oficial",
            "motivo": "apuração mista com boletim, mista com boletim, urna encerrada com eleitores na fila",
        },
        ["Início do procedimento de contingência"],
    )
    assert "sistema de apuração mista com boletim impresso" in frase
    assert "bloco do sistema de apuração" in frase
    assert "eleitores na fila" in frase
    assert "contém 1 frase de procedimento de contingência" in frase


def test_sem_rdv_no_pacote_nao_trata_zero_como_divergencia():
    from urna_logs.verificar_vsc import _texto_votacao

    chave = "MA:07846:0074:0228"
    votos = {chave: {"13": 158, "22": 52, "branco": 2, "nulo": 4, "bu_rdv": False}}
    secoes = {chave: {"comparecimento": 219, "aptos": 295}}
    texto = _texto_votacao(chave, votos, secoes, rdv_no_pacote=False)
    assert "divergem" not in texto
    assert "não está no pacote" in texto


def test_motivo_trio_separa_arquivo_ausente_de_hash():
    assert "Falta rdv.dat" in motivo_trio("bu.dat=ok;rdv.dat=ausente_pacote;log.jez=ok", 0)
    assert motivo_trio("bu.dat=hash_fail", 1).startswith("O SHA-512")


def test_fixture_de_boletim_declara_um_tipo():
    info = identidade_boletim((FIXTURES / "sample-bu.dat").read_bytes())
    assert info["tipo_urna"]
    assert info["bloco"] in {"dadosSecao", "dadosSA"}


@pytest.mark.skipif(not zip_path("MA", 1).exists(), reason="ZIP do MA 1º turno ausente")
def test_ma_rdv_ausente_le_secao_no_boletim():
    frase = pacote_das_falhas("MA", 1, {"o03220ma0784600740228": ["rdv.dat"]})
    texto = frase["o03220ma0784600740228"][1]
    assert "urna de seção" in texto
    assert "até o término" in texto
    assert "não contém as frases de procedimento de contingência" in texto


@pytest.mark.skipif(not zip_path("SP", 2).exists(), reason="ZIP do SP 2º turno ausente")
def test_sp_log_ausente_le_secao_no_boletim():
    frase = pacote_das_falhas("SP", 2, {"o03221sp6477703950298": ["log.jez"]})
    texto = frase["o03221sp6477703950298"][1]
    assert "urna de seção" in texto
    assert "até o término" not in texto
    assert "procedimento de contingência" not in texto
