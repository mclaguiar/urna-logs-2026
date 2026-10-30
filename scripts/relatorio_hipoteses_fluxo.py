"""
Relatório didático: hipóteses de fluxo 1º→2º por UF + Brasil.

Usa comparar_turnos_* + taxas IPF (fluxo_taxas_* se existir; senão calcula
ponto IPF na hora, sem bootstrap — o IC fica só onde o CSV de taxas existe).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from urna_logs.config import REPORTS_DIR, UFS, ensure_dirs
from urna_logs.fluxo_ecologico import (
    ORIGENS_FOCO,
    DESTINOS,
    attach_ipf_flows,
    compute_bounds_frame,
    load_compare,
    _weighted_rates,
)

ORIGEM_LABEL = {
    "elim": "Eliminados",
    "branco": "Branco",
    "nulo": "Nulo",
    "abst": "Abstenção (1º)",
}
DEST_LABEL = {
    "fa": "Fa (13)",
    "fb": "Fb (22)",
    "branco": "Branco",
    "nulo": "Nulo",
    "abst": "Abstenção (2º)",
}


def _rates_for_uf(uf: str, bounds: pd.DataFrame) -> dict[str, float]:
    csv = REPORTS_DIR / f"fluxo_taxas_{uf}_1t_2t.csv"
    if csv.exists():
        d = pd.read_csv(csv).set_index("taxa")["estimate"]
        return {k: float(d[k]) for k in d.index if str(k).startswith("p_")}
    return {str(k): float(v) for k, v in _weighted_rates(bounds).items()}


def _uf_block(uf: str) -> dict | None:
    compare = load_compare(uf, 1, 2)
    if compare is None:
        return None
    ambos = compare[compare["status"] == "ambos"].copy()
    if ambos.empty:
        return None

    def s(col: str) -> float:
        return float(ambos[col].fillna(0).sum()) if col in ambos.columns else 0.0

    apt1, apt2 = s("aptos_1t"), s("aptos_2t")
    comp1, comp2 = s("comparecimento_1t"), s("comparecimento_2t")
    fa1, fa2 = s("votos_fa_1t"), s("votos_fa_2t")
    fb1, fb2 = s("votos_fb_1t"), s("votos_fb_2t")
    elim = s("votos_eliminados_1t")
    b1, b2 = s("branco_1t"), s("branco_2t")
    n1, n2 = s("nulo_1t"), s("nulo_2t")
    abst1, abst2 = apt1 - comp1, apt2 - comp2

    bounds = attach_ipf_flows(compute_bounds_frame(compare))
    rates = _rates_for_uf(uf, bounds)
    origins = {"elim": elim, "branco": b1, "nulo": n1, "abst": abst1}
    flows: dict[str, dict[str, float]] = {}
    for o, n in origins.items():
        flows[o] = {}
        for d in DESTINOS:
            p = float(rates.get(f"p_{o}_to_{d}", 0.0) or 0.0)
            flows[o][d] = n * p

    forced_fa = int(bounds["elim_forced_fa"].sum()) if "elim_forced_fa" in bounds else 0
    forced_fb = int(bounds["elim_forced_fb"].sum()) if "elim_forced_fb" in bounds else 0
    taxas_csv = (REPORTS_DIR / f"fluxo_taxas_{uf}_1t_2t.csv").exists()

    return {
        "uf": uf,
        "secoes": len(ambos),
        "taxas_com_ic": taxas_csv,
        "aptos_1t": apt1,
        "aptos_2t": apt2,
        "comp_1t": comp1,
        "comp_2t": comp2,
        "fa_1t": fa1,
        "fa_2t": fa2,
        "fb_1t": fb1,
        "fb_2t": fb2,
        "elim_1t": elim,
        "branco_1t": b1,
        "branco_2t": b2,
        "nulo_1t": n1,
        "nulo_2t": n2,
        "abst_1t": abst1,
        "abst_2t": abst2,
        "delta_fa": fa2 - fa1,
        "delta_fb": fb2 - fb1,
        "delta_comp": comp2 - comp1,
        "ganho_finalistas": (fa2 - fa1) + (fb2 - fb1),
        "flows": flows,
        "origins": origins,
        "rates": rates,
        "forced_fa": forced_fa,
        "forced_fb": forced_fb,
    }


def _fmt_int(x: float) -> str:
    return f"{int(round(x)):,}".replace(",", ".")


def _fmt_pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def _h1_label(flows: dict) -> str:
    e13 = flows["elim"]["fa"]
    e22 = flows["elim"]["fb"]
    if e22 > e13 * 1.25:
        return "H1 favorecida (Elim→22 > Elim→13)"
    if e13 > e22 * 1.25:
        return "H2 favorecida (Elim→13 > Elim→22)"
    return "H1/H2 equilibradas"


def build_report(blocks: list[dict]) -> str:
    lines: list[str] = []
    lines += [
        "# Hipóteses de fluxo 1º→2º — por UF e Brasil",
        "",
        "Estimativa ecológica (IPF por seção → taxas da UF × estoques do 1º).",
        "Fa = **13**, Fb = **22**. Não é migração eleitor a eleitor.",
        "",
        "| Hipótese | Ideia |",
        "|---|---|",
        "| **H1** | Eliminados do 1º → sobretudo **22** (compatível com apoios públicos) |",
        "| **H2** | Eliminados → sobretudo **13** |",
        "| **H3** | Eliminados → abstenção no 2º |",
        "| **H4** | Branco/nulo do 1º migram para finalistas |",
        "| **H5** | Quem se absteve no 1º vota no 2º (composição estimada) |",
        "| **H6** | Fluxo *forçado* pelos bounds Duncan–Davis (lim. inf. > 50%) |",
        "| **H7** | Abstenção seletiva (só contextual; ver `fluxo_ecologico_*.md`) |",
        "",
        "Votos estimados = `estoque_origem_1º × taxa_IPF`. "
        "Onde existe `fluxo_taxas_*`, a taxa é a mesma do relatório oficial (com IC lá); "
        "caso contrário, ponto IPF recalculado neste script.",
        "",
    ]

    # --- resumo nacional antecipado (preenche depois) ---
    br = _aggregate(blocks)

    lines += [
        "## Visão rápida — Eliminados → 13 vs 22 (todas as UFs)",
        "",
        "| UF | Elim 1º | →13 (est.) | % | →22 (est.) | % | →abst (est.) | % | Leitura |",
        "|:--:|--:|--:|--:|--:|--:|--:|--:|---|",
    ]
    for b in blocks:
        e = b["origins"]["elim"]
        f = b["flows"]["elim"]
        p13 = f["fa"] / e if e else 0
        p22 = f["fb"] / e if e else 0
        pa = f["abst"] / e if e else 0
        lines.append(
            f"| {b['uf']} | {_fmt_int(e)} | {_fmt_int(f['fa'])} | {_fmt_pct(p13)} | "
            f"{_fmt_int(f['fb'])} | {_fmt_pct(p22)} | {_fmt_int(f['abst'])} | {_fmt_pct(pa)} | "
            f"{_h1_label(b['flows'])} |"
        )
    e = br["origins"]["elim"]
    f = br["flows"]["elim"]
    lines.append(
        f"| **BR** | **{_fmt_int(e)}** | **{_fmt_int(f['fa'])}** | "
        f"**{_fmt_pct(f['fa']/e if e else 0)}** | **{_fmt_int(f['fb'])}** | "
        f"**{_fmt_pct(f['fb']/e if e else 0)}** | **{_fmt_int(f['abst'])}** | "
        f"**{_fmt_pct(f['abst']/e if e else 0)}** | **{_h1_label(br['flows'])}** |"
    )
    lines += ["", "---", ""]

    # --- por UF ---
    for b in blocks:
        lines += _section_uf(b)

    # --- Brasil ---
    lines += _section_uf(br, title="Brasil (soma das UFs)")

    lines += _didatico(br, blocks)
    return "\n".join(lines) + "\n"


def _aggregate(blocks: list[dict]) -> dict:
    keys = [
        "secoes",
        "aptos_1t",
        "aptos_2t",
        "comp_1t",
        "comp_2t",
        "fa_1t",
        "fa_2t",
        "fb_1t",
        "fb_2t",
        "elim_1t",
        "branco_1t",
        "branco_2t",
        "nulo_1t",
        "nulo_2t",
        "abst_1t",
        "abst_2t",
        "forced_fa",
        "forced_fb",
    ]
    out = {k: sum(b[k] for b in blocks) for k in keys}
    out["uf"] = "BR"
    out["taxas_com_ic"] = all(b["taxas_com_ic"] for b in blocks)
    out["delta_fa"] = out["fa_2t"] - out["fa_1t"]
    out["delta_fb"] = out["fb_2t"] - out["fb_1t"]
    out["delta_comp"] = out["comp_2t"] - out["comp_1t"]
    out["ganho_finalistas"] = out["delta_fa"] + out["delta_fb"]
    origins = {
        "elim": out["elim_1t"],
        "branco": out["branco_1t"],
        "nulo": out["nulo_1t"],
        "abst": out["abst_1t"],
    }
    flows = {o: {d: 0.0 for d in DESTINOS} for o in ORIGENS_FOCO}
    for b in blocks:
        for o in ORIGENS_FOCO:
            for d in DESTINOS:
                flows[o][d] += b["flows"][o][d]
    # taxas implícitas Brasil = fluxo / origem
    rates = {}
    for o in ORIGENS_FOCO:
        n = origins[o]
        for d in DESTINOS:
            rates[f"p_{o}_to_{d}"] = (flows[o][d] / n) if n else 0.0
    out["origins"] = origins
    out["flows"] = flows
    out["rates"] = rates
    return out


def _section_uf(b: dict, title: str | None = None) -> list[str]:
    uf = b["uf"]
    title = title or f"{uf}"
    ic = "taxas com IC (`fluxo_taxas`)" if b["taxas_com_ic"] else "ponto IPF (sem IC neste arquivo)"
    lines = [
        f"## {title}",
        "",
        f"Seções em ambos os turnos: **{_fmt_int(b['secoes'])}** · fonte de taxas: {ic}.",
        "",
        "### Totais observados (BU / audit)",
        "",
        "| | 1º | 2º | Δ |",
        "|---|---:|---:|---:|",
        f"| Aptos | {_fmt_int(b['aptos_1t'])} | {_fmt_int(b['aptos_2t'])} | {_fmt_int(b['aptos_2t']-b['aptos_1t'])} |",
        f"| Comparecimento | {_fmt_int(b['comp_1t'])} | {_fmt_int(b['comp_2t'])} | {_fmt_int(b['delta_comp'])} |",
        f"| Fa (13) | {_fmt_int(b['fa_1t'])} | {_fmt_int(b['fa_2t'])} | {_fmt_int(b['delta_fa'])} |",
        f"| Fb (22) | {_fmt_int(b['fb_1t'])} | {_fmt_int(b['fb_2t'])} | {_fmt_int(b['delta_fb'])} |",
        f"| Eliminados | {_fmt_int(b['elim_1t'])} | — | — |",
        f"| Branco | {_fmt_int(b['branco_1t'])} | {_fmt_int(b['branco_2t'])} | {_fmt_int(b['branco_2t']-b['branco_1t'])} |",
        f"| Nulo | {_fmt_int(b['nulo_1t'])} | {_fmt_int(b['nulo_2t'])} | {_fmt_int(b['nulo_2t']-b['nulo_1t'])} |",
        f"| Abstenção | {_fmt_int(b['abst_1t'])} | {_fmt_int(b['abst_2t'])} | {_fmt_int(b['abst_2t']-b['abst_1t'])} |",
        "",
        f"Ganho líquido dos finalistas (Δ13+Δ22): **{_fmt_int(b['ganho_finalistas'])}**.",
        "",
        "### Fluxos estimados (hipóteses H1–H5)",
        "",
    ]
    for o in ORIGENS_FOCO:
        n = b["origins"][o]
        lines += [
            f"#### Origem: {ORIGEM_LABEL[o]} = {_fmt_int(n)}",
            "",
            "| Destino 2º | % | Votos est. | Hipótese |",
            "|---|---:|---:|---|",
        ]
        for d in DESTINOS:
            p = b["rates"].get(f"p_{o}_to_{d}", 0.0)
            v = b["flows"][o][d]
            hip = ""
            if o == "elim" and d == "fb":
                hip = "H1"
            elif o == "elim" and d == "fa":
                hip = "H2"
            elif o == "elim" and d == "abst":
                hip = "H3"
            elif o in ("branco", "nulo") and d in ("fa", "fb"):
                hip = "H4"
            elif o == "abst" and d in ("fa", "fb"):
                hip = "H5"
            lines.append(
                f"| {DEST_LABEL[d]} | {_fmt_pct(p)} | {_fmt_int(v)} | {hip} |"
            )
        lines.append("")
    lines += [
        "### H6 — seções com fluxo Elim *forçado* (bounds)",
        "",
        f"- Elim → 13 forçado: **{b['forced_fa']}** seções",
        f"- Elim → 22 forçado: **{b['forced_fb']}** seções",
        "",
        f"**Leitura H1/H2:** {_h1_label(b['flows'])}.",
        "",
        "---",
        "",
    ]
    return lines


def _didatico(br: dict, blocks: list[dict]) -> list[str]:
    e = br["origins"]["elim"]
    f = br["flows"]["elim"]
    p22 = f["fb"] / e if e else 0
    p13 = f["fa"] / e if e else 0
    n_h1 = sum(1 for b in blocks if "H1 favorecida" in _h1_label(b["flows"]))
    n_h2 = sum(1 for b in blocks if "H2 favorecida" in _h1_label(b["flows"]))
    n_eq = len(blocks) - n_h1 - n_h2
    return [
        "## Explicação didática (como ler este relatório)",
        "",
        "### 1. O que é fato e o que é modelo",
        "",
        "A primeira tabela de cada UF (**Totais observados**) vem do boletim de urna "
        "agregado por seção. Soma 13+22+eliminados+branco+nulo = comparecimento do 1º; "
        "no 2º só restam 13, 22, branco e nulo. Isso **não depende** de hipótese.",
        "",
        "A segunda parte (**Fluxos estimados**) responde: *se* montarmos uma matriz que "
        "fecha os totais de origem e destino seção a seção (IPF), qual a taxa média da UF "
        "e quantos votos isso implica? É a melhor *história contábil* sob a semente de "
        "independência — **não** um censo de eleitores.",
        "",
        "### 2. Por que não dá para “provar” migração",
        "",
        "Em cada seção, infinitas matrizes diferentes podem gerar os mesmos totais "
        "(sistema subdeterminado). Duncan–Davis só diz o intervalo possível; H6 conta "
        "quantas seções têm intervalo tão apertado que *quase* força Elim→13 ou Elim→22. "
        "Quando H6 ≈ 0, a narrativa política **não** está matematicamente obrigada pelos totais.",
        "",
        "### 3. Ligando hipóteses aos números",
        "",
        f"- **H1 (apoios ao 22):** no Brasil agregado, dos **{_fmt_int(e)}** votos em "
        f"eliminados no 1º, o modelo aloca **{_fmt_int(f['fb'])}** (**{_fmt_pct(p22)}**) "
        f"ao 22 e **{_fmt_int(f['fa'])}** (**{_fmt_pct(p13)}**) ao 13. "
        f"UFs com H1 favorecida: **{n_h1}**; H2: **{n_h2}**; equilibradas: **{n_eq}**.",
        f"- **H3:** **{_fmt_int(f['abst'])}** eliminados estimados como abstenção no 2º "
        f"(**{_fmt_pct(f['abst']/e if e else 0)}**) — parte do “sumiço” sem ir a finalista.",
        "- **H4:** veja blocos Branco e Nulo → Fa/Fb em cada UF; em muitos estados o "
        "padrão espelha H1 (mais para 22), mas não em todos.",
        "- **H5:** abstenção do 1º **não é voto**; a linha é composição *compatível* com "
        "quem entra/sai do comparecimento. Se o comparecimento cai (Δ negativo), H5 não "
        "significa “milhões de estreantes líquidos” — o IPF redistribui margens.",
        f"- **H6:** Brasil soma **{br['forced_fa']}** seções forçadas →13 e "
        f"**{br['forced_fb']}** →22. Poucas forçadas = pouca identificação forte.",
        "",
        "### 4. Como o Brasil foi somado",
        "",
        "Totais = soma das UFs. Fluxos = soma dos fluxos estimados de cada UF "
        "(cada estado com *sua* taxa). A % Brasil = fluxo_BR / estoque_BR — "
        "média **ponderada** pelo tamanho do eleitorado de origem, não média simples de %.",
        "",
        "### 5. Escopo do modelo",
        "",
        "- Totais observados fecham a conta do BU; fluxos IPF são **uma** decomposição "
        "factível (outras nos bounds Duncan–Davis também fecham).",
        "- Sem microdados de eleitor: taxas médias e ICs descrevem o agregado, "
        "não trajetórias individuais.",
        "- RDV≡BU≡CSV e estas taxas são camadas distintas "
        "(consistência de arquivo ≠ identificação de fluxo).",
        "- Leitura de razoabilidade (H1/H2/…): comparar taxas e forçados; "
        "a conclusão interpretativa fica com o leitor.",
        "",
        "### 6. Arquivos para reproduzir",
        "",
        "```bash",
        "urna-logs comparar-turnos --ufs ALL",
        "urna-logs fluxo-ecologico --ufs ALL   # grava fluxo_taxas_* com IC",
        "python scripts/relatorio_hipoteses_fluxo.py",
        "```",
        "",
        f"Saída: `reports/hipoteses_fluxo_1t_2t.md` · resumo CSV ao lado.",
        "",
    ]


def write_csv(blocks: list[dict], br: dict) -> Path:
    rows = []
    for b in list(blocks) + [br]:
        row = {
            "uf": b["uf"],
            "secoes": b["secoes"],
            "elim_1t": round(b["origins"]["elim"]),
            "elim_to_fa": round(b["flows"]["elim"]["fa"]),
            "elim_to_fb": round(b["flows"]["elim"]["fb"]),
            "elim_to_abst": round(b["flows"]["elim"]["abst"]),
            "p_elim_to_fa": b["rates"].get("p_elim_to_fa"),
            "p_elim_to_fb": b["rates"].get("p_elim_to_fb"),
            "p_elim_to_abst": b["rates"].get("p_elim_to_abst"),
            "delta_fa": round(b["delta_fa"]),
            "delta_fb": round(b["delta_fb"]),
            "delta_comp": round(b["delta_comp"]),
            "leitura_h1_h2": _h1_label(b["flows"]),
            "forced_fa": b["forced_fa"],
            "forced_fb": b["forced_fb"],
        }
        rows.append(row)
    out = REPORTS_DIR / "hipoteses_fluxo_resumo_1t_2t.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    return out


def main() -> int:
    ensure_dirs()
    blocks: list[dict] = []
    missing: list[str] = []
    for uf in UFS:
        print(f"… {uf}", flush=True)
        b = _uf_block(uf)
        if b is None:
            missing.append(uf)
            continue
        blocks.append(b)
    if not blocks:
        print("Nenhum comparar_turnos_* encontrado.", file=sys.stderr)
        return 1
    br = _aggregate(blocks)
    md = build_report(blocks)
    out_md = REPORTS_DIR / "hipoteses_fluxo_1t_2t.md"
    out_md.write_text(md, encoding="utf-8")
    out_csv = write_csv(blocks, br)
    print(f"OK: {out_md}")
    print(f"OK: {out_csv}")
    if missing:
        print("Sem comparar:", ", ".join(missing))
    print(
        f"BR Elim→22: {br['flows']['elim']['fb']:.0f} "
        f"({100*br['rates']['p_elim_to_fb']:.1f}%) · "
        f"Elim→13: {br['flows']['elim']['fa']:.0f} "
        f"({100*br['rates']['p_elim_to_fa']:.1f}%)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
