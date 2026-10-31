"""Gera CSVs leves para o painel Quarto (foco 1º×2º + sem digital)."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
OUT = ROOT / "site" / "data"

OUTLIERS_PER_UF = 5
OUTLIERS_MAX = 80


def _read_glob(pattern: str, *, multi_name: str | None = None) -> pd.DataFrame | None:
    """Lê summaries per-UF; MULTI só se cobrir ≥ UFs dos per-UF (evita MULTI parcial)."""
    frames = [
        pd.read_csv(p)
        for p in sorted(REPORTS.glob(pattern))
        if "MULTI" not in p.name
    ]
    per_uf = pd.concat(frames, ignore_index=True) if frames else None
    if per_uf is not None and not per_uf.empty and "uf" in per_uf.columns:
        per_uf = per_uf.drop_duplicates(["uf"], keep="last").copy()
        n_uf = int(per_uf["uf"].nunique())
    else:
        n_uf = 0

    multi = REPORTS / multi_name if multi_name else None
    if multi is not None and multi.exists():
        mdf = pd.read_csv(multi)
        if not mdf.empty and "uf" in mdf.columns:
            mdf = mdf.drop_duplicates(["uf"], keep="last").copy()
            n_multi = int(mdf["uf"].nunique())
        else:
            n_multi = 0
        if n_multi >= n_uf and n_multi > 0:
            return mdf
        if n_uf > 0:
            return per_uf
        return mdf if n_multi else None

    return per_uf if n_uf else None


def _sem_digital_turno(turno: int) -> pd.DataFrame:
    suffix = f"_{turno}t"
    rows: list[dict] = []
    for path in sorted(REPORTS.glob(f"by_municipio_*{suffix}.csv")):
        if "MULTI" in path.name:
            continue
        df = pd.read_csv(path)
        if df.empty:
            continue
        uf = str(df["uf"].iloc[0]).upper()
        com = df[df["pct_sem_digital"].notna()].copy()
        if com.empty:
            rows.append(
                {
                    "uf": uf,
                    f"municipios{suffix}": int(df["municipio"].nunique()),
                    f"urnas{suffix}": int(df["urnas"].sum()),
                    f"comparecimento{suffix}": int(df["comparecimento"].sum()),
                    f"pct_sem_digital{suffix}": None,
                    f"com_detalhe_bio{suffix}": False,
                }
            )
            continue
        comparecimento = int(com["comparecimento"].sum())
        sem_digital = int(com["sem_digital"].sum())
        rows.append(
            {
                "uf": uf,
                f"municipios{suffix}": int(com["municipio"].nunique()),
                f"urnas{suffix}": int(com["urnas"].sum()),
                f"comparecimento{suffix}": comparecimento,
                f"pct_sem_digital{suffix}": round(
                    100 * sem_digital / comparecimento, 4
                ),
                f"com_detalhe_bio{suffix}": True,
            }
        )
    return pd.DataFrame(rows) if rows else pd.DataFrame()


def _sem_digital_por_uf() -> pd.DataFrame:
    return _sem_digital_turno(1)


def _cruzar_por_uf(turno: int = 1) -> pd.DataFrame:
    df = _read_glob(
        f"cruzar_oficial_summary_*_{turno}t.csv",
        multi_name=f"cruzar_oficial_summary_MULTI_{turno}t.csv",
    )
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.drop_duplicates(["uf"], keep="last").copy()
    df["uf"] = df["uf"].astype(str).str.upper()
    pct_col = f"pct_secoes_ok_oficial_{turno}t"
    df[pct_col] = df.apply(
        lambda r: round(100 * r["secoes_ok"] / r["secoes"], 4) if r.get("secoes") else None,
        axis=1,
    )
    df = df.rename(
        columns={
            "secoes": f"secoes_oficial_{turno}t",
            "secoes_ok": f"secoes_ok_oficial_{turno}t",
            "secoes_divergentes": f"secoes_divergentes_{turno}t",
        }
    )
    keep = [
        "uf",
        f"secoes_oficial_{turno}t",
        f"secoes_ok_oficial_{turno}t",
        f"secoes_divergentes_{turno}t",
        pct_col,
    ]
    return df[[c for c in keep if c in df.columns]]


def _horario_summary_por_turno(turno: int) -> pd.DataFrame:
    multi = REPORTS / f"horario_summary_MULTI_{turno}t.csv"
    if multi.exists():
        df = pd.read_csv(multi)
    else:
        frames = [
            pd.read_csv(p)
            for p in sorted(REPORTS.glob(f"horario_summary_*_{turno}t.csv"))
            if "MULTI" not in p.name
        ]
        if not frames:
            return pd.DataFrame()
        df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates(["uf"], keep="last").copy()
    df["uf"] = df["uf"].astype(str).str.upper()
    suffix = f"_{turno}t"
    return df.rename(
        columns={
            "pct_apos_17h": f"pct_apos_17h{suffix}",
            "hora_pico": f"hora_pico{suffix}",
            "total_habilitacoes": f"habilitacoes{suffix}",
            "pct_17_18": f"pct_17_18{suffix}",
            "pct_18_19": f"pct_18_19{suffix}",
            "pct_19_mais": f"pct_19_mais{suffix}",
        }
    )[
        [
            "uf",
            f"pct_apos_17h{suffix}",
            f"hora_pico{suffix}",
            f"habilitacoes{suffix}",
            f"pct_17_18{suffix}",
            f"pct_18_19{suffix}",
            f"pct_19_mais{suffix}",
        ]
    ]


def _achados_por_uf() -> pd.DataFrame:
    df = _read_glob(
        "achados_summary_*_1t_2t.csv",
        multi_name="achados_summary_MULTI_1t_2t.csv",
    )
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.drop_duplicates(["uf"], keep="last").copy()
    df["uf"] = df["uf"].astype(str).str.upper()
    keep = [
        c
        for c in (
            "uf",
            "n_achados",
            "n_A",
            "n_B",
            "n_C",
            "protocolo_versao",
        )
        if c in df.columns
    ]
    return df[keep].rename(
        columns={
            "n_achados": "achados_total",
            "n_A": "achados_A",
            "n_B": "achados_B",
            "n_C": "achados_C",
        }
    )


def _comparar_por_uf() -> pd.DataFrame:
    df = _read_glob(
        "comparar_turnos_summary_*_1t_2t.csv",
        multi_name="comparar_turnos_summary_MULTI_1t_2t.csv",
    )
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.drop_duplicates(["uf"], keep="last").copy()
    df["uf"] = df["uf"].astype(str).str.upper()
    keep = [
        "uf",
        "turno_a_disponivel",
        "turno_b_disponivel",
        "secoes_1t",
        "secoes_2t",
        "pronto",
        "horario_1t_pct_apos_17h",
        "horario_2t_pct_apos_17h",
        "delta_pct_apos_17h",
        "delta_abstencao_pp",
        "delta_comparecimento",
        "pct_sem_digital_1t",
        "pct_sem_digital_2t",
        "delta_pct_sem_digital",
        "finalistas",
        "n_flag_margem",
        "n_flag_abstencao",
        "mensagem",
    ]
    keep = [c for c in keep if c in df.columns]
    out = df[keep].rename(columns={"pronto": "pronto_2t"})
    return out


def build_painel_uf() -> pd.DataFrame:
    parts = [
        _sem_digital_por_uf(),
        _sem_digital_turno(2),
        _cruzar_por_uf(1),
        _cruzar_por_uf(2),
        _horario_summary_por_turno(1),
        _horario_summary_por_turno(2),
        _comparar_por_uf(),
        _achados_por_uf(),
    ]
    parts = [p for p in parts if p is not None and not p.empty]
    if not parts:
        return pd.DataFrame()

    painel = parts[0]
    for p in parts[1:]:
        # comparar pode trazer pct_sem_digital_* — suffixes
        overlap = [c for c in p.columns if c != "uf" and c in painel.columns]
        if overlap:
            p = p.rename(columns={c: f"{c}_cmp" for c in overlap})
        painel = painel.merge(p, on="uf", how="outer")

    # Preferir by-municipio; fallback do summary do comparar
    for col in ("pct_sem_digital_1t", "pct_sem_digital_2t", "delta_pct_sem_digital"):
        cmp_col = f"{col}_cmp"
        if cmp_col in painel.columns:
            if col not in painel.columns:
                painel[col] = painel[cmp_col]
            else:
                painel[col] = painel[col].fillna(painel[cmp_col])
            painel = painel.drop(columns=[cmp_col])

    for col in (
        "delta_abstencao_pp",
        "delta_comparecimento",
        "delta_pct_sem_digital",
    ):
        cmp_col = f"{col}_cmp"
        if cmp_col in painel.columns:
            if col not in painel.columns:
                painel[col] = painel[cmp_col]
            else:
                painel[col] = painel[col].fillna(painel[cmp_col])
            painel = painel.drop(columns=[cmp_col])

    # Colunas 2º / Δ já no schema (vazias até existir dado)
    for col in (
        "pct_sem_digital_2t",
        "delta_pct_sem_digital",
        "delta_abstencao_pp",
        "delta_comparecimento",
        "pct_apos_17h_2t",
        "hora_pico_2t",
        "habilitacoes_2t",
    ):
        if col not in painel.columns:
            painel[col] = pd.NA

    if (
        "pct_sem_digital_1t" in painel.columns
        and "pct_sem_digital_2t" in painel.columns
    ):
        both_sd = painel["pct_sem_digital_1t"].notna() & painel["pct_sem_digital_2t"].notna()
        if both_sd.any():
            need = painel["delta_pct_sem_digital"].isna() if "delta_pct_sem_digital" in painel.columns else both_sd
            painel.loc[both_sd & need, "delta_pct_sem_digital"] = (
                painel.loc[both_sd & need, "pct_sem_digital_2t"].astype(float)
                - painel.loc[both_sd & need, "pct_sem_digital_1t"].astype(float)
            ).round(4)

    if "delta_pct_apos_17h" not in painel.columns:
        painel["delta_pct_apos_17h"] = pd.NA
    if "pct_apos_17h_1t" in painel.columns and "pct_apos_17h_2t" in painel.columns:
        both = painel["pct_apos_17h_1t"].notna() & painel["pct_apos_17h_2t"].notna()
        if both.any():
            painel["delta_pct_apos_17h"] = painel["delta_pct_apos_17h"].astype("Float64")
            painel.loc[both, "delta_pct_apos_17h"] = (
                painel.loc[both, "pct_apos_17h_2t"].astype(float)
                - painel.loc[both, "pct_apos_17h_1t"].astype(float)
            ).round(4)

    if "pronto_2t" not in painel.columns:
        painel["pronto_2t"] = False
    else:
        painel["pronto_2t"] = painel["pronto_2t"].fillna(False).astype(bool)

    if "secoes_1t" not in painel.columns:
        painel["secoes_1t"] = pd.NA
    if "secoes_oficial_1t" in painel.columns:
        painel["secoes_1t"] = painel["secoes_1t"].fillna(painel["secoes_oficial_1t"])
    if "secoes_2t" not in painel.columns:
        painel["secoes_2t"] = 0
    painel["secoes_2t"] = painel["secoes_2t"].fillna(0)

    painel["status_2t"] = painel["pronto_2t"].map(
        {True: "comparativo ativo", False: "pendente"}
    )
    return painel.sort_values("uf").reset_index(drop=True)


def build_curva_horaria() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for turno in (1, 2):
        multi = REPORTS / f"curva_horaria_MULTI_{turno}t.csv"
        if not multi.exists():
            multi = REPORTS / f"horario_por_hora_MULTI_{turno}t.csv"
        if multi.exists():
            df = pd.read_csv(multi)
        else:
            parts = [
                pd.read_csv(p)
                for p in sorted(
                    list(REPORTS.glob(f"curva_horaria_*_{turno}t.csv"))
                    + list(REPORTS.glob(f"horario_por_hora_*_{turno}t.csv"))
                )
                if "MULTI" not in p.name
            ]
            if not parts:
                continue
            df = pd.concat(parts, ignore_index=True)
        if "turno" not in df.columns:
            df["turno"] = turno
        frames.append(df)
    if not frames:
        return pd.DataFrame(columns=["uf", "turno", "hora", "habilitacoes", "pct", "after_17h"])
    out = pd.concat(frames, ignore_index=True)
    out["uf"] = out["uf"].astype(str).str.upper()
    return out.sort_values(["turno", "uf", "hora"]).reset_index(drop=True)


def build_outliers_sem_digital() -> pd.DataFrame:
    """Top seções por % sem digital (1º) + Δ do comparar quando existir."""
    rows: list[pd.DataFrame] = []
    for path in sorted(REPORTS.glob("audit_presidente_*_1t.parquet")):
        if "MULTI" in path.name or "votos" in path.name:
            continue
        df = pd.read_parquet(path)
        if df.empty:
            continue
        ok = df[df["ok"] == True].copy()  # noqa: E712
        if ok.empty:
            continue
        has = ok["bio"].notna() | ok["biografia"].notna() | ok["sem_biometria"].notna()
        ok = ok[has & ok["bu_comparecimento"].fillna(0).gt(0)].copy()
        if ok.empty:
            continue
        ok["sem_digital"] = ok["biografia"].fillna(0) + ok["sem_biometria"].fillna(0)
        ok["pct_sem_digital"] = (
            100 * ok["sem_digital"] / ok["bu_comparecimento"]
        ).round(4)
        ok["delta_abstencao"] = pd.NA
        ok["delta_margem"] = pd.NA
        ok["flags"] = ""
        uf = str(ok["uf"].iloc[0]).upper()
        cmp_path = REPORTS / f"comparar_turnos_{uf}_1t_2t.parquet"
        if cmp_path.exists():
            cmp = pd.read_parquet(cmp_path)
            cols = [
                c
                for c in (
                    "join_key",
                    "delta_abstencao",
                    "delta_margem",
                    "flags",
                    "pct_sem_digital_1t",
                    "votos_fa_1t",
                    "votos_fb_1t",
                    "votos_eliminados_1t",
                    "votos_fa_2t",
                    "votos_fb_2t",
                )
                if c in cmp.columns
            ]
            if "join_key" in cols:
                ok = ok.drop(columns=["delta_abstencao", "delta_margem", "flags"], errors="ignore")
                ok = ok.merge(cmp[cols], on="join_key", how="left")
                if "pct_sem_digital_1t" in ok.columns:
                    ok["pct_sem_digital"] = ok["pct_sem_digital"].fillna(
                        ok["pct_sem_digital_1t"]
                    )
        # Preferir seções com flag; senão top % sem digital
        if "flags" not in ok.columns:
            ok["flags"] = ""
        ok["delta_margem_pp"] = _delta_margem_pp(ok)
        flag_mask = ok["flags"].fillna("").astype(str).str.len() > 0
        flagged = ok[flag_mask]
        if not flagged.empty:
            top = flagged.nlargest(OUTLIERS_PER_UF, "pct_sem_digital")
        else:
            top = ok.nlargest(OUTLIERS_PER_UF, "pct_sem_digital")
        keep_cols = [
            c
            for c in (
                "uf",
                "join_key",
                "municipio",
                "zona",
                "secao",
                "bu_comparecimento",
                "pct_abstencao",
                "pct_sem_digital",
                "delta_abstencao",
                "delta_margem",
                "delta_margem_pp",
                "flags",
            )
            if c in top.columns
        ]
        rows.append(top[keep_cols])
    if not rows:
        return pd.DataFrame()
    all_top = pd.concat(rows, ignore_index=True)
    if "flags" not in all_top.columns:
        all_top["flags"] = ""
    # Prioriza quem tem Δ/flag; depois % sem digital
    all_top["_has_delta"] = all_top["delta_margem"].notna() | all_top["flags"].fillna("").astype(str).str.len().gt(0)
    all_top = all_top.sort_values(
        ["_has_delta", "pct_sem_digital"], ascending=[False, False]
    ).head(OUTLIERS_MAX)
    all_top = all_top.drop(columns=["_has_delta"])
    mun_path = ROOT / "data" / "ref" / "municipios_tse.csv"
    if mun_path.exists():
        mun = pd.read_csv(mun_path)
        mun["uf"] = mun["uf"].astype(str).str.upper()
        all_top = all_top.merge(mun, on=["uf", "municipio"], how="left")
        all_top["nome"] = all_top["nome"].fillna("(desconhecido)")
    else:
        all_top["nome"] = "(desconhecido)"
    all_top["turno"] = 1
    return all_top.reset_index(drop=True)


def _delta_margem_pp(df: pd.DataFrame) -> pd.Series:
    """Δ da margem em pp dos válidos. Sinal: Lula (13) − Flávio (22)."""
    need = (
        "votos_fa_1t",
        "votos_fb_1t",
        "votos_eliminados_1t",
        "votos_fa_2t",
        "votos_fb_2t",
    )
    if any(c not in df.columns for c in need):
        return pd.Series(pd.NA, index=df.index)
    v13_1 = pd.to_numeric(df["votos_fa_1t"], errors="coerce")
    v22_1 = pd.to_numeric(df["votos_fb_1t"], errors="coerce")
    elim = pd.to_numeric(df["votos_eliminados_1t"], errors="coerce").fillna(0)
    v13_2 = pd.to_numeric(df["votos_fa_2t"], errors="coerce")
    v22_2 = pd.to_numeric(df["votos_fb_2t"], errors="coerce")
    val1 = v13_1 + v22_1 + elim
    val2 = v13_2 + v22_2
    m1 = (v13_1 - v22_1) / val1.where(val1 > 0)
    m2 = (v13_2 - v22_2) / val2.where(val2 > 0)
    return (100 * (m2 - m1)).round(2)


def build_anomalias_secao() -> pd.DataFrame:
    """Seções do piloto com flags no comparativo (para scatter do painel)."""
    frames: list[pd.DataFrame] = []
    for path in sorted(REPORTS.glob("comparar_turnos_*_1t_2t.parquet")):
        if "MULTI" in path.name:
            continue
        df = pd.read_parquet(path)
        if df.empty or "status" not in df.columns:
            continue
        both = df[df["status"] == "ambos"].copy()
        if both.empty:
            continue
        both["delta_margem_pp"] = _delta_margem_pp(both)
        keep = [
            c
            for c in (
                "uf",
                "join_key",
                "municipio",
                "zona",
                "secao",
                "pct_sem_digital_1t",
                "delta_margem",
                "delta_margem_pp",
                "delta_abstencao",
                "pct_apos_17h_2t",
                "flags",
            )
            if c in both.columns
        ]
        frames.append(both[keep])
    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, ignore_index=True)
    ach_path = REPORTS / "achados_MULTI_1t_2t.parquet"
    if ach_path.exists():
        ach = pd.read_parquet(ach_path, columns=["uf", "join_key", "nivel"])
        ach = ach.drop_duplicates(["uf", "join_key"])
        out = out.merge(ach, on=["uf", "join_key"], how="left")
    else:
        out["nivel"] = pd.NA
    return out.reset_index(drop=True)


def _votavel_code(tipo: str, numero) -> str | None:
    if tipo == "branco":
        return "95"
    if tipo == "nulo":
        return "96"
    if tipo != "nominal" or numero is None or pd.isna(numero):
        return None
    return str(int(numero))


def _pack_turno(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por seção: votos do BU compactados e flag se RDV ≠ BU."""
    keys = ["municipio", "zona", "secao"]
    work = df.copy()
    work["code"] = [
        _votavel_code(t, n) for t, n in zip(work["tipo"], work["numero"], strict=False)
    ]
    work = work[work["code"].notna()]
    if work.empty:
        return pd.DataFrame(columns=[*keys, "bit", "bad"])
    dif = (
        work.assign(bad=work["votos_bu"].ne(work["votos_rdv"]))
        .groupby(keys, as_index=False)["bad"]
        .any()
    )
    pos = work[work["votos_bu"] > 0].sort_values(
        [*keys, "votos_bu"], ascending=[True, True, True, False]
    )
    pos = pos.assign(
        bit=pos["code"].astype(str) + "=" + pos["votos_bu"].astype("int64").astype(str)
    )
    packed = pos.groupby(keys, as_index=False)["bit"].agg("|".join)
    out = dif.merge(packed, on=keys, how="left")
    out["bit"] = out["bit"].fillna("")
    return out


def _divergencias_votavel(
    bruto: list[tuple[int, pd.DataFrame]],
    cruzamentos: list[tuple[int, pd.DataFrame]],
) -> pd.DataFrame:
    """Conta votáveis em que RDV≠BU ou BU≠oficial. Só grava o detalhe quando há diferença."""
    keys = ["municipio", "zona", "secao"]
    partes: list[pd.DataFrame] = []
    for turno, raw in bruto:
        work = raw.copy()
        work["code"] = [
            _votavel_code(t, n) for t, n in zip(work["tipo"], work["numero"], strict=False)
        ]
        work = work[work["code"].notna()]
        if work.empty:
            continue
        work["rdv"] = pd.to_numeric(work["votos_rdv"], errors="coerce")
        work["bu"] = pd.to_numeric(work["votos_bu"], errors="coerce")
        g = work.groupby([*keys, "code"], as_index=False).agg(rdv=("rdv", "sum"), bu=("bu", "sum"))
        g["turno"] = turno
        ruim = g[g["rdv"].notna() & g["bu"].notna() & g["rdv"].ne(g["bu"])]
        if ruim.empty:
            continue
        ruim = ruim.copy()
        ruim["pedaco"] = (
            ruim["turno"].astype(str)
            + ":"
            + ruim["code"].astype(str)
            + ":"
            + ruim["rdv"].astype("int64").astype(str)
            + ":"
            + ruim["bu"].astype("int64").astype(str)
            + ":"
        )
        partes.append(ruim[[*keys, "pedaco"]])
    for turno, cruz in cruzamentos:
        if cruz.empty or "votavel" not in cruz.columns:
            continue
        c = cruz.copy()
        c["code"] = pd.to_numeric(c["votavel"], errors="coerce")
        c = c[c["code"].notna()]
        c["bu"] = pd.to_numeric(c["votos_bu"], errors="coerce")
        c["oficial"] = pd.to_numeric(c["votos_oficial"], errors="coerce")
        ruim = c[c["bu"].notna() & c["oficial"].notna() & c["bu"].ne(c["oficial"])]
        if ruim.empty:
            continue
        ruim = ruim.copy()
        ruim["pedaco"] = (
            str(turno)
            + ":"
            + ruim["code"].astype("int64").astype(str)
            + "::"
            + ruim["bu"].astype("int64").astype(str)
            + ":"
            + ruim["oficial"].astype("int64").astype(str)
        )
        partes.append(ruim[[*keys, "pedaco"]])
    if not partes:
        return pd.DataFrame(columns=[*keys, "ndiv", "det"])
    tudo = pd.concat(partes, ignore_index=True)
    tudo["chave_v"] = tudo["pedaco"].str.split(":").str[:2].str.join(":")
    out = tudo.groupby(keys, as_index=False).agg(
        ndiv=("chave_v", "nunique"),
        det=("pedaco", "|".join),
    )
    return out


def build_secao_lookup() -> None:
    """CSVs por UF para a consulta de seção no site (totais do BU, presidente)."""
    dest = OUT / "secao"
    dest.mkdir(parents=True, exist_ok=True)

    mun_path = ROOT / "data" / "ref" / "municipios_tse.csv"
    if mun_path.exists():
        mun = pd.read_csv(mun_path, dtype={"uf": str, "nome": str})
        mun["municipio"] = mun["municipio"].astype(int)
        mun = mun.drop_duplicates(["uf", "municipio"]).sort_values(["uf", "nome"])
        mun.to_csv(dest / "municipios.csv", index=False)
        print(f"escrito {dest / 'municipios.csv'} ({len(mun)} municípios)")
    else:
        print(f"aviso: sem {mun_path} — a página mostra o código do município")

    rot_frames = []
    for turno in (1, 2):
        path = REPORTS / f"cruzar_oficial_AC_{turno}t.parquet"
        if not path.exists():
            continue
        part = pd.read_parquet(path, columns=["votavel", "nome_votavel"])
        rot_frames.append(part)
    if rot_frames:
        rot = (
            pd.concat(rot_frames, ignore_index=True)
            .dropna(subset=["votavel"])
            .drop_duplicates(["votavel"])
            .sort_values("votavel")
        )
        rot.to_csv(dest / "rotulos.csv", index=False)
        print(f"escrito {dest / 'rotulos.csv'} ({len(rot)} votáveis)")

    from urna_logs.config import UFS

    total_bytes = 0
    for uf in UFS:
        frames = []
        bruto: list[tuple[int, pd.DataFrame]] = []
        cruzamentos: list[tuple[int, pd.DataFrame]] = []
        for turno in (1, 2):
            path = REPORTS / f"audit_presidente_votos_{uf}_{turno}t.parquet"
            if path.exists():
                raw = pd.read_parquet(
                    path,
                    columns=["municipio", "zona", "secao", "tipo", "numero", "votos_bu", "votos_rdv"],
                )
                bruto.append((turno, raw))
                packed = _pack_turno(raw).rename(columns={"bit": f"t{turno}", "bad": f"bad_{turno}"})
                frames.append(packed)
            cruz_path = REPORTS / f"cruzar_oficial_{uf}_{turno}t.parquet"
            if cruz_path.exists():
                cruzamentos.append(
                    (
                        turno,
                        pd.read_parquet(
                            cruz_path,
                            columns=["municipio", "zona", "secao", "votavel", "votos_bu", "votos_oficial"],
                        ),
                    )
                )
        if not frames:
            print(f"sem votos {uf}")
            continue
        merged = frames[0]
        for extra in frames[1:]:
            merged = merged.merge(extra, on=["municipio", "zona", "secao"], how="outer")
        for turno in (1, 2):
            col = f"t{turno}"
            if col not in merged.columns:
                merged[col] = ""
            merged[col] = merged[col].fillna("")
            bad = f"bad_{turno}"
            if bad not in merged.columns:
                merged[bad] = False
            merged[bad] = merged[bad].fillna(False).astype(bool)
        merged["dif"] = (merged["bad_1"] | merged["bad_2"]).astype(int)
        cmp_path = REPORTS / f"comparar_turnos_{uf}_1t_2t.parquet"
        cmp_cols = [
            "municipio",
            "zona",
            "secao",
            "status",
            "aptos_1t",
            "aptos_2t",
            "comparecimento_1t",
            "comparecimento_2t",
            "abstencao_1t",
            "abstencao_2t",
            "pct_sem_digital_1t",
            "pct_sem_digital_2t",
            "pct_apos_17h_1t",
            "pct_apos_17h_2t",
            "flags",
        ]
        if cmp_path.exists():
            cmp = pd.read_parquet(cmp_path, columns=cmp_cols)
            cmp["a1"] = pd.to_numeric(cmp["abstencao_1t"], errors="coerce")
            cmp["a2"] = pd.to_numeric(cmp["abstencao_2t"], errors="coerce")
            merged = merged.merge(
                cmp.drop(columns=["abstencao_1t", "abstencao_2t"]),
                on=["municipio", "zona", "secao"],
                how="left",
            )
        else:
            merged["a1"] = pd.NA
            merged["a2"] = pd.NA
            for col in cmp_cols[3:]:
                if col not in ("abstencao_1t", "abstencao_2t"):
                    merged[col] = pd.NA
        div = _divergencias_votavel(bruto, cruzamentos)
        if div.empty:
            merged["ndiv"] = 0
            merged["det"] = ""
        else:
            merged = merged.merge(div, on=["municipio", "zona", "secao"], how="left")
            merged["ndiv"] = merged["ndiv"].fillna(0).astype(int)
            merged["det"] = merged["det"].fillna("")
        ach_uf = REPORTS / f"achados_{uf}_1t_2t.parquet"
        if ach_uf.exists():
            ach = pd.read_parquet(
                ach_uf, columns=["municipio", "zona", "secao", "nivel", "codigos", "conclusao_permitida"]
            )
            ach["conclusao_permitida"] = ach["conclusao_permitida"].where(
                ach["nivel"].isin(["A", "B"]), ""
            )
            merged = merged.merge(ach, on=["municipio", "zona", "secao"], how="left")
        else:
            merged["nivel"] = pd.NA
            merged["codigos"] = pd.NA
            merged["conclusao_permitida"] = pd.NA
        for col in ("status", "flags", "nivel", "codigos", "conclusao_permitida"):
            merged[col] = merged[col].fillna("").astype(str)
        out = merged[
            [
                "municipio",
                "zona",
                "secao",
                "t1",
                "t2",
                "dif",
                "a1",
                "a2",
                "status",
                "aptos_1t",
                "aptos_2t",
                "comparecimento_1t",
                "comparecimento_2t",
                "pct_sem_digital_1t",
                "pct_sem_digital_2t",
                "pct_apos_17h_1t",
                "pct_apos_17h_2t",
                "flags",
                "nivel",
                "codigos",
                "conclusao_permitida",
                "ndiv",
                "det",
            ]
        ].sort_values(["municipio", "zona", "secao"])
        out_path = dest / f"votos_{uf}.csv"
        out.to_csv(out_path, index=False)
        total_bytes += out_path.stat().st_size
        print(f"escrito {out_path.name} ({len(out)} seções)")
    print(f"consulta de seção: {total_bytes / 1e6:.1f} MB")


def escrever_protocolo() -> None:
    """Grava os limiares registrados para o site ler, sem copiar o número na página."""
    import hashlib

    from urna_logs import __version__
    from urna_logs.thresholds import (
        CONFLUENCIA_FLAGS,
        CONFLUENCIA_MIN,
        P_FLAG_ABST,
        P_FLAG_MARGEM,
        P_FLAG_POS17,
        P_FLAG_SEM_DIG,
        PROTOCOLO_NOTA,
        PROTOCOLO_VERSAO,
    )
    from urna_logs.transferencia import CONFIANCA, MAX_LINHAS_LPHOM, MIN_SECOES

    canon = "|".join(
        [
            PROTOCOLO_VERSAO,
            f"abst={P_FLAG_ABST}",
            f"margem={P_FLAG_MARGEM}",
            f"sem_dig={P_FLAG_SEM_DIG}",
            f"pos17={P_FLAG_POS17}",
            f"confluencia_min={CONFLUENCIA_MIN}",
            "flags=" + ",".join(CONFLUENCIA_FLAGS),
            PROTOCOLO_NOTA,
        ]
    )
    rows = [
        ("protocolo_versao", PROTOCOLO_VERSAO),
        ("protocolo_nota", PROTOCOLO_NOTA),
        ("pkg_version", __version__),
        ("hash_sha256", hashlib.sha256(canon.encode("utf-8")).hexdigest()),
        ("p_flag_abst", P_FLAG_ABST),
        ("p_flag_margem", P_FLAG_MARGEM),
        ("p_flag_sem_dig", P_FLAG_SEM_DIG),
        ("p_flag_pos17", P_FLAG_POS17),
        ("confluencia_min", CONFLUENCIA_MIN),
        ("confluencia_flags", ",".join(CONFLUENCIA_FLAGS)),
        ("min_secoes", MIN_SECOES),
        ("max_linhas_lphom", MAX_LINHAS_LPHOM),
        ("confianca", CONFIANCA),
    ]
    out = OUT / "protocolo.csv"
    pd.DataFrame(rows, columns=["chave", "valor"]).to_csv(out, index=False)
    print(f"escrito {out}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    painel = build_painel_uf()
    out_p = OUT / "painel_uf.csv"
    painel.to_csv(out_p, index=False)
    print(f"escrito {out_p} ({len(painel)} UFs)")

    horas = build_curva_horaria()
    out_h = OUT / "curva_horaria.csv"
    horas.to_csv(out_h, index=False)
    n_uf = int(horas["uf"].nunique()) if not horas.empty else 0
    print(f"escrito {out_h} ({n_uf} UFs, turnos={sorted(horas['turno'].unique().tolist()) if not horas.empty else []})")

    outliers = build_outliers_sem_digital()
    out_o = OUT / "outliers_sem_digital.csv"
    try:
        outliers.to_csv(out_o, index=False)
        print(f"escrito {out_o} ({len(outliers)} seções)")
    except PermissionError:
        alt = OUT / "outliers_sem_digital.new.csv"
        outliers.to_csv(alt, index=False)
        print(f"aviso: {out_o.name} bloqueado — escrito {alt.name} ({len(outliers)} seções)")

    anom = build_anomalias_secao()
    out_a = OUT / "anomalias_secao.csv"
    anom.to_csv(out_a, index=False)
    print(f"escrito {out_a} ({len(anom)} seções)")

    # achados A/B (documental/operacional) — C fica no Parquet completo
    ach_path = REPORTS / "achados_MULTI_1t_2t.parquet"
    if not ach_path.exists():
        parts = [
            pd.read_parquet(p)
            for p in sorted(REPORTS.glob("achados_*_1t_2t.parquet"))
            if "MULTI" not in p.name
        ]
        ach = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
    else:
        ach = pd.read_parquet(ach_path)
    if not ach.empty and "nivel" in ach.columns:
        ab = ach[ach["nivel"].isin(["A", "B"])].copy()
        out_ach = OUT / "achados_ab.csv"
        ab.to_csv(out_ach, index=False)
        print(f"escrito {out_ach} ({len(ab)} fichas A/B)")

    build_secao_lookup()
    build_migracao_site()
    escrever_protocolo()
    build_hw_cadeia()

    # limpa CSVs antigos do site que o painel não usa mais
    for legacy in (
        "resumo_uf_1t.csv",
        "cruzar_oficial_uf_1t.csv",
        "horario_por_hora.csv",
        "horario_por_hora_1t.csv",
        "horario_uf_1t.csv",
        "comparar_turnos_uf_1t_2t.csv",
        "fluxo_br.csv",
    ):
        p = OUT / legacy
        if p.exists():
            p.unlink()
            print(f"removido {p.name}")


_TURNOS = (
    (1, "13", "votos_fa_1t"),
    (1, "22", "votos_fb_1t"),
    (1, "eliminados", "votos_eliminados_1t"),
    (1, "branco", "branco_1t"),
    (1, "nulo", "nulo_1t"),
    (1, "abstencao", "abstencao_1t"),
    (2, "13", "votos_fa_2t"),
    (2, "22", "votos_fb_2t"),
    (2, "branco", "branco_2t"),
    (2, "nulo", "nulo_2t"),
    (2, "abstencao", "abstencao_2t"),
)


def build_migracao_site() -> None:
    """Totais por turno e matriz de transferência para o site."""
    dest = OUT / "migracao"
    dest.mkdir(parents=True, exist_ok=True)
    _escrever_turnos(dest)
    _escrever_conferencia(dest)
    matrizes, fluxos, presentes = _ler_transferencias()
    if matrizes:
        pd.concat(matrizes, ignore_index=True).to_csv(dest / "matriz.csv", index=False)
    else:
        pd.DataFrame(
            columns=["uf", "municipio", "modelo", "origem", "destino", "taxa", "taxa_lo", "taxa_hi"]
        ).to_csv(dest / "matriz.csv", index=False)
    fluxo = _fluxo_com_brasil(fluxos)
    fluxo.to_csv(dest / "fluxo.csv", index=False)
    faltam = [uf for uf in _ufs() if uf not in presentes]
    pd.DataFrame(
        {
            "presentes": [",".join(presentes)],
            "faltam": [",".join(faltam)],
            "n_presentes": [len(presentes)],
            "n_ufs": [len(_ufs())],
        }
    ).to_csv(dest / "cobertura.csv", index=False)
    print(
        f"migração no site: {len(presentes)} estados com matriz, "
        f"{len(faltam)} sem matriz"
    )


def _ufs() -> list[str]:
    from urna_logs.config import UFS

    return list(UFS)


def _escrever_turnos(dest: Path) -> None:
    linhas = []
    for uf in _ufs():
        path = REPORTS / f"comparar_turnos_{uf}_1t_2t.parquet"
        if not path.exists():
            continue
        df = pd.read_parquet(path)
        for turno, grupo, col in _TURNOS:
            if col not in df.columns:
                continue
            linhas.append(
                {
                    "uf": uf,
                    "turno": turno,
                    "grupo": grupo,
                    "votos": int(pd.to_numeric(df[col], errors="coerce").fillna(0).sum()),
                }
            )
    pd.DataFrame(linhas).to_csv(dest / "turnos.csv", index=False)


def _grupo_oficial(votavel: object) -> str:
    codigo = str(votavel).strip().lstrip("0") or "0"
    if codigo == "13":
        return "13"
    if codigo == "22":
        return "22"
    if codigo == "95":
        return "branco"
    if codigo == "96":
        return "nulo"
    return "eliminados"


def _escrever_conferencia(dest: Path) -> None:
    """BU do cruzamento e CSV oficial, por estado e no total."""
    linhas = []
    for turno in (1, 2):
        for uf in _ufs():
            path = REPORTS / f"cruzar_oficial_{uf}_{turno}t.parquet"
            if not path.exists():
                continue
            df = pd.read_parquet(path, columns=["votavel", "votos_bu", "votos_oficial"])
            df["grupo"] = df["votavel"].map(_grupo_oficial)
            soma = df.groupby("grupo", as_index=False)[["votos_bu", "votos_oficial"]].sum()
            for _, row in soma.iterrows():
                linhas.append(
                    {
                        "uf": uf,
                        "turno": turno,
                        "grupo": row["grupo"],
                        "votos_bu": int(row["votos_bu"]),
                        "votos_oficial": int(row["votos_oficial"]),
                    }
                )
    frame = pd.DataFrame(linhas)
    if frame.empty:
        frame.to_csv(dest / "conferencia.csv", index=False)
        return
    pais = (
        frame.groupby(["turno", "grupo"], as_index=False)[["votos_bu", "votos_oficial"]]
        .sum()
    )
    pais.insert(0, "uf", "BR")
    pd.concat([frame, pais], ignore_index=True).to_csv(dest / "conferencia.csv", index=False)


def _ler_transferencias() -> tuple[list[pd.DataFrame], list[pd.DataFrame], list[str]]:
    matrizes = []
    fluxos = []
    presentes = []
    for uf in _ufs():
        path = REPORTS / f"transferencia_{uf}.parquet"
        if not path.exists():
            continue
        df = pd.read_parquet(path)
        if "nivel" not in df.columns:
            continue
        presentes.append(uf)
        taxas = df.loc[
            df["modelo"].isin(["brown_payne", "lphom"])
            & df["nivel"].isin(["estado", "municipio"])
        ]
        if not taxas.empty:
            out = taxas.copy()
            mun = out["municipio"].fillna("").astype(str).str.replace(r"\.0$", "", regex=True)
            out["municipio"] = mun.where(out["nivel"] == "municipio", "0")
            out["uf"] = uf
            for col in ("taxa_lo", "taxa_hi"):
                if col not in out.columns:
                    out[col] = pd.NA
            matrizes.append(
                out[["uf", "municipio", "modelo", "origem", "destino", "taxa", "taxa_lo", "taxa_hi"]]
            )
        soma = df.loc[df["nivel"] == "estado_soma"].copy()
        if not soma.empty:
            soma["uf"] = uf
            fluxos.append(soma)
    return matrizes, fluxos, presentes


def _fluxo_com_brasil(partes: list[pd.DataFrame]) -> pd.DataFrame:
    colunas = ["uf", "modelo", "origem", "destino", "votos", "taxa", "taxa_lo", "taxa_hi"]
    if not partes:
        return pd.DataFrame(columns=colunas)
    frames = []
    for parte in partes:
        bloco = parte.copy()
        for col in ("votos", "taxa", "taxa_lo", "taxa_hi", "se"):
            if col not in bloco.columns:
                bloco[col] = pd.NA
        frames.append(bloco[["uf", "modelo", "origem", "destino", "votos", "taxa", "taxa_lo", "taxa_hi", "se"]])
    base = pd.concat(frames, ignore_index=True)
    pais = []
    z = 1.959963984540054
    for (modelo, origem, destino), g in base.groupby(["modelo", "origem", "destino"]):
        votos = float(pd.to_numeric(g["votos"], errors="coerce").fillna(0).sum())
        total_origem = float(
            pd.to_numeric(
                base.loc[(base["modelo"] == modelo) & (base["origem"] == origem), "votos"],
                errors="coerce",
            ).fillna(0).sum()
        )
        taxa = (votos / total_origem) if total_origem else pd.NA
        ses = pd.to_numeric(g["se"], errors="coerce")
        se = pd.NA
        if votos > 0 and ses.notna().all():
            var = float(((pd.to_numeric(g["votos"], errors="coerce").fillna(0) ** 2) * (ses ** 2)).sum())
            se = var**0.5 / votos
        lo = hi = pd.NA
        if pd.notna(se) and pd.notna(taxa):
            lo = max(0.0, float(taxa) - z * float(se))
            hi = min(1.0, float(taxa) + z * float(se))
        pais.append(
            {
                "uf": "BR",
                "modelo": modelo,
                "origem": origem,
                "destino": destino,
                "votos": votos,
                "taxa": taxa,
                "taxa_lo": lo,
                "taxa_hi": hi,
            }
        )
    return pd.concat([base[colunas], pd.DataFrame(pais)], ignore_index=True)


_MODELOS = {"13": "UE2013", "15": "UE2015", "20": "UE2020", "22": "UE2022"}


def _parte_join(join_key: str) -> tuple[int, int, int] | None:
    partes = str(join_key).split(":")
    if len(partes) != 4:
        return None
    try:
        return int(partes[1]), int(partes[2]), int(partes[3])
    except ValueError:
        return None


def build_hw_cadeia() -> None:
    """Agrega verificar-vsc por UF e turno e grava o selo por seção.

    Não grava votos. Cadeia fechada é Ed521 conferido, ou ECDSA cuja mensagem
    já diz que a AC URNA publicada conferiu. Relatório sem a coluna hw_cadeia
    fica no bloco anterior. Relatório com cadeia pendente foi gravado antes
    de fixar o certificado publicado.
    """
    from urna_logs.config import UFS

    OUT.mkdir(parents=True, exist_ok=True)
    secao_dir = OUT / "secao"
    secao_dir.mkdir(parents=True, exist_ok=True)
    resumo = []
    por_uf: dict[str, list[dict]] = {uf: [] for uf in UFS}

    for path in sorted(REPORTS.glob("verificar_vsc_*_*t.csv")):
        if "MULTI" in path.name:
            continue
        df = pd.read_csv(path, dtype=str)
        if df.empty or "uf" not in df.columns or "turno" not in df.columns:
            continue
        uf = str(df["uf"].iloc[0])
        turno = int(df["turno"].iloc[0])
        modelo = df["modelo_hw"].fillna("")
        alg = df["alg_hw"].fillna("")
        hash_fail = pd.to_numeric(df["n_hash_fail"], errors="coerce").fillna(0)
        criticos = df["criticos_ok"].fillna("") == "True"
        hw_txt = df["hw_sig_ok"].fillna("")
        hw_ok = hw_txt == "True"
        hw_falhou = hw_txt == "False"
        nivel = pd.to_numeric(df["nivel_ok"], errors="coerce").fillna(0)
        tem = df["tem_vsc"].fillna("") == "True"
        parse = df["parse_ok"].fillna("") == "True"
        verificadas = tem & parse
        hashes_ok = verificadas & (hash_fail == 0) & criticos
        cadeia_col = df["hw_cadeia"] if "hw_cadeia" in df.columns else pd.Series([""] * len(df))
        msg = df["hw_sig_msg"].fillna("") if "hw_sig_msg" in df.columns else pd.Series([""] * len(df))
        ecdsa_ok = msg.str.startswith("ECDSA ok") | (cadeia_col == "ok") & modelo.isin(["13", "15"])
        ed521 = (
            hashes_ok
            & modelo.isin(["20", "22"])
            & (alg == "4")
            & hw_ok
            & (nivel >= 2)
        )
        ecdsa_fecha = hashes_ok & modelo.isin(["13", "15"]) & (alg == "2") & ecdsa_ok & hw_ok
        fechada = ed521 | ecdsa_fecha
        antiga = "hw_cadeia" not in df.columns
        ecdsa_hash = hashes_ok & modelo.isin(["13", "15"]) & (alg == "2") & ~fechada
        if antiga:
            bloco = "anterior"
            aberta = ecdsa_hash
        elif bool((cadeia_col == "pendente").any()):
            bloco = "pre_ac"
            aberta = ecdsa_hash
        else:
            bloco = "novo"
            aberta = ecdsa_hash & (cadeia_col == "pendente")
        falha_cadeia = hashes_ok & ~fechada & ~aberta & (
            (cadeia_col == "falha") | hw_falhou
        )
        hash_falhou = verificadas & ~hashes_ok
        fora = verificadas & ~hash_falhou & ~fechada & ~aberta & ~falha_cadeia
        classe_pre = bloco in {"anterior", "pre_ac"}

        linhas = []
        for i, rec in enumerate(df.itertuples(index=False)):
            if not bool(verificadas.iloc[i]):
                continue
            chave = _parte_join(getattr(rec, "join_key"))
            if chave is None:
                continue
            mun, zona, secao = chave
            if bool(fechada.iloc[i]):
                rotulo = "fechada"
            elif bool(aberta.iloc[i]) and (antiga or classe_pre):
                rotulo = "nao_reprocessada"
            elif bool(aberta.iloc[i]):
                rotulo = "aberta"
            elif bool(falha_cadeia.iloc[i]):
                rotulo = "falha"
            elif bool(fora.iloc[i]):
                rotulo = "nao_conferida"
            else:
                rotulo = ""
            linhas.append(
                {
                    "municipio": mun,
                    "zona": zona,
                    "secao": secao,
                    "turno": turno,
                    "modelo": _MODELOS.get(str(modelo.iloc[i]), str(modelo.iloc[i])),
                    "cadeia": rotulo,
                    "hash": "ok" if bool(hashes_ok.iloc[i]) else "falhou",
                }
            )
        por_uf.setdefault(uf, []).extend(linhas)
        n = int(verificadas.sum())
        resumo.append(
            {
                "uf": uf,
                "turno": turno,
                "secoes": n,
                "hash_ok": int(hashes_ok.sum()),
                "hash_falhou": int(hash_falhou.sum()),
                "cadeia_fechada": int(fechada.sum()),
                "cadeia_aberta": int(aberta.sum()),
                "fora": int(fora.sum()),
                "n_ue2013": int((verificadas & (modelo == "13")).sum()),
                "n_ue2015": int((verificadas & (modelo == "15")).sum()),
                "n_ue2020": int((verificadas & (modelo == "20")).sum()),
                "n_ue2022": int((verificadas & (modelo == "22")).sum()),
                "verificador": "anterior" if antiga else "novo",
                "bloco": bloco,
            }
        )

    frame = pd.DataFrame(resumo)
    if not frame.empty:
        frame = frame.sort_values(["turno", "uf"])
    out = OUT / "hw_cadeia.csv"
    frame.to_csv(out, index=False)

    cobertura = []
    for uf in UFS:
        for turno in (1, 2):
            hit = frame[(frame["uf"] == uf) & (frame["turno"] == turno)] if not frame.empty else frame
            secoes = int(hit["secoes"].iloc[0]) if len(hit) else 0
            bloco = str(hit["bloco"].iloc[0]) if len(hit) else ""
            cobertura.append({"uf": uf, "turno": turno, "secoes": secoes, "bloco": bloco})
    out_c = OUT / "hw_cobertura.csv"
    pd.DataFrame(cobertura).to_csv(out_c, index=False)

    cabecalho = ["municipio", "zona", "secao", "turno", "modelo", "cadeia", "hash"]
    for uf in UFS:
        destino = secao_dir / f"hw_{uf}.csv"
        linhas = por_uf.get(uf) or []
        pd.DataFrame(linhas, columns=cabecalho).to_csv(destino, index=False)
    print(f"escrito {out} ({len(frame)} linhas)")
    print(f"escrito {out_c} ({len(cobertura)} UF×turno)")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "migracao":
        build_migracao_site()
    elif len(sys.argv) > 1 and sys.argv[1] == "protocolo":
        escrever_protocolo()
    elif len(sys.argv) > 1 and sys.argv[1] == "secao":
        build_secao_lookup()
    elif len(sys.argv) > 1 and sys.argv[1] == "hw":
        build_hw_cadeia()
    else:
        main()
