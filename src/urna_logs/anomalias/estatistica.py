"""Testes por seção. Os dois candidatos e as duas caudas entram juntos."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy.stats import binomtest, chisquare

from urna_logs.anomalias.bh import (
    benjamini_hochberg,
    esperados_z,
    p_bicaudal,
    z_por_grupo,
)
from urna_logs.thresholds import (
    BIN_ESPERADO_MIN,
    BIN_PP,
    BIN_RAZAO,
    CANDIDATOS_TURNO,
    FDR_Q,
    MIN_SECOES_LOCAL,
    Z_LIMIAR,
)


def _num(serie: pd.Series) -> pd.Series:
    return pd.to_numeric(serie, errors="coerce")


def preparar(secao: pd.DataFrame, votos: pd.DataFrame) -> pd.DataFrame:
    from urna_logs.anomalias.integridade import _pivot

    base = secao.copy()
    amplo = _pivot(votos)
    if amplo.empty:
        for col in ("votos_13", "votos_22", "branco", "nulo", "outros"):
            base[col] = 0
    else:
        base = base.merge(amplo, on="join_key", how="left")
    for col in ("votos_13", "votos_22", "branco", "nulo", "outros", "aptos", "bu_comparecimento"):
        if col not in base.columns:
            base[col] = np.nan
        base[col] = _num(base[col])
    aptos = base["aptos"]
    comp = base["bu_comparecimento"]
    base["comparecimento"] = comp
    base["pct_comparecimento"] = np.where(aptos > 0, comp / aptos, np.nan)
    sem = _num(base.get("sem_biometria", 0)).fillna(0) + _num(base.get("biografia", 0)).fillna(0)
    base["pct_sem_digital"] = np.where(comp > 0, sem / comp, np.nan)
    for cod in CANDIDATOS_TURNO:
        base[f"p_{cod}"] = np.where(aptos > 0, base[f"votos_{cod}"] / aptos, np.nan)
    base["p_bn"] = np.where(aptos > 0, (base["branco"].fillna(0) + base["nulo"].fillna(0)) / aptos, np.nan)
    base["p_abst"] = np.where(aptos > 0, (aptos - comp) / aptos, np.nan)
    base["p_outros"] = np.where(
        aptos > 0,
        (comp - base["votos_13"].fillna(0) - base["votos_22"].fillna(0) - base["branco"].fillna(0) - base["nulo"].fillna(0)) / aptos,
        np.nan,
    )
    return base


def _alertas_z(df: pd.DataFrame, coluna: str, teste: str, candidato: str = "") -> list[dict]:
    trabalho = df.dropna(subset=[coluna]).copy()
    if trabalho.empty:
        return []
    grupo = ["municipio", "zona", "local"]
    trabalho["z"] = z_por_grupo(trabalho, coluna, grupo, MIN_SECOES_LOCAL)
    trabalho["p"] = trabalho["z"].map(p_bicaudal)
    rejeita, q = benjamini_hochberg(trabalho["p"].to_numpy(), FDR_Q)
    trabalho["q"] = q
    trabalho["rejeita"] = rejeita & (trabalho["z"].abs() > Z_LIMIAR)
    n = int(trabalho["z"].notna().sum())
    esperados = esperados_z(n)
    linhas = []
    for rec in trabalho[trabalho["rejeita"]].to_dict(orient="records"):
        linhas.append(
            {
                "join_key": rec["join_key"],
                "municipio": rec.get("municipio") or 0,
                "zona": rec.get("zona") or 0,
                "secao": rec.get("secao") or 0,
                "local": rec.get("local") or 0,
                "teste": teste,
                "candidato": candidato,
                "observado": rec[coluna],
                "referencia": rec["z"],
                "esperados": esperados,
                "q": rec["q"],
            }
        )
    return linhas


def alertas_z(df: pd.DataFrame) -> list[dict]:
    linhas = _alertas_z(df, "pct_comparecimento", "z_comparecimento")
    linhas.extend(_alertas_z(df, "pct_sem_digital", "sem_digital"))
    for cod in CANDIDATOS_TURNO:
        linhas.extend(_alertas_z(df, f"p_{cod}", "z_candidato", cod))
    return linhas


def _bin(serie: pd.Series) -> pd.Series:
    pct = serie.astype(float) * 100
    bruto = np.floor(np.minimum(pct, 99.999) / BIN_PP) * BIN_PP
    return pd.Series(bruto, index=serie.index)


def fingerprint(
    atual: pd.DataFrame, referencia: pd.DataFrame, candidato: str
) -> tuple[pd.DataFrame, list[dict]]:
    coluna = f"p_{candidato}"
    def _grades(df: pd.DataFrame) -> pd.DataFrame:
        parte = df.dropna(subset=["pct_comparecimento", coluna]).copy()
        parte["bin_comp"] = _bin(parte["pct_comparecimento"])
        parte["bin_share"] = _bin(parte[coluna])
        return parte

    a = _grades(atual)
    r = _grades(referencia)
    if a.empty or r.empty:
        return pd.DataFrame(columns=["bin_comp", "bin_share", "n"]), []
    cont_a = a.groupby(["bin_comp", "bin_share"]).size().rename("n_atual")
    cont_r = r.groupby(["bin_comp", "bin_share"]).size().rename("n_ref")
    grade = pd.concat([cont_a, cont_r], axis=1).fillna(0).reset_index()
    total_ref = grade["n_ref"].sum()
    total_atual = grade["n_atual"].sum()
    grade["esperado"] = np.where(total_ref > 0, grade["n_ref"] / total_ref * total_atual, np.nan)
    grade["razao"] = np.where(grade["esperado"] > 0, grade["n_atual"] / grade["esperado"], np.nan)
    from scipy.stats import poisson

    p = []
    for esp, n in zip(grade["esperado"], grade["n_atual"], strict=False):
        if not np.isfinite(esp) or esp < BIN_ESPERADO_MIN:
            p.append(np.nan)
        else:
            p.append(float(poisson.sf(n - 1, esp)))
    grade["p"] = p
    rejeita, q = benjamini_hochberg(grade["p"].to_numpy(), FDR_Q)
    grade["q"] = q
    grade["alerta"] = rejeita & (grade["razao"] > BIN_RAZAO) & (grade["esperado"] >= BIN_ESPERADO_MIN)
    quentes = set(zip(grade.loc[grade["alerta"], "bin_comp"], grade.loc[grade["alerta"], "bin_share"]))
    linhas = []
    if quentes:
        for rec in a.to_dict(orient="records"):
            chave = (rec["bin_comp"], rec["bin_share"])
            if chave not in quentes:
                continue
            linhas.append(
                {
                    "join_key": rec["join_key"],
                    "municipio": rec.get("municipio") or 0,
                    "zona": rec.get("zona") or 0,
                    "secao": rec.get("secao") or 0,
                    "local": rec.get("local") or 0,
                    "teste": "fingerprint",
                    "candidato": candidato,
                    "observado": rec[coluna],
                    "referencia": rec["pct_comparecimento"],
                    "esperados": float(grade.loc[grade["alerta"], "esperado"].sum()),
                    "q": float(grade.loc[
                        (grade["bin_comp"] == chave[0]) & (grade["bin_share"] == chave[1]), "q"
                    ].iloc[0]),
                }
            )
    grade["candidato"] = candidato
    return grade, linhas


def _ultimo(serie: pd.Series) -> pd.Series:
    valores = pd.to_numeric(serie, errors="coerce").dropna().astype(int)
    return valores % 10


def _segundo(serie: pd.Series) -> pd.Series:
    valores = pd.to_numeric(serie, errors="coerce").dropna().astype(int)
    texto = valores.astype(str)
    return texto[texto.str.len() >= 2].str[1].astype(int)


def _probs_mebane() -> np.ndarray:
    return np.array(
        [sum(math.log10(1 + 1 / (10 * k + d)) for k in range(1, 10)) for d in range(10)]
    )


def alertas_digitos(df: pd.DataFrame, uf: str) -> list[dict]:
    linhas = []
    medidas = {
        "comparecimento": df["comparecimento"],
        "13": df["votos_13"],
        "22": df["votos_22"],
    }
    familia_p = []
    familia_meta = []
    for nome, serie in medidas.items():
        dig = _ultimo(serie)
        if len(dig) < 20:
            continue
        contagem = np.bincount(dig.to_numpy(), minlength=10).astype(float)
        chi, p = chisquare(contagem)
        familia_p.append(p)
        familia_meta.append((nome, "ultimo_digito", chi, p, len(dig)))
        k = int((dig == 0).sum())
        p_redondo = float(binomtest(k, len(dig), 0.1).pvalue)
        familia_p.append(p_redondo)
        familia_meta.append((nome, "numero_redondo", k / len(dig), p_redondo, len(dig)))
    if familia_p:
        rejeita, q = benjamini_hochberg(np.array(familia_p), FDR_Q)
        for (nome, teste, obs, _p, n), fica, qq in zip(familia_meta, rejeita, q, strict=False):
            if not fica:
                continue
            linhas.append(
                {
                    "join_key": "",
                    "municipio": 0,
                    "zona": 0,
                    "secao": 0,
                    "local": 0,
                    "teste": teste,
                    "candidato": "" if nome == "comparecimento" else nome,
                    "observado": obs,
                    "referencia": n,
                    "esperados": n / 10,
                    "q": qq,
                    "uf": uf,
                }
            )
    probs = _probs_mebane()
    for nome, serie in medidas.items():
        dig = _segundo(serie)
        if len(dig) < 20:
            continue
        contagem = np.bincount(dig.to_numpy(), minlength=10).astype(float)
        esperado = probs * contagem.sum()
        chi, p = chisquare(contagem, esperado)
        if p >= FDR_Q:
            continue
        linhas.append(
            {
                "join_key": "",
                "municipio": 0,
                "zona": 0,
                "secao": 0,
                "local": 0,
                "teste": "mebane",
                "candidato": "" if nome == "comparecimento" else nome,
                "observado": chi,
                "referencia": p,
                "esperados": FDR_Q,
                "q": p,
                "uf": uf,
            }
        )
    return linhas


def residuos_padronizados(
    df: pd.DataFrame, y: str, xs: list[str], por: list[str]
) -> pd.Series:
    """Resíduo / desvio, depois do efeito fixo em `por`. As duas caudas ficam no sinal."""
    cols = [y, *xs]
    trabalho = df.dropna(subset=cols + por).copy()
    vazio = pd.Series(np.nan, index=df.index)
    if len(trabalho) < len(xs) + 8:
        return vazio
    for col in cols:
        trabalho[col] = trabalho[col] - trabalho.groupby(por)[col].transform("mean")
    matriz = trabalho[xs].to_numpy(dtype=float)
    alvo = trabalho[y].to_numpy(dtype=float)
    coef, *_ = np.linalg.lstsq(matriz, alvo, rcond=None)
    residuo = alvo - matriz @ coef
    sigma = float(residuo.std(ddof=min(len(xs), len(residuo) - 1)))
    if not sigma:
        return vazio
    vazio.loc[trabalho.index] = residuo / sigma
    return vazio


def alertas_regressao(primeiro: pd.DataFrame, segundo: pd.DataFrame) -> tuple[list[dict], str]:
    chaves = ["join_key", "municipio", "zona", "secao", "local"]
    esq = primeiro[chaves + ["p_13", "p_22", "p_outros", "p_bn", "p_abst"]].copy()
    direita = segundo[["join_key", "p_13", "p_22"]].copy()
    esq = esq.rename(columns={c: f"{c}_1" for c in esq.columns if c != "join_key"})
    direita = direita.rename(columns={c: f"{c}_2" for c in direita.columns if c != "join_key"})
    junto = esq.merge(direita, on="join_key", how="inner")
    for col in ("municipio", "zona", "secao", "local"):
        if f"{col}_1" in junto.columns:
            junto[col] = junto[f"{col}_1"]
    if junto.empty:
        return [], ""
    linhas: list[dict] = []
    notas: list[str] = []
    for cod in CANDIDATOS_TURNO:
        y = f"p_{cod}_2"
        xs = [f"p_{cod}_1", "p_outros_1", "p_bn_1", "p_abst_1"]
        z = residuos_padronizados(junto, y, xs, ["municipio"])
        z_local = residuos_padronizados(junto, y, xs, ["municipio", "local"])
        p = z.map(p_bicaudal).to_numpy()
        rejeita, q = benjamini_hochberg(p, FDR_Q)
        fica = rejeita & (z.abs().to_numpy() > Z_LIMIAR)
        n = int(np.isfinite(z.to_numpy(dtype=float)).sum())
        esperados = esperados_z(n)
        mantem = int(np.nansum(fica & (z_local.abs().to_numpy() > Z_LIMIAR)))
        notas.append(f"{cod}: efeito fixo de local mantém {mantem} de {int(fica.sum())}")
        pos = np.flatnonzero(fica)
        for i in pos:
            rec = junto.iloc[i]
            linhas.append(
                {
                    "join_key": rec["join_key"],
                    "municipio": rec.get("municipio") or 0,
                    "zona": rec.get("zona") or 0,
                    "secao": rec.get("secao") or 0,
                    "local": rec.get("local") or 0,
                    "teste": "residuo_2t",
                    "candidato": cod,
                    "observado": rec[y],
                    "referencia": float(z.iloc[i]),
                    "esperados": esperados,
                    "q": float(q[i]),
                }
            )
    return linhas, "; ".join(notas)
