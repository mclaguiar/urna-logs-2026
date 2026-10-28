"""Comparativo 1º × 2º turno seção a seção: abstenção, votos, sem digital, pós-17h."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.table import Table

from urna_logs.config import REPORTS_DIR, ensure_dirs
from urna_logs.thresholds import (
    P_FLAG_ABST,
    P_FLAG_MARGEM,
    P_FLAG_POS17,
    P_FLAG_SEM_DIG,
)

console = Console()

COMPARE_COLS = [
    "uf",
    "join_key",
    "municipio",
    "zona",
    "secao",
    "aptos_1t",
    "aptos_2t",
    "comparecimento_1t",
    "comparecimento_2t",
    "abstencao_1t",
    "abstencao_2t",
    "delta_comparecimento",
    "delta_abstencao",
    "pct_abstencao_1t",
    "pct_abstencao_2t",
    "bu_total_1t",
    "bu_total_2t",
    "sem_digital_1t",
    "sem_digital_2t",
    "pct_sem_digital_1t",
    "pct_sem_digital_2t",
    "delta_pct_sem_digital",
    "votos_fa_1t",
    "votos_fa_2t",
    "votos_fb_1t",
    "votos_fb_2t",
    "margem_1t",
    "margem_2t",
    "delta_margem",
    "votos_eliminados_1t",
    "branco_1t",
    "branco_2t",
    "delta_branco",
    "nulo_1t",
    "nulo_2t",
    "delta_nulo",
    "ganho_finalistas",
    "gap_transferencia",
    "pct_apos_17h_1t",
    "pct_apos_17h_2t",
    "delta_pct_apos_17h_secao",
    "flag_abstencao",
    "flag_margem",
    "flag_sem_digital_x_margem",
    "flag_pos17",
    "flag_so_turno",
    "flags",
    "status",  # ambos | so_1t | so_2t | pendente_2t
]


def audit_secoes_path(uf: str, turno: int) -> Path:
    return REPORTS_DIR / f"audit_presidente_{uf.upper()}_{turno}t.parquet"


def audit_votos_path(uf: str, turno: int) -> Path:
    return REPORTS_DIR / f"audit_presidente_votos_{uf.upper()}_{turno}t.parquet"


def horario_summary_path(uf: str, turno: int) -> Path:
    return REPORTS_DIR / f"horario_summary_{uf.upper()}_{turno}t.csv"


def horario_secao_path(uf: str, turno: int) -> Path:
    return REPORTS_DIR / f"horario_secao_{uf.upper()}_{turno}t.parquet"


def load_secoes(uf: str, turno: int) -> pd.DataFrame | None:
    path = audit_secoes_path(uf, turno)
    if not path.exists():
        return None
    cols = [
        "join_key",
        "municipio",
        "zona",
        "secao",
        "aptos",
        "bu_comparecimento",
        "abstencao",
        "pct_abstencao",
        "bu_total",
        "ok",
        "biografia",
        "sem_biometria",
        "bio",
    ]
    df = pd.read_parquet(path)
    keep = [c for c in cols if c in df.columns]
    out = df[keep].copy()
    if "biografia" in out.columns and "sem_biometria" in out.columns:
        has = (
            out["biografia"].notna()
            | out["sem_biometria"].notna()
            | (out["bio"].notna() if "bio" in out.columns else False)
        )
        out["sem_digital"] = pd.NA
        out.loc[has, "sem_digital"] = (
            out.loc[has, "biografia"].fillna(0) + out.loc[has, "sem_biometria"].fillna(0)
        )
        out["pct_sem_digital"] = pd.NA
        mask = has & out["bu_comparecimento"].fillna(0).gt(0)
        out.loc[mask, "pct_sem_digital"] = (
            100 * out.loc[mask, "sem_digital"] / out.loc[mask, "bu_comparecimento"]
        ).round(4)
    else:
        out["sem_digital"] = pd.NA
        out["pct_sem_digital"] = pd.NA
    return out


def load_votos(uf: str, turno: int) -> pd.DataFrame | None:
    path = audit_votos_path(uf, turno)
    if not path.exists():
        return None
    return pd.read_parquet(path)


def load_horario_secao(uf: str, turno: int) -> pd.DataFrame | None:
    path = horario_secao_path(uf, turno)
    if not path.exists():
        return None
    df = pd.read_parquet(path)
    keep = [c for c in ("join_key", "hab_total", "hab_apos_17h", "pct_apos_17h") if c in df.columns]
    return df[keep].copy()


def pct_apos_17h_uf(uf: str, turno: int) -> float | None:
    """% ≥17h da UF: summary CSV; senão agrega horario_secao (hab)."""
    hp = horario_summary_path(uf, turno)
    if hp.exists():
        row = pd.read_csv(hp).iloc[0]
        val = row.get("pct_apos_17h")
        return float(val) if pd.notna(val) else None
    secao = load_horario_secao(uf, turno)
    if secao is None or secao.empty:
        return None
    if "hab_total" not in secao.columns or "hab_apos_17h" not in secao.columns:
        return None
    total = float(pd.to_numeric(secao["hab_total"], errors="coerce").fillna(0).sum())
    apos = float(pd.to_numeric(secao["hab_apos_17h"], errors="coerce").fillna(0).sum())
    if total <= 0:
        return None
    return round(100.0 * apos / total, 4)


def discover_finalistas(votos_2t: pd.DataFrame) -> list[str]:
    """Números nominais presentes no 2º turno (ordenados)."""
    nom = votos_2t[votos_2t["tipo"].astype(str).str.lower() == "nominal"].copy()
    nums = (
        nom["numero"]
        .dropna()
        .astype(str)
        .str.replace(r"\.0$", "", regex=True)
        .unique()
        .tolist()
    )
    return sorted(nums, key=lambda x: int(x) if str(x).isdigit() else str(x))


def pivot_votos_secao(
    votos: pd.DataFrame, finalistas: list[str]
) -> pd.DataFrame:
    """Uma linha por join_key com votos dos finalistas, eliminados, branco, nulo."""
    df = votos.copy()
    df["numero"] = (
        df["numero"]
        .astype(str)
        .str.replace(r"\.0$", "", regex=True)
        .replace({"nan": None, "None": None, "<NA>": None})
    )
    df.loc[df["numero"].isin(["None", "nan", ""]), "numero"] = None
    tipo = df["tipo"].astype(str).str.lower()

    rows: list[dict] = []
    for jk, g in df.groupby("join_key", sort=False):
        t = tipo.loc[g.index]
        nom = g[t == "nominal"]
        fa = fb = elim = branco = nulo = 0
        if len(finalistas) >= 1:
            fa = int(
                nom.loc[
                    nom["numero"].astype(str) == str(finalistas[0]), "votos_bu"
                ].sum()
            )
        if len(finalistas) >= 2:
            fb = int(
                nom.loc[
                    nom["numero"].astype(str) == str(finalistas[1]), "votos_bu"
                ].sum()
            )
        elim = int(
            nom.loc[~nom["numero"].astype(str).isin([str(x) for x in finalistas]), "votos_bu"].sum()
        )
        branco = int(g.loc[t == "branco", "votos_bu"].sum())
        nulo = int(g.loc[t == "nulo", "votos_bu"].sum())
        rows.append(
            {
                "join_key": jk,
                "votos_fa": fa,
                "votos_fb": fb,
                "votos_eliminados": elim,
                "branco": branco,
                "nulo": nulo,
            }
        )
    return pd.DataFrame(rows) if rows else pd.DataFrame(
        columns=[
            "join_key",
            "votos_fa",
            "votos_fb",
            "votos_eliminados",
            "branco",
            "nulo",
        ]
    )


def empty_compare_frame(uf: str) -> pd.DataFrame:
    return pd.DataFrame(columns=COMPARE_COLS)


def _pct_threshold(series: pd.Series, q: float) -> float | None:
    s = pd.to_numeric(series, errors="coerce").dropna()
    if s.empty:
        return None
    return float(s.quantile(q))


def apply_anomaly_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Flags por percentis da UF (apenas status=ambos quando aplicável)."""
    out = df.copy()
    for col in (
        "flag_abstencao",
        "flag_margem",
        "flag_sem_digital_x_margem",
        "flag_pos17",
        "flag_so_turno",
    ):
        out[col] = False

    ambos = out["status"] == "ambos"
    thr_abst = _pct_threshold(out.loc[ambos, "delta_abstencao"].abs(), P_FLAG_ABST)
    thr_marg = _pct_threshold(out.loc[ambos, "delta_margem"].abs(), P_FLAG_MARGEM)
    thr_sd = _pct_threshold(out.loc[ambos, "pct_sem_digital_1t"], P_FLAG_SEM_DIG)
    thr_pos = _pct_threshold(out.loc[ambos, "pct_apos_17h_2t"], P_FLAG_POS17)
    thr_dpos = _pct_threshold(
        out.loc[ambos, "delta_pct_apos_17h_secao"].abs(), P_FLAG_POS17
    )

    if thr_abst is not None and thr_abst > 0:
        out.loc[
            ambos & (out["delta_abstencao"].abs() >= thr_abst), "flag_abstencao"
        ] = True
    if thr_marg is not None and thr_marg > 0:
        out.loc[ambos & (out["delta_margem"].abs() >= thr_marg), "flag_margem"] = True
    if thr_sd is not None and thr_marg is not None and thr_marg > 0:
        out.loc[
            ambos
            & (out["pct_sem_digital_1t"] >= thr_sd)
            & (out["delta_margem"].abs() >= thr_marg),
            "flag_sem_digital_x_margem",
        ] = True
    # Evita marcar todas as seções quando a série é constante (p90 == max == min)
    if thr_pos is not None:
        series_pos = pd.to_numeric(out.loc[ambos, "pct_apos_17h_2t"], errors="coerce")
        if series_pos.nunique(dropna=True) > 1:
            out.loc[
                ambos & (out["pct_apos_17h_2t"] >= thr_pos), "flag_pos17"
            ] = True
    if thr_dpos is not None and thr_dpos > 0:
        out.loc[
            ambos & (out["delta_pct_apos_17h_secao"].abs() >= thr_dpos), "flag_pos17"
        ] = True

    out["flag_so_turno"] = out["status"].isin(["so_1t", "so_2t"])

    def _flags_row(r: pd.Series) -> str:
        names = []
        if r["flag_abstencao"]:
            names.append("abstencao")
        if r["flag_margem"]:
            names.append("margem")
        if r["flag_sem_digital_x_margem"]:
            names.append("sem_digital_x_margem")
        if r["flag_pos17"]:
            names.append("pos17")
        if r["flag_so_turno"]:
            names.append("so_turno")
        return "|".join(names)

    out["flags"] = out.apply(_flags_row, axis=1)
    return out


def enrich_with_votos(
    merged: pd.DataFrame, uf: str, turno_a: int, turno_b: int, meta: dict
) -> pd.DataFrame:
    v1 = load_votos(uf, turno_a)
    v2 = load_votos(uf, turno_b)
    if v2 is None:
        meta["finalistas"] = ""
        meta["votos_disponiveis"] = False
        return merged

    finalistas = discover_finalistas(v2)
    meta["finalistas"] = ",".join(finalistas)
    meta["votos_disponiveis"] = True
    meta["finalista_a"] = finalistas[0] if finalistas else None
    meta["finalista_b"] = finalistas[1] if len(finalistas) > 1 else None

    p2 = pivot_votos_secao(v2, finalistas).rename(
        columns={
            "votos_fa": "votos_fa_2t",
            "votos_fb": "votos_fb_2t",
            "votos_eliminados": "votos_eliminados_2t",
            "branco": "branco_2t",
            "nulo": "nulo_2t",
        }
    )
    if v1 is not None:
        p1 = pivot_votos_secao(v1, finalistas).rename(
            columns={
                "votos_fa": "votos_fa_1t",
                "votos_fb": "votos_fb_1t",
                "votos_eliminados": "votos_eliminados_1t",
                "branco": "branco_1t",
                "nulo": "nulo_1t",
            }
        )
    else:
        p1 = pd.DataFrame(
            columns=[
                "join_key",
                "votos_fa_1t",
                "votos_fb_1t",
                "votos_eliminados_1t",
                "branco_1t",
                "nulo_1t",
            ]
        )

    out = merged.merge(p1, on="join_key", how="left").merge(p2, on="join_key", how="left")
    for c in (
        "votos_fa_1t",
        "votos_fb_1t",
        "votos_fa_2t",
        "votos_fb_2t",
        "votos_eliminados_1t",
        "branco_1t",
        "branco_2t",
        "nulo_1t",
        "nulo_2t",
    ):
        if c not in out.columns:
            out[c] = pd.NA

    out["margem_1t"] = out["votos_fa_1t"] - out["votos_fb_1t"]
    out["margem_2t"] = out["votos_fa_2t"] - out["votos_fb_2t"]
    out["delta_margem"] = out["margem_2t"] - out["margem_1t"]
    out["delta_branco"] = out["branco_2t"] - out["branco_1t"]
    out["delta_nulo"] = out["nulo_2t"] - out["nulo_1t"]
    fin_1 = out["votos_fa_1t"].fillna(0) + out["votos_fb_1t"].fillna(0)
    fin_2 = out["votos_fa_2t"].fillna(0) + out["votos_fb_2t"].fillna(0)
    out["ganho_finalistas"] = fin_2 - fin_1
    # eliminados_1t ≈ ganho_finalistas − Δ comparecimento  → gap residual
    out["gap_transferencia"] = (
        out["votos_eliminados_1t"].fillna(0)
        - (out["ganho_finalistas"] - out["delta_comparecimento"].fillna(0))
    )
    return out


def enrich_with_horario_secao(
    merged: pd.DataFrame, uf: str, turno_a: int, turno_b: int
) -> pd.DataFrame:
    h1 = load_horario_secao(uf, turno_a)
    h2 = load_horario_secao(uf, turno_b)
    out = merged
    if h1 is not None:
        out = out.merge(
            h1.rename(
                columns={
                    "pct_apos_17h": "pct_apos_17h_1t",
                    "hab_total": "hab_total_1t",
                    "hab_apos_17h": "hab_apos_17h_1t",
                }
            )[["join_key", "pct_apos_17h_1t"]],
            on="join_key",
            how="left",
        )
    else:
        out["pct_apos_17h_1t"] = pd.NA
    if h2 is not None:
        out = out.merge(
            h2.rename(
                columns={
                    "pct_apos_17h": "pct_apos_17h_2t",
                    "hab_total": "hab_total_2t",
                    "hab_apos_17h": "hab_apos_17h_2t",
                }
            )[["join_key", "pct_apos_17h_2t"]],
            on="join_key",
            how="left",
        )
    else:
        out["pct_apos_17h_2t"] = pd.NA
    out["delta_pct_apos_17h_secao"] = out["pct_apos_17h_2t"] - out["pct_apos_17h_1t"]
    return out


def build_compare(uf: str, turno_a: int, turno_b: int) -> tuple[pd.DataFrame, dict]:
    """Monta frame seção a seção. Se turno_b ausente, status=pendente_2t."""
    uf = uf.upper()
    a = load_secoes(uf, turno_a)
    b = load_secoes(uf, turno_b)

    meta: dict = {
        "uf": uf,
        "turno_a": turno_a,
        "turno_b": turno_b,
        "turno_a_disponivel": a is not None,
        "turno_b_disponivel": b is not None,
        "secoes_1t": int(len(a)) if a is not None else 0,
        "secoes_2t": int(len(b)) if b is not None else 0,
        "secoes_ambos": 0,
        "secoes_so_1t": 0,
        "secoes_so_2t": 0,
        "horario_1t_pct_apos_17h": None,
        "horario_2t_pct_apos_17h": None,
        "delta_pct_apos_17h": None,
        "finalistas": "",
        "finalista_a": None,
        "finalista_b": None,
        "votos_disponiveis": False,
        "n_flag_abstencao": 0,
        "n_flag_margem": 0,
        "n_flag_sem_digital_x_margem": 0,
        "n_flag_pos17": 0,
        "n_flag_so_turno": 0,
        "delta_abstencao_pp": None,
        "delta_comparecimento": None,
        "pct_sem_digital_1t": None,
        "pct_sem_digital_2t": None,
        "delta_pct_sem_digital": None,
        "pronto": False,
        "mensagem": "",
    }

    for label, turno in (("1t", turno_a), ("2t", turno_b)):
        meta[f"horario_{label}_pct_apos_17h"] = pct_apos_17h_uf(uf, turno)

    if meta["horario_1t_pct_apos_17h"] is not None and meta["horario_2t_pct_apos_17h"] is not None:
        meta["delta_pct_apos_17h"] = round(
            meta["horario_2t_pct_apos_17h"] - meta["horario_1t_pct_apos_17h"], 4
        )

    if a is None:
        meta["mensagem"] = f"Falta audit do {turno_a}º turno. Rode `urna-logs audit`."
        return empty_compare_frame(uf), meta

    if b is None:
        meta["mensagem"] = (
            f"{turno_b}º turno ainda não disponível "
            f"(sem `{audit_secoes_path(uf, turno_b).name}`). "
            "Esqueleto gravado; rode de novo quando o CDN publicar."
        )
        out = pd.DataFrame(
            {
                "uf": uf,
                "join_key": a["join_key"],
                "municipio": a["municipio"],
                "zona": a["zona"],
                "secao": a["secao"],
                "aptos_1t": a.get("aptos"),
                "aptos_2t": pd.NA,
                "comparecimento_1t": a.get("bu_comparecimento"),
                "comparecimento_2t": pd.NA,
                "abstencao_1t": a.get("abstencao"),
                "abstencao_2t": pd.NA,
                "delta_comparecimento": pd.NA,
                "delta_abstencao": pd.NA,
                "pct_abstencao_1t": a.get("pct_abstencao"),
                "pct_abstencao_2t": pd.NA,
                "bu_total_1t": a.get("bu_total"),
                "bu_total_2t": pd.NA,
                "sem_digital_1t": a.get("sem_digital"),
                "sem_digital_2t": pd.NA,
                "pct_sem_digital_1t": a.get("pct_sem_digital"),
                "pct_sem_digital_2t": pd.NA,
                "status": "pendente_2t",
            }
        )
        meta["secoes_so_1t"] = int(len(out))
        for col in COMPARE_COLS:
            if col not in out.columns:
                out[col] = pd.NA
        return out.reindex(columns=COMPARE_COLS), meta

    left = a.rename(
        columns={
            "aptos": "aptos_1t",
            "bu_comparecimento": "comparecimento_1t",
            "abstencao": "abstencao_1t",
            "pct_abstencao": "pct_abstencao_1t",
            "bu_total": "bu_total_1t",
            "sem_digital": "sem_digital_1t",
            "pct_sem_digital": "pct_sem_digital_1t",
        }
    )
    right = b.rename(
        columns={
            "aptos": "aptos_2t",
            "bu_comparecimento": "comparecimento_2t",
            "abstencao": "abstencao_2t",
            "pct_abstencao": "pct_abstencao_2t",
            "bu_total": "bu_total_2t",
            "sem_digital": "sem_digital_2t",
            "pct_sem_digital": "pct_sem_digital_2t",
        }
    )
    right_cols = [
        c
        for c in (
            "join_key",
            "aptos_2t",
            "comparecimento_2t",
            "abstencao_2t",
            "pct_abstencao_2t",
            "bu_total_2t",
            "sem_digital_2t",
            "pct_sem_digital_2t",
            "municipio",
            "zona",
            "secao",
        )
        if c in right.columns
    ]
    merged = left.merge(
        right[right_cols],
        on="join_key",
        how="outer",
        indicator=True,
        suffixes=("", "_r"),
    )
    for col in ("municipio", "zona", "secao"):
        if f"{col}_r" in merged.columns:
            merged[col] = merged[col].fillna(merged[f"{col}_r"])
            merged = merged.drop(columns=[f"{col}_r"])

    merged["uf"] = uf
    merged["status"] = merged["_merge"].map(
        {"both": "ambos", "left_only": "so_1t", "right_only": "so_2t"}
    )
    merged["delta_comparecimento"] = (
        merged["comparecimento_2t"] - merged["comparecimento_1t"]
    )
    merged["delta_abstencao"] = merged["abstencao_2t"] - merged["abstencao_1t"]
    merged["delta_pct_sem_digital"] = (
        merged["pct_sem_digital_2t"] - merged["pct_sem_digital_1t"]
    )

    meta["secoes_ambos"] = int((merged["status"] == "ambos").sum())
    meta["secoes_so_1t"] = int((merged["status"] == "so_1t").sum())
    meta["secoes_so_2t"] = int((merged["status"] == "so_2t").sum())

    # totais UF para o painel
    ambos = merged["status"] == "ambos"
    if ambos.any():
        apt1 = pd.to_numeric(merged.loc[ambos, "aptos_1t"], errors="coerce").sum()
        apt2 = pd.to_numeric(merged.loc[ambos, "aptos_2t"], errors="coerce").sum()
        ab1 = pd.to_numeric(merged.loc[ambos, "abstencao_1t"], errors="coerce").sum()
        ab2 = pd.to_numeric(merged.loc[ambos, "abstencao_2t"], errors="coerce").sum()
        if apt1 and apt2:
            meta["delta_abstencao_pp"] = round(
                100 * float(ab2) / float(apt2) - 100 * float(ab1) / float(apt1), 4
            )
        meta["delta_comparecimento"] = int(
            pd.to_numeric(merged.loc[ambos, "delta_comparecimento"], errors="coerce")
            .fillna(0)
            .sum()
        )
        for label, col_sd, col_comp in (
            ("1t", "sem_digital_1t", "comparecimento_1t"),
            ("2t", "sem_digital_2t", "comparecimento_2t"),
        ):
            sd = pd.to_numeric(merged.loc[ambos, col_sd], errors="coerce")
            cp = pd.to_numeric(merged.loc[ambos, col_comp], errors="coerce")
            mask = sd.notna() & cp.gt(0)
            if mask.any():
                meta[f"pct_sem_digital_{label}"] = round(
                    100 * float(sd[mask].sum()) / float(cp[mask].sum()), 4
                )
        if meta["pct_sem_digital_1t"] is not None and meta["pct_sem_digital_2t"] is not None:
            meta["delta_pct_sem_digital"] = round(
                meta["pct_sem_digital_2t"] - meta["pct_sem_digital_1t"], 4
            )

    merged = enrich_with_votos(merged, uf, turno_a, turno_b, meta)
    merged = enrich_with_horario_secao(merged, uf, turno_a, turno_b)
    merged = apply_anomaly_flags(merged)

    meta["n_flag_abstencao"] = int(merged["flag_abstencao"].sum())
    meta["n_flag_margem"] = int(merged["flag_margem"].sum())
    meta["n_flag_sem_digital_x_margem"] = int(merged["flag_sem_digital_x_margem"].sum())
    meta["n_flag_pos17"] = int(merged["flag_pos17"].sum())
    meta["n_flag_so_turno"] = int(merged["flag_so_turno"].sum())
    meta["pronto"] = True
    fa = meta.get("finalista_a") or "?"
    fb = meta.get("finalista_b") or "?"
    meta["mensagem"] = (
        f"Comparativo 1º×2º preenchido (finalistas {fa}×{fb}; "
        f"saldo agregado por seção — não é migração eleitor a eleitor)."
    )
    out = merged.reindex(columns=COMPARE_COLS)
    return out, meta


def write_compare_report(
    df: pd.DataFrame, meta: dict, uf: str, turno_a: int, turno_b: int
) -> tuple[Path, Path, Path]:
    ensure_dirs()
    uf = uf.upper()
    pq = REPORTS_DIR / f"comparar_turnos_{uf}_{turno_a}t_{turno_b}t.parquet"
    csv = REPORTS_DIR / f"comparar_turnos_summary_{uf}_{turno_a}t_{turno_b}t.csv"
    md = REPORTS_DIR / f"comparar_turnos_{uf}_{turno_a}t_{turno_b}t.md"

    df.to_parquet(pq, index=False)
    pd.DataFrame([meta]).to_csv(csv, index=False)

    fa = meta.get("finalista_a") or "?"
    fb = meta.get("finalista_b") or "?"
    lines = [
        f"# Comparativo {turno_a}º × {turno_b}º turno — {uf}",
        "",
        f"Status: **{'pronto' if meta['pronto'] else 'esqueleto (aguardando 2º)'}**",
        "",
        meta["mensagem"],
        "",
        "## Disponibilidade",
        "",
        f"- {turno_a}º turno (audit): "
        f"{'sim' if meta['turno_a_disponivel'] else 'não'} · "
        f"{meta['secoes_1t']:,} seções",
        f"- {turno_b}º turno (audit): "
        f"{'sim' if meta['turno_b_disponivel'] else 'não'} · "
        f"{meta['secoes_2t']:,} seções",
        f"- Finalistas (nominais no {turno_b}º): **{fa}** e **{fb}**",
        f"- Margem = votos({fa}) − votos({fb})",
        "",
        "## Métricas",
        "",
        f"- Seções em ambos: **{meta['secoes_ambos']:,}**",
        f"- Só no {turno_a}º: **{meta['secoes_so_1t']:,}** · "
        f"só no {turno_b}º: **{meta['secoes_so_2t']:,}**",
        f"- Δ comparecimento (soma seções ambos): **{meta.get('delta_comparecimento')}**",
        f"- Δ abstenção (pp, aptos ambos): **{meta.get('delta_abstencao_pp')}**",
        f"- % sem digital 1º→2º: **{meta.get('pct_sem_digital_1t')}** → "
        f"**{meta.get('pct_sem_digital_2t')}** (Δ **{meta.get('delta_pct_sem_digital')}**)",
        "",
        "## Pós-17h (UF)",
        "",
        f"- % ≥17h no {turno_a}º: **{meta['horario_1t_pct_apos_17h']}**",
        f"- % ≥17h no {turno_b}º: **{meta['horario_2t_pct_apos_17h']}**",
        f"- Δ (2º − 1º): **{meta['delta_pct_apos_17h']}**",
        "",
        "## Flags de anomalia (percentis na UF)",
        "",
        f"- `|Δ abstenção|` ≥ p{int(P_FLAG_ABST*100)}: **{meta.get('n_flag_abstencao', 0)}**",
        f"- `|Δ margem|` ≥ p{int(P_FLAG_MARGEM*100)}: **{meta.get('n_flag_margem', 0)}**",
        f"- alto % sem digital 1º × `|Δ margem|`: "
        f"**{meta.get('n_flag_sem_digital_x_margem', 0)}**",
        f"- cauda pós-17h atípica: **{meta.get('n_flag_pos17', 0)}**",
        f"- só em um turno: **{meta.get('n_flag_so_turno', 0)}**",
        "",
    ]

    if meta.get("pronto") and not df.empty:
        ambos = df[df["status"] == "ambos"].copy()
        if not ambos.empty and "delta_margem" in ambos.columns:
            lines += [
                f"## Seções que mais movem a margem ({fa}−{fb})",
                "",
            ]
            top = ambos.reindex(
                ambos["delta_margem"].abs().sort_values(ascending=False).index
            ).head(15)
            lines += [
                "| join_key | Δ margem | Δ abst | % sem dig 1º | %≥17h 2º | flags |",
                "|---|---:|---:|---:|---:|---|",
            ]
            for _, r in top.iterrows():
                lines.append(
                    f"| `{r['join_key']}` | {r.get('delta_margem')} | "
                    f"{r.get('delta_abstencao')} | {r.get('pct_sem_digital_1t')} | "
                    f"{r.get('pct_apos_17h_2t')} | {r.get('flags') or '—'} |"
                )
            lines.append("")

        flagged = df[df["flags"].fillna("").astype(str).str.len() > 0]
        if not flagged.empty:
            lines += [
                "## Seções com flag",
                "",
                f"{len(flagged):,} seção(ões) (até 30):",
                "",
            ]
            for _, r in flagged.head(30).iterrows():
                lines.append(
                    f"- `{r['join_key']}` · {r['flags']} · "
                    f"Δmargem={r.get('delta_margem')} · "
                    f"Δabst={r.get('delta_abstencao')}"
                )
            if len(flagged) > 30:
                lines.append(f"- … e mais {len(flagged) - 30}")
            lines.append("")

    lines += [
        "## Hipóteses → observáveis (agregado; não conclusões)",
        "",
        "| Hipótese | Observável |",
        "|---|---|",
        "| Transferência aparente dos eliminados | "
        "`votos_eliminados_1t` ≈ `ganho_finalistas` − `delta_comparecimento` "
        "(residual em `gap_transferencia`) |",
        "| Abstenção seletiva | `|delta_abstencao|` alto com pouco Δ nos finalistas |",
        "| Risco operacional | alto `% sem digital` × `|delta_margem|` |",
        "| Cauda horária | alto `% ≥17h` × Δ comparecimento/margem |",
        "| Contingência / troca de urna | status `so_1t` / `so_2t` |",
        "",
        "## Limites",
        "",
        "- Comparação é **agregada por seção** (`join_key`).",
        "- Não dá para saber *quem* mudou de candidato entre turnos (sigilo do voto).",
        "- “Migração” = mudança dos totais da seção (finalistas, eliminados, abstenção).",
        "- Correlação ≠ fraude. RDV≡BU e BU≡CSV oficial só validam **integridade "
        "entre arquivos públicos** disponibilizados.",
        "",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")
    return md, pq, csv


def print_compare_meta(meta: dict) -> None:
    console.print(f"\n[bold]Comparativo turnos — {meta['uf']}[/bold]")
    table = Table()
    table.add_column("Campo")
    table.add_column("Valor")
    table.add_row("Pronto", "sim" if meta["pronto"] else "não (esqueleto)")
    table.add_row("Mensagem", str(meta["mensagem"])[:90])
    table.add_row("Finalistas", str(meta.get("finalistas") or "—"))
    table.add_row("Seções 1º", f"{meta['secoes_1t']:,}")
    table.add_row("Seções 2º", f"{meta['secoes_2t']:,}")
    table.add_row("Flags margem", str(meta.get("n_flag_margem", 0)))
    table.add_row("% ≥17h 1º", str(meta["horario_1t_pct_apos_17h"]))
    table.add_row("% ≥17h 2º", str(meta["horario_2t_pct_apos_17h"]))
    console.print(table)


def consolidate_compare(
    ufs: list[str], turno_a: int, turno_b: int
) -> Path | None:
    frames: list[pd.DataFrame] = []
    for uf in ufs:
        p = REPORTS_DIR / f"comparar_turnos_summary_{uf.upper()}_{turno_a}t_{turno_b}t.csv"
        if p.exists():
            frames.append(pd.read_csv(p))
    if not frames:
        return None
    out = REPORTS_DIR / f"comparar_turnos_summary_MULTI_{turno_a}t_{turno_b}t.csv"
    pd.concat(frames, ignore_index=True).to_csv(out, index=False)
    return out


def run_comparar_turnos(
    ufs: list[str], turno_a: int = 1, turno_b: int = 2
) -> list[Path]:
    outputs: list[Path] = []
    done: list[str] = []
    for i, uf in enumerate(ufs, start=1):
        uf = uf.upper()
        console.print(f"\n[bold][{i}/{len(ufs)}] Comparar turnos {uf}[/bold]")
        df, meta = build_compare(uf, turno_a, turno_b)
        print_compare_meta(meta)
        md, pq, csv = write_compare_report(df, meta, uf, turno_a, turno_b)
        console.print(f"[green]Relatório:[/green] {md}")
        outputs.extend([md, pq, csv])
        done.append(uf)
    if len(done) > 1:
        multi = consolidate_compare(done, turno_a, turno_b)
        if multi:
            console.print(f"\n[green]Resumo multi-UF:[/green] {multi}")
            outputs.append(multi)
    return outputs
