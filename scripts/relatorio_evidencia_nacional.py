"""
Relatório reproduzível: o que os arquivos públicos permitem concluir (A/B/C).

Não baixa ZIP de novo — só lê `reports/` já gerados pelo pipeline.

Saídas:
  reports/evidencia_nacional_1t_2t.md
  reports/nivel_A_cobertura_nacional.csv
  reports/nivel_ABC_resumo_nacional.csv
  reports/cobertura_pipeline_nacional.csv
  reports/log_x_bu_secao_resumo_nacional.csv   (se houver horario_secao + comparar)
  reports/log_x_bu_secao_outliers_nacional.csv

Uso:
  python scripts/relatorio_evidencia_nacional.py
  python scripts/relatorio_evidencia_nacional.py --hipoteses   # chama relatorio_hipoteses_fluxo
  python scripts/relatorio_evidencia_nacional.py --site        # chama build_site_data
  python scripts/relatorio_evidencia_nacional.py --all
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from urna_logs.config import REPORTS_DIR, UFS, ensure_dirs

TURNOS = (1, 2)

ARTIFACTS = (
    ("audit_parquet", "audit_presidente_{uf}_{t}t.parquet"),
    ("audit_md", "audit_presidente_{uf}_{t}t.md"),
    ("cruzar_md", "cruzar_oficial_{uf}_{t}t.md"),
    ("horario_md", "horario_{uf}_{t}t.md"),
    ("horario_secao", "horario_secao_{uf}_{t}t.parquet"),
    ("comparar", "comparar_turnos_{uf}_1t_2t.parquet"),  # turno ignored
    ("achados_md", "achados_{uf}_1t_2t.md"),
    ("achados_pq", "achados_{uf}_1t_2t.parquet"),
    ("fluxo_md", "fluxo_ecologico_{uf}_1t_2t.md"),
    ("fluxo_taxas", "fluxo_taxas_{uf}_1t_2t.csv"),
    ("verificar_vsc", "verificar_vsc_{uf}_{t}t.parquet"),
)


def _int_br(s: str) -> int:
    return int(s.replace(".", "").replace(",", ""))


def parse_audit_md(path: Path) -> dict:
    t = path.read_text(encoding="utf-8")
    out = {"audit_ok": None, "audit_div": None, "audit_urnas": None}
    m = re.search(
        r"Urnas auditadas:\s*\*\*([0-9.,]+)\*\*\s*·\s*OK:\s*\*\*([0-9.,]+)\*\*"
        r"\s*·\s*divergentes/erro:\s*\*\*([0-9.,]+)\*\*",
        t,
    )
    if m:
        out["audit_urnas"] = _int_br(m.group(1))
        out["audit_ok"] = _int_br(m.group(2))
        out["audit_div"] = _int_br(m.group(3))
    return out


def parse_cruzar_md(path: Path) -> dict:
    t = path.read_text(encoding="utf-8")
    out = {"cruzar_secoes": None, "cruzar_ok": None, "cruzar_div": None}
    m = re.search(
        r"Seções:\s*\*\*([0-9.,]+)\*\*\s*·\s*OK:\s*\*\*([0-9.,]+)\*\*"
        r"\s*·\s*divergentes:\s*\*\*([0-9.,]+)\*\*",
        t,
    )
    if m:
        out["cruzar_secoes"] = _int_br(m.group(1))
        out["cruzar_ok"] = _int_br(m.group(2))
        out["cruzar_div"] = _int_br(m.group(3))
    return out


def parse_achados_md(path: Path) -> dict:
    t = path.read_text(encoding="utf-8")

    def grab(label: str) -> int | None:
        m = re.search(rf"{label}[^:]*:\s*\*\*([0-9.,]+)\*\*", t)
        return _int_br(m.group(1)) if m else None

    return {
        "A": grab(r"Nível A"),
        "B": grab(r"Nível B"),
        "C": grab(r"Nível C"),
        "total": grab(r"Total classificado"),
    }


def cobertura_pipeline() -> pd.DataFrame:
    rows = []
    for uf in UFS:
        row: dict = {"uf": uf}
        for key, pat in ARTIFACTS:
            if "{t}" in pat:
                for t in TURNOS:
                    name = pat.format(uf=uf, t=t)
                    row[f"{key}_{t}t"] = (REPORTS_DIR / name).exists()
            else:
                row[key] = (REPORTS_DIR / pat.format(uf=uf)).exists()
        rows.append(row)
    return pd.DataFrame(rows)


def nivel_a_frame() -> pd.DataFrame:
    rows = []
    for uf in UFS:
        for t in TURNOS:
            row = {"uf": uf, "turno": t}
            aud = REPORTS_DIR / f"audit_presidente_{uf}_{t}t.md"
            cruz = REPORTS_DIR / f"cruzar_oficial_{uf}_{t}t.md"
            if aud.exists():
                row.update(parse_audit_md(aud))
            if cruz.exists():
                row.update(parse_cruzar_md(cruz))
            rows.append(row)
    return pd.DataFrame(rows)


def nivel_abc_frame() -> pd.DataFrame:
    rows = []
    for uf in UFS:
        p = REPORTS_DIR / f"achados_{uf}_1t_2t.md"
        if not p.exists():
            rows.append({"uf": uf, "A": None, "B": None, "C": None, "total": None})
            continue
        row = {"uf": uf}
        row.update(parse_achados_md(p))
        rows.append(row)
    return pd.DataFrame(rows)


def log_x_bu_secao(
    *, abs_delta_min: int = 5, top_n: int = 200
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Cruzamento seção: habilitações do dia (horario_secao.hab_total)
    × comparecimento do BU no mesmo turno (comparar_turnos).
    """
    resumo_rows = []
    outlier_parts: list[pd.DataFrame] = []

    for uf in UFS:
        cmp_path = REPORTS_DIR / f"comparar_turnos_{uf}_1t_2t.parquet"
        if not cmp_path.exists():
            continue
        cmp = pd.read_parquet(cmp_path)
        if "join_key" not in cmp.columns:
            continue
        for t in TURNOS:
            hs = REPORTS_DIR / f"horario_secao_{uf}_{t}t.parquet"
            if not hs.exists():
                continue
            hab = pd.read_parquet(hs)
            if "join_key" not in hab.columns or "hab_total" not in hab.columns:
                continue
            col_comp = f"comparecimento_{t}t"
            if col_comp not in cmp.columns:
                continue
            m = hab.merge(
                cmp[["join_key", col_comp]].rename(columns={col_comp: "bu_comparecimento"}),
                on="join_key",
                how="inner",
            )
            if m.empty:
                continue
            m["delta_hab_menos_bu"] = m["hab_total"].astype(float) - m[
                "bu_comparecimento"
            ].astype(float)
            m["abs_delta"] = m["delta_hab_menos_bu"].abs()
            n = len(m)
            exact = int((m["delta_hab_menos_bu"] == 0).sum())
            resumo_rows.append(
                {
                    "uf": uf,
                    "turno": t,
                    "secoes_join": n,
                    "delta_0": exact,
                    "pct_delta_0": round(100 * exact / n, 4) if n else None,
                    "delta_mediano": float(m["delta_hab_menos_bu"].median()),
                    "delta_p05": float(m["delta_hab_menos_bu"].quantile(0.05)),
                    "delta_p95": float(m["delta_hab_menos_bu"].quantile(0.95)),
                    "hab_sum": int(m["hab_total"].sum()),
                    "bu_sum": int(m["bu_comparecimento"].sum()),
                    "delta_sum": int(m["delta_hab_menos_bu"].sum()),
                }
            )
            outs = m.loc[m["abs_delta"] >= abs_delta_min].copy()
            if not outs.empty:
                outs["uf"] = uf
                outs["turno"] = t
                keep = [
                    "uf",
                    "turno",
                    "join_key",
                    "hab_total",
                    "bu_comparecimento",
                    "delta_hab_menos_bu",
                ]
                for opt in ("hab_apos_17h", "hab_historico_outro_dia", "hab_fora_previsto"):
                    if opt in outs.columns:
                        keep.append(opt)
                outlier_parts.append(outs[keep])

    resumo = pd.DataFrame(resumo_rows)
    if outlier_parts:
        outliers = pd.concat(outlier_parts, ignore_index=True)
        outliers = outliers.sort_values("delta_hab_menos_bu", key=abs, ascending=False)
        outliers = outliers.head(top_n)
    else:
        outliers = pd.DataFrame()
    return resumo, outliers


def _extract_divergencias(text: str, *, max_chars: int = 1200) -> str:
    """Puxa o bloco de divergências do Markdown de audit/cruzar."""
    for marker in ("## Divergências / erros", "## Divergências"):
        i = text.find(marker)
        if i >= 0:
            chunk = text[i:]
            nxt = re.search(r"\n## (?!Diverg)", chunk[3:])
            if nxt:
                chunk = chunk[: nxt.start() + 3]
            chunk = chunk.strip()
            if len(chunk) > max_chars:
                return chunk[: max_chars - 20].rstrip() + "\n… (truncado)"
            return chunk
    return ""


def vsc_resumo_nacional() -> pd.DataFrame:
    """Consolida verificar_vsc_*_{t}t.parquet → uma linha por UF/turno."""
    rows = []
    for uf in UFS:
        for t in TURNOS:
            p = REPORTS_DIR / f"verificar_vsc_{uf}_{t}t.parquet"
            if not p.exists():
                continue
            df = pd.read_parquet(p)
            n = len(df)
            rows.append(
                {
                    "uf": uf,
                    "turno": t,
                    "stems": n,
                    "com_vsc": int(df["tem_vsc"].sum()) if n else 0,
                    "parse_ok": int(df["parse_ok"].sum()) if n else 0,
                    "nivel_ge1": int((df["nivel_ok"] >= 1).sum()) if n else 0,
                    "criticos_ok": int(df["criticos_ok"].fillna(False).sum())
                    if n
                    else 0,
                    "hash_fail_stems": int((df["n_hash_fail"] > 0).sum()) if n else 0,
                    "sem_vsc": int((~df["tem_vsc"]).sum()) if n else 0,
                }
            )
    return pd.DataFrame(rows)


def gaps_from_cobertura(cov: pd.DataFrame) -> list[str]:
    gaps = []
    for key in (
        "audit_parquet_1t",
        "audit_parquet_2t",
        "cruzar_md_1t",
        "cruzar_md_2t",
        "comparar",
        "achados_md",
        "horario_secao_1t",
        "horario_secao_2t",
        "fluxo_taxas",
        "verificar_vsc_1t",
        "verificar_vsc_2t",
    ):
        if key not in cov.columns:
            continue
        miss = cov.loc[~cov[key].astype(bool), "uf"].tolist()
        if miss:
            gaps.append(f"{key}: faltam {len(miss)} UF(s) — {', '.join(miss)}")
    gaps.append(
        "`.vsc` nível 2 (assinatura HW Ed521/ECPy): ainda parcial — "
        "nível 1 (hashes) cobre integridade dos arquivos presentes no ZIP"
    )
    return gaps


def build_markdown(
    cov: pd.DataFrame,
    nivel_a: pd.DataFrame,
    abc: pd.DataFrame,
    log_resumo: pd.DataFrame,
    gaps: list[str],
    vsc: pd.DataFrame | None = None,
) -> str:
    lines: list[str] = [
        "# Evidência nacional (arquivos públicos) — 1º×2º",
        "",
        "Gerado por `scripts/relatorio_evidencia_nacional.py` a partir de `reports/`.",
        "Hierarquia: **A** documental · **B** operacional · **C** ecológico/contexto.",
        "",
        "## Síntese (o que os números mostram)",
        "",
    ]

    a_div = int(nivel_a["audit_div"].fillna(0).sum()) if "audit_div" in nivel_a else -1
    c_div = int(nivel_a["cruzar_div"].fillna(0).sum()) if "cruzar_div" in nivel_a else -1
    a_sum = int(abc["A"].fillna(0).sum()) if "A" in abc else -1
    b_sum = int(abc["B"].fillna(0).sum()) if "B" in abc else -1
    c_sum = int(abc["C"].fillna(0).sum()) if "C" in abc else -1

    if a_div == 0 and c_div == 0:
        lines.append(
            "- **Nível A (RDV≡BU e BU≡oficial):** nenhuma divergência contabilizada "
            "nos Markdown de audit/cruzar lidos — arquivos públicos **consistentes entre si** "
            "nas UFs presentes."
        )
    else:
        lines.append(
            f"- **Nível A:** audit divergentes/erro soma={a_div}; "
            f"cruzar divergentes soma={c_div}. Ver CSV e seção «Fichas A» abaixo."
        )
        # Detalhe das UFs com div
        ad = (
            nivel_a["audit_div"].fillna(0)
            if "audit_div" in nivel_a.columns
            else 0
        )
        cd = (
            nivel_a["cruzar_div"].fillna(0)
            if "cruzar_div" in nivel_a.columns
            else 0
        )
        hit = nivel_a[(ad > 0) | (cd > 0)]
        if not hit.empty:
            lines += ["", "### Fichas A (audit / cruzar com divergência)", ""]
            for _, r in hit.iterrows():
                uf, t = r["uf"], int(r["turno"])
                lines.append(f"#### {uf} {t}º turno")
                aud = REPORTS_DIR / f"audit_presidente_{uf}_{t}t.md"
                cruz = REPORTS_DIR / f"cruzar_oficial_{uf}_{t}t.md"
                if aud.exists():
                    block = _extract_divergencias(aud.read_text(encoding="utf-8"))
                    if block:
                        lines += ["", f"Audit (`{aud.name}`):", "", "```", block, "```"]
                if cruz.exists():
                    block = _extract_divergencias(cruz.read_text(encoding="utf-8"))
                    if block:
                        lines += ["", f"Cruzar (`{cruz.name}`):", "", "```", block, "```"]
                lines.append("")
    lines += [
        f"- **Achados classificados:** A={a_sum:,} · B={b_sum:,} · C={c_sum:,} "
        "(seções com ficha; B prioriza revisão operacional).",
        "- **Nível C / fluxo:** ver `hipoteses_fluxo_1t_2t.md` (taxas IPF agregadas, se gerado).",
        "",
        "## Cobertura do pipeline",
        "",
        f"UFs no config: **{len(UFS)}**. "
        f"Comparar presente: **{int(cov['comparar'].sum()) if 'comparar' in cov else 0}**. "
        f"Fluxo taxas: **{int(cov['fluxo_taxas'].sum()) if 'fluxo_taxas' in cov else 0}**.",
        "",
        "Detalhe: `cobertura_pipeline_nacional.csv`.",
        "",
        "## Nível A — audit e cruzar",
        "",
        "| Turno | Audit OK (soma) | Audit div | Cruzar OK | Cruzar div |",
        "|---:|---:|---:|---:|---:|",
    ]
    for t in TURNOS:
        sub = nivel_a[nivel_a["turno"] == t]
        lines.append(
            f"| {t}º | {int(sub['audit_ok'].fillna(0).sum())} | "
            f"{int(sub['audit_div'].fillna(0).sum())} | "
            f"{int(sub['cruzar_ok'].fillna(0).sum())} | "
            f"{int(sub['cruzar_div'].fillna(0).sum())} |"
        )
    lines += [
        "",
        "Por UF/turno: `nivel_A_cobertura_nacional.csv`.",
        "",
        "## Nível B/C — achados",
        "",
        "| UF | A | B | C | Total |",
        "|:--:|--:|--:|--:|--:|",
    ]
    for _, r in abc.sort_values("uf").iterrows():
        def cell(v):
            return "—" if pd.isna(v) else f"{int(v)}"

        lines.append(
            f"| {r['uf']} | {cell(r.get('A'))} | {cell(r.get('B'))} | "
            f"{cell(r.get('C'))} | {cell(r.get('total'))} |"
        )
    lines += [
        f"| **Σ** | **{a_sum}** | **{b_sum}** | **{c_sum}** | "
        f"**{int(abc['total'].fillna(0).sum())}** |",
        "",
        "CSV: `nivel_ABC_resumo_nacional.csv`.",
        "",
        "## `.vsc` — hashes da mídia de resultado",
        "",
    ]
    if vsc is None or vsc.empty:
        lines.append(
            "_Ainda sem `verificar_vsc_*`. Rode "
            "`urna-logs verificar-vsc --ufs ALL --turno 1` (e `--turno 2`)._"
        )
    else:
        lines += [
            "Nível 1: SHA-512 dos arquivos **presentes** no ZIP (bu/rdv/log/…) "
            "bate com `-vota.vsc`. Ausentes no CDN ≠ falha.",
            "",
            "| UF | Turno | Stems | Nível≥1 | Críticos OK | Hash fail | Sem .vsc |",
            "|:--:|---:|---:|---:|---:|---:|---:|",
        ]
        for _, r in vsc.sort_values(["uf", "turno"]).iterrows():
            lines.append(
                f"| {r['uf']} | {int(r['turno'])} | {int(r['stems'])} | "
                f"{int(r['nivel_ge1'])} | {int(r['criticos_ok'])} | "
                f"{int(r['hash_fail_stems'])} | {int(r['sem_vsc'])} |"
            )
        lines += [
            "",
            f"Σ stems: **{int(vsc['stems'].sum())}** · "
            f"nível≥1: **{int(vsc['nivel_ge1'].sum())}** · "
            f"hash fail: **{int(vsc['hash_fail_stems'].sum())}**.",
            "",
            "CSV: `verificar_vsc_resumo_nacional.csv`.",
        ]
    lines += [
        "",
        "## Log × BU (habilitações do dia × comparecimento)",
        "",
    ]
    if log_resumo.empty:
        lines.append(
            "_Sem junção possível (falta `horario_secao_*` ou `comparar_turnos_*`)._"
        )
    else:
        lines += [
            "Por seção: `hab_total` (dia oficial no log) − `comparecimento` (BU). "
            "Delta ≠ 0 é compatível com suspensão sem voto, multi-urna ou gap de join; "
            "avaliar magnitude e concentração por UF.",
            "",
            "| UF | Turno | Seções | Δ=0 (%) | Δ mediano | Hab Σ | BU Σ | Δ Σ |",
            "|:--:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for _, r in log_resumo.sort_values(["uf", "turno"]).iterrows():
            lines.append(
                f"| {r['uf']} | {int(r['turno'])} | {int(r['secoes_join'])} | "
                f"{r['pct_delta_0']} | {r['delta_mediano']:.1f} | "
                f"{int(r['hab_sum'])} | {int(r['bu_sum'])} | {int(r['delta_sum'])} |"
            )
        lines += [
            "",
            "Outliers (|Δ|≥5): `log_x_bu_secao_outliers_nacional.csv`.",
            "Resumo: `log_x_bu_secao_resumo_nacional.csv`.",
        ]

    lines += [
        "",
        "## Lacunas de cobertura / método",
        "",
    ]
    for g in gaps:
        lines.append(f"- {g}")
    lines += [
        "",
        "## Como reproduzir",
        "",
        "```bash",
        "# (opcional) pipeline completo por UF — já deve ter rodado",
        "# urna-logs audit / cruzar-oficial / horario --por-secao / comparar-turnos / achados",
        "",
        "python scripts/relatorio_evidencia_nacional.py",
        "python scripts/relatorio_evidencia_nacional.py --hipoteses   # C: fluxo IPF BR",
        "python scripts/relatorio_evidencia_nacional.py --site        # painel Quarto",
        "python scripts/relatorio_evidencia_nacional.py --all",
        "",
        "# IC bootstrap por UF (lento):",
        "# urna-logs fluxo-ecologico --ufs ALL",
        "```",
        "",
        "## Escopo dos números",
        "",
        "A = consistência entre arquivos públicos; B = seções no extremo da UF "
        "(priorização); C = saldos/taxas agregadas. "
        "Interpretação causal ou jurídica fica com o leitor.",
        "",
    ]
    return "\n".join(lines)


def _run_helper(script: str) -> int:
    cmd = [sys.executable, str(ROOT / "scripts" / script)]
    print("+", " ".join(cmd), flush=True)
    return subprocess.call(cmd, cwd=str(ROOT))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--hipoteses",
        action="store_true",
        help="Também roda scripts/relatorio_hipoteses_fluxo.py",
    )
    parser.add_argument(
        "--site",
        action="store_true",
        help="Também roda scripts/build_site_data.py",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Atalho: --hipoteses --site",
    )
    parser.add_argument(
        "--abs-delta-min",
        type=int,
        default=5,
        help="Limiar |hab−BU| para outliers (default 5)",
    )
    args = parser.parse_args(argv)
    if args.all:
        args.hipoteses = True
        args.site = True

    ensure_dirs()
    print("Cobertura…", flush=True)
    cov = cobertura_pipeline()
    cov.to_csv(REPORTS_DIR / "cobertura_pipeline_nacional.csv", index=False)

    print("Nível A…", flush=True)
    nivel_a = nivel_a_frame()
    nivel_a.to_csv(REPORTS_DIR / "nivel_A_cobertura_nacional.csv", index=False)

    print("Achados A/B/C…", flush=True)
    abc = nivel_abc_frame()
    abc.to_csv(REPORTS_DIR / "nivel_ABC_resumo_nacional.csv", index=False)

    print("Log × BU (seção)…", flush=True)
    log_resumo, log_out = log_x_bu_secao(abs_delta_min=args.abs_delta_min)
    log_resumo.to_csv(REPORTS_DIR / "log_x_bu_secao_resumo_nacional.csv", index=False)
    log_out.to_csv(REPORTS_DIR / "log_x_bu_secao_outliers_nacional.csv", index=False)

    print(".vsc…", flush=True)
    vsc = vsc_resumo_nacional()
    if not vsc.empty:
        vsc.to_csv(REPORTS_DIR / "verificar_vsc_resumo_nacional.csv", index=False)

    gaps = gaps_from_cobertura(cov)
    md = build_markdown(cov, nivel_a, abc, log_resumo, gaps, vsc=vsc)
    out_md = REPORTS_DIR / "evidencia_nacional_1t_2t.md"
    out_md.write_text(md, encoding="utf-8")
    print(f"OK: {out_md}", flush=True)

    if args.hipoteses:
        rc = _run_helper("relatorio_hipoteses_fluxo.py")
        if rc != 0:
            return rc
    if args.site:
        rc = _run_helper("build_site_data.py")
        if rc != 0:
            return rc

    print(
        f"A audit_div={int(nivel_a['audit_div'].fillna(0).sum())} · "
        f"cruzar_div={int(nivel_a['cruzar_div'].fillna(0).sum())} · "
        f"achados A/B/C="
        f"{int(abc['A'].fillna(0).sum())}/"
        f"{int(abc['B'].fillna(0).sum())}/"
        f"{int(abc['C'].fillna(0).sum())}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
