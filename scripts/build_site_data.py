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


def _sem_digital_por_uf() -> pd.DataFrame:
    rows: list[dict] = []
    for path in sorted(REPORTS.glob("by_municipio_*_1t.csv")):
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
                    "municipios_1t": int(df["municipio"].nunique()),
                    "urnas_1t": int(df["urnas"].sum()),
                    "comparecimento_1t": int(df["comparecimento"].sum()),
                    "pct_sem_digital_1t": None,
                    "com_detalhe_bio_1t": False,
                }
            )
            continue
        comparecimento = int(com["comparecimento"].sum())
        sem_digital = int(com["sem_digital"].sum())
        rows.append(
            {
                "uf": uf,
                "municipios_1t": int(com["municipio"].nunique()),
                "urnas_1t": int(com["urnas"].sum()),
                "comparecimento_1t": comparecimento,
                "pct_sem_digital_1t": round(100 * sem_digital / comparecimento, 4),
                "com_detalhe_bio_1t": True,
            }
        )
    return pd.DataFrame(rows) if rows else pd.DataFrame()


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
        "mensagem",
    ]
    keep = [c for c in keep if c in df.columns]
    out = df[keep].rename(columns={"pronto": "pronto_2t"})
    return out


def build_painel_uf() -> pd.DataFrame:
    parts = [
        _sem_digital_por_uf(),
        _cruzar_por_uf(),
        _horario_summary_por_turno(1),
        _horario_summary_por_turno(2),
        _comparar_por_uf(),
    ]
    parts = [p for p in parts if p is not None and not p.empty]
    if not parts:
        return pd.DataFrame()

    painel = parts[0]
    for p in parts[1:]:
        painel = painel.merge(p, on="uf", how="outer")

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


def build_horario_por_hora() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for turno in (1, 2):
        multi = REPORTS / f"horario_por_hora_MULTI_{turno}t.csv"
        if multi.exists():
            df = pd.read_csv(multi)
        else:
            parts = [
                pd.read_csv(p)
                for p in sorted(REPORTS.glob(f"horario_por_hora_*_{turno}t.csv"))
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
    """Top seções por % sem digital (1º turno) — indicador de risco até existir Δ 2º."""
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
        top = ok.nlargest(OUTLIERS_PER_UF, "pct_sem_digital")
        rows.append(
            top[
                [
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
                ]
            ]
        )
    if not rows:
        return pd.DataFrame()
    all_top = pd.concat(rows, ignore_index=True)
    all_top = all_top.sort_values("pct_sem_digital", ascending=False).head(OUTLIERS_MAX)
    # nomes de município, se houver cache
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


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    painel = build_painel_uf()
    out_p = OUT / "painel_uf.csv"
    painel.to_csv(out_p, index=False)
    print(f"escrito {out_p} ({len(painel)} UFs)")

    horas = build_horario_por_hora()
    out_h = OUT / "horario_por_hora.csv"
    horas.to_csv(out_h, index=False)
    n_uf = int(horas["uf"].nunique()) if not horas.empty else 0
    print(f"escrito {out_h} ({n_uf} UFs, turnos={sorted(horas['turno'].unique().tolist()) if not horas.empty else []})")

    outliers = build_outliers_sem_digital()
    out_o = OUT / "outliers_sem_digital.csv"
    outliers.to_csv(out_o, index=False)
    print(f"escrito {out_o} ({len(outliers)} seções)")

    # limpa CSVs antigos do site que o painel não usa mais
    for legacy in (
        "resumo_uf_1t.csv",
        "cruzar_oficial_uf_1t.csv",
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
