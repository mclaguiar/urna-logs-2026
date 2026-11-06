"""Benjamini-Hochberg e cauda normal. Limiares vêm de urna_logs.thresholds."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from urna_logs.thresholds import FDR_Q, MAD_ESCALA, Z_LIMIAR


def norm_sf(z: float) -> float:
    return 0.5 * math.erfc(float(z) / math.sqrt(2.0))


def p_bicaudal(z: float) -> float:
    if z is None or (isinstance(z, float) and math.isnan(z)):
        return math.nan
    return min(1.0, 2.0 * norm_sf(abs(float(z))))


def esperados_z(n: int, limiar: float = Z_LIMIAR) -> float:
    if n <= 0:
        return 0.0
    return n * 2.0 * norm_sf(limiar)


def benjamini_hochberg(pvalues: np.ndarray, alpha: float = FDR_Q) -> tuple[np.ndarray, np.ndarray]:
    """Devolve (rejeita, q) na ordem original. NaN não entra na família."""
    p = np.asarray(pvalues, dtype=float)
    n = len(p)
    rejeita = np.zeros(n, dtype=bool)
    q = np.full(n, np.nan)
    ok = np.isfinite(p)
    if not ok.any():
        return rejeita, q
    idx = np.flatnonzero(ok)
    pp = p[idx]
    m = len(pp)
    order = np.argsort(pp)
    ranked = pp[order]
    thresh = alpha * (np.arange(1, m + 1) / m)
    below = ranked <= thresh
    if below.any():
        corte = ranked[np.max(np.where(below))]
        rejeita[idx] = pp <= corte + 1e-15
    ranks = np.empty(m, dtype=float)
    ranks[order] = np.arange(1, m + 1)
    qq = pp * m / ranks
    qq_ord = qq[order]
    qq_ord = np.minimum.accumulate(qq_ord[::-1])[::-1]
    q_ok = np.empty(m)
    q_ok[order] = np.clip(qq_ord, 0, 1)
    q[idx] = q_ok
    return rejeita, q


def z_robusto(serie: pd.Series) -> pd.Series:
    """z = 0,6745 * (x − mediana) / MAD. MAD nulo não produz número."""
    if serie.notna().sum() == 0:
        return pd.Series(np.nan, index=serie.index)
    med = serie.median()
    mad = (serie - med).abs().median()
    if mad == 0 or pd.isna(mad):
        return pd.Series(np.nan, index=serie.index)
    return MAD_ESCALA * (serie - med) / mad


def z_por_grupo(df: pd.DataFrame, valor: str, grupo: list[str], minimo: int) -> pd.Series:
    def _um(s: pd.Series) -> pd.Series:
        if s.notna().sum() < minimo:
            return pd.Series(np.nan, index=s.index)
        return z_robusto(s)

    return df.groupby(grupo, dropna=False)[valor].transform(_um)
