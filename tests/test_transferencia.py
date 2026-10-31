"""Balanceamento das margens e soma das transferências. Não chama o R."""

import pandas as pd

from urna_logs.transferencia import (
    _nota_grao,
    fonte_por_municipio,
    montar_margens,
    somar_fluxos,
    taxas_pais,
)


def _comparar() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "status": "ambos",
                "join_key": "AC:00001:0001:0001",
                "municipio": 1,
                "zona": 1,
                "secao": 1,
                "votos_fa_1t": 10,
                "votos_fb_1t": 0,
                "votos_eliminados_1t": 0,
                "branco_1t": 0,
                "nulo_1t": 0,
                "abstencao_1t": 0,
                "votos_fa_2t": 8,
                "votos_fb_2t": 0,
                "branco_2t": 0,
                "nulo_2t": 0,
                "abstencao_2t": 0,
            },
            {
                "status": "ambos",
                "join_key": "AC:00002:0001:0001",
                "municipio": 2,
                "zona": 1,
                "secao": 1,
                "votos_fa_1t": 0,
                "votos_fb_1t": 40,
                "votos_eliminados_1t": 0,
                "branco_1t": 0,
                "nulo_1t": 0,
                "abstencao_1t": 0,
                "votos_fa_2t": 0,
                "votos_fb_2t": 40,
                "branco_2t": 0,
                "nulo_2t": 0,
                "abstencao_2t": 0,
            },
        ]
    )


def test_montar_margens_fecha_na_abstencao():
    margens = montar_margens(_comparar())
    primeira = margens.loc[margens["municipio"] == 1].iloc[0]
    assert primeira["o_13"] == 10
    assert primeira["d_13"] == 8
    assert primeira["d_abstencao"] == 2
    assert primeira["n"] == 10


def test_cidade_pequena_herda_o_estado():
    fonte = fonte_por_municipio(pd.Series({1: 10, 2: 40}), min_secoes=30)
    assert fonte.loc[1] == "estado"
    assert fonte.loc[2] == "municipio"


def test_soma_usa_a_taxa_da_cidade_grande_e_a_do_estado_na_pequena():
    margens = montar_margens(_comparar())
    linhas = []
    for modelo in ("brown_payne", "lphom"):
        linhas.append(
            {
                "nivel": "estado",
                "municipio": "",
                "modelo": modelo,
                "origem": "13",
                "destino": "13",
                "taxa": 0.5,
                "n_secoes": 2,
                "r2": 0.9,
                "convergencia": 0,
                "min_secoes": 30,
            }
        )
        linhas.append(
            {
                "nivel": "municipio",
                "municipio": "2",
                "modelo": modelo,
                "origem": "22",
                "destino": "22",
                "taxa": 1.0,
                "n_secoes": 1,
                "r2": 1.0,
                "convergencia": 0,
                "min_secoes": 30,
            }
        )
        for origem in ("13", "22", "eliminados", "branco", "nulo", "abstencao"):
            for destino in ("13", "22", "branco", "nulo", "abstencao"):
                if origem == "13" and destino == "13":
                    continue
                if origem == "22" and destino == "22":
                    continue
                linhas.append(
                    {
                        "nivel": "estado",
                        "municipio": "",
                        "modelo": modelo,
                        "origem": origem,
                        "destino": destino,
                        "taxa": 0.0 if destino != "abstencao" else 1.0,
                        "n_secoes": 2,
                        "r2": 0.9,
                        "convergencia": 0,
                        "min_secoes": 30,
                    }
                )
    taxas = pd.DataFrame(linhas)
    soma = somar_fluxos(margens, taxas)
    ficou = soma.loc[
        (soma["modelo"] == "brown_payne")
        & (soma["origem"] == "13")
        & (soma["destino"] == "13")
    ].iloc[0]
    assert ficou["taxa"] == 0.5


def test_pais_soma_votos_e_nao_a_media_das_taxas():
    def bloco(uf: str, fica: float, sai: float) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "uf": uf,
                    "nivel": "estado_soma",
                    "modelo": "brown_payne",
                    "origem": "13",
                    "destino": "13",
                    "votos": fica,
                    "taxa": fica / (fica + sai),
                },
                {
                    "uf": uf,
                    "nivel": "estado_soma",
                    "modelo": "brown_payne",
                    "origem": "13",
                    "destino": "22",
                    "votos": sai,
                    "taxa": sai / (fica + sai),
                },
            ]
        )

    pais = taxas_pais([bloco("AC", 90, 10), bloco("SP", 10, 190)])
    taxa = pais.loc[
        (pais["origem"] == "13") & (pais["destino"] == "13"), "taxa"
    ].iloc[0]
    assert abs(taxa - (100 / 300)) < 1e-9


def _taxas_com_se(municipio: str, se: float, min_secoes: int) -> list[dict]:
    linhas = []
    for origem in ("13", "22", "eliminados", "branco", "nulo", "abstencao"):
        for destino in ("13", "22", "branco", "nulo", "abstencao"):
            linhas.append(
                {
                    "nivel": "municipio",
                    "municipio": municipio,
                    "modelo": "brown_payne",
                    "origem": origem,
                    "destino": destino,
                    "taxa": 0.8 if destino == "13" else 0.05,
                    "se": se,
                    "n_secoes": 1,
                    "r2": 0.9,
                    "convergencia": 0,
                    "min_secoes": min_secoes,
                }
            )
    return linhas


def test_se_de_cidades_com_matriz_propria_nao_se_soma_como_o_mesmo_ajuste():
    margens = montar_margens(_comparar())
    # Cada cidade tem uma seção. min_secoes=1 faz as duas estimarem a própria matriz.
    linhas = _taxas_com_se("1", 0.10, 1) + _taxas_com_se("2", 0.0, 1)
    margens = margens.copy()
    margens["o_13"] = 100
    soma = somar_fluxos(margens, pd.DataFrame(linhas))
    se = soma.loc[
        (soma["modelo"] == "brown_payne")
        & (soma["origem"] == "13")
        & (soma["destino"] == "13"),
        "se",
    ].iloc[0]
    assert abs(se - 0.05) < 1e-9


def test_se_herdado_do_estado_entra_uma_vez():
    margens = montar_margens(_comparar())
    margens = margens.copy()
    margens["o_13"] = 100
    linhas = []
    for origem in ("13", "22", "eliminados", "branco", "nulo", "abstencao"):
        for destino in ("13", "22", "branco", "nulo", "abstencao"):
            linhas.append(
                {
                    "nivel": "estado",
                    "municipio": "",
                    "modelo": "brown_payne",
                    "origem": origem,
                    "destino": destino,
                    "taxa": 0.8 if destino == "13" else 0.05,
                    "se": 0.10,
                    "n_secoes": 2,
                    "r2": 0.9,
                    "convergencia": 0,
                    "min_secoes": 30,
                }
            )
    soma = somar_fluxos(margens, pd.DataFrame(linhas))
    se = soma.loc[
        (soma["modelo"] == "brown_payne")
        & (soma["origem"] == "13")
        & (soma["destino"] == "13"),
        "se",
    ].iloc[0]
    assert abs(se - 0.10) < 1e-9


def test_nota_diz_quando_o_lphom_sai_da_secao():
    taxas = pd.DataFrame(
        [
            {
                "nivel": "estado",
                "municipio": "",
                "modelo": "lphom",
                "grao": "zona",
                "n_unidades": 107,
                "n_secoes": 7101,
            },
            {
                "nivel": "municipio",
                "municipio": "2704302",
                "modelo": "lphom",
                "grao": "zona",
                "n_unidades": 5,
                "n_secoes": 1661,
            },
            {
                "nivel": "municipio",
                "municipio": "2700102",
                "modelo": "lphom",
                "grao": "secao",
                "n_unidades": 40,
                "n_secoes": 40,
            },
        ]
    )
    texto = _nota_grao(taxas)
    assert "usou zona: 107 linhas, 7101 seções" in texto
    assert "2704302 (zona, 5 linhas, 1661 seções)" in texto
    assert "2700102" not in texto
