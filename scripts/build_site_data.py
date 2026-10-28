"""Gera CSVs leves para o painel Quarto (foco 1º×2º + sem digital)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
OUT = ROOT / "site" / "data"

OUTLIERS_PER_UF = 5
OUTLIERS_MAX = 80


def _read_glob(pattern: str, *, multi_name: str | None = None) -> pd.DataFrame | None:
    multi = REPORTS / multi_name if multi_name else None
    if multi and multi.exists():
        return pd.read_csv(multi)
    frames = [
        pd.read_csv(p)
        for p in sorted(REPORTS.glob(pattern))
        if "MULTI" not in p.name
    ]
    if not frames:
        return None
    return pd.concat(frames, ignore_index=True)


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


def _cruzar_por_uf() -> pd.DataFrame:
    df = _read_glob("cruzar_oficial_summary_*_1t.csv", multi_name="cruzar_oficial_summary_MULTI_1t.csv")
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.drop_duplicates(["uf"], keep="last").copy()
    df["uf"] = df["uf"].astype(str).str.upper()
    df["pct_secoes_ok_oficial_1t"] = df.apply(
        lambda r: round(100 * r["secoes_ok"] / r["secoes"], 4) if r.get("secoes") else None,
        axis=1,
    )
    return df.rename(
        columns={
            "secoes": "secoes_oficial_1t",
            "secoes_ok": "secoes_ok_oficial_1t",
            "secoes_divergentes": "secoes_divergentes_1t",
        }
    )[
        [
            "uf",
            "secoes_oficial_1t",
            "secoes_ok_oficial_1t",
            "secoes_divergentes_1t",
            "pct_secoes_ok_oficial_1t",
        ]
    ]


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


def _fluxo_por_uf() -> pd.DataFrame:
    df = _read_glob(
        "fluxo_ecologico_summary_*_1t_2t.csv",
        multi_name="fluxo_ecologico_summary_MULTI_1t_2t.csv",
    )
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.drop_duplicates(["uf"], keep="last").copy()
    df["uf"] = df["uf"].astype(str).str.upper()
    keep = [
        c
        for c in (
            "uf",
            "secoes",
            "secoes_narrow_majority",
            "elim_forced_fa",
            "elim_forced_fb",
            "p_elim_to_fa",
            "p_elim_to_fa_p05",
            "p_elim_to_fa_p95",
            "p_elim_to_fb",
            "p_elim_to_fb_p05",
            "p_elim_to_fb_p95",
            "p_elim_to_abst",
            "p_elim_to_abst_p05",
            "p_elim_to_abst_p95",
            "p_branco_to_fa",
            "p_branco_to_fb",
            "p_nulo_to_fa",
            "p_nulo_to_fb",
            "p_abst_to_fa",
            "p_abst_to_fb",
            "corr_pct_elim_delta_abst",
            "corr_margem1_delta_abst",
        )
        if c in df.columns
    ]
    return df[keep].rename(
        columns={
            "secoes": "fluxo_secoes",
            "secoes_narrow_majority": "fluxo_secoes_narrow",
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
        _cruzar_por_uf(),
        _horario_summary_por_turno(1),
        _horario_summary_por_turno(2),
        _comparar_por_uf(),
        _fluxo_por_uf(),
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
    return out.reset_index(drop=True)


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

    # limpa CSVs antigos do site que o painel não usa mais
    for legacy in (
        "resumo_uf_1t.csv",
        "cruzar_oficial_uf_1t.csv",
        "horario_por_hora.csv",
        "horario_por_hora_1t.csv",
        "horario_uf_1t.csv",
        "comparar_turnos_uf_1t_2t.csv",
    ):
        p = OUT / legacy
        if p.exists():
            p.unlink()
            print(f"removido {p.name}")


if __name__ == "__main__":
    main()
