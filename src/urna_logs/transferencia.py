"""Transferência 1º→2º por município.

A seção é a observação. A matriz é da cidade, quando há seções suficientes.
Cidade pequena recebe a matriz do estado. O resumo do estado soma os votos
transferidos, não a média das taxas.

Modelos: Brown e Payne (1986) e lphom (cenário simultaneous). A R×C do piloto
AC ficou de fora: a cadeia curta não concordou com os outros dois.

O Brown e Payne entra com cada seção. O lphom também, até MAX_LINHAS_LPHOM
seções no grupo. Acima disso, soma as seções da mesma zona: o programa
linear do lphom cresce com o quadrado do número de linhas.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.table import Table

from urna_logs.config import REPORTS_DIR, UFS, ensure_dirs

console = Console()

MIN_SECOES = 30
MAX_LINHAS_LPHOM = 2500
CONFIANCA = 0.95
_Z95 = 1.959963984540054
ORIGENS = ("13", "22", "eliminados", "branco", "nulo", "abstencao")
DESTINOS = ("13", "22", "branco", "nulo", "abstencao")
_ORIGEM_COL = {
    "13": "votos_fa_1t",
    "22": "votos_fb_1t",
    "eliminados": "votos_eliminados_1t",
    "branco": "branco_1t",
    "nulo": "nulo_1t",
    "abstencao": "abstencao_1t",
}
_DESTINO_COL = {
    "13": "votos_fa_2t",
    "22": "votos_fb_2t",
    "branco": "branco_2t",
    "nulo": "nulo_2t",
    "abstencao": "abstencao_2t",
}


def rscript_path() -> Path:
    found = shutil.which("Rscript")
    if found:
        return Path(found)
    base = Path(r"C:\Program Files\R")
    if base.exists():
        candidatos = sorted(base.glob("R-*/bin/Rscript.exe"))
        if candidatos:
            return candidatos[-1]
    raise FileNotFoundError(
        "Rscript não encontrado. A transferência usa os pacotes R lphom."
    )


def script_r() -> Path:
    path = Path(__file__).resolve().parent / "r" / "transferencia.R"
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def montar_margens(df: pd.DataFrame) -> pd.DataFrame:
    """Contagens do 1º e do 2º. A diferença de total vai para a abstenção."""
    base = df.loc[df["status"] == "ambos"].copy()
    out = base[["join_key", "municipio", "zona", "secao"]].copy()
    for nome, col in _ORIGEM_COL.items():
        out[f"o_{nome}"] = pd.to_numeric(base[col], errors="coerce").fillna(0).clip(lower=0)
    for nome, col in _DESTINO_COL.items():
        out[f"d_{nome}"] = pd.to_numeric(base[col], errors="coerce").fillna(0).clip(lower=0)
    o_cols = [f"o_{k}" for k in ORIGENS]
    d_cols = [f"d_{k}" for k in DESTINOS]
    so = out[o_cols].sum(axis=1)
    sd = out[d_cols].sum(axis=1)
    n = so.combine(sd, max)
    out["ajuste_1t"] = n - so
    out["ajuste_2t"] = n - sd
    out["o_abstencao"] = out["o_abstencao"] + out["ajuste_1t"]
    out["d_abstencao"] = out["d_abstencao"] + out["ajuste_2t"]
    out["n"] = n
    out = out.loc[out["n"] > 0].copy()
    for col in o_cols + d_cols + ["ajuste_1t", "ajuste_2t", "n"]:
        out[col] = out[col].round(0).astype(int)
    out["municipio"] = out["municipio"].astype(int)
    return out.reset_index(drop=True)


def fonte_por_municipio(n_secoes: pd.Series, min_secoes: int) -> pd.Series:
    """Cidade com seções suficientes estima a própria matriz."""
    return pd.Series(
        ["municipio" if int(n) >= min_secoes else "estado" for n in n_secoes],
        index=n_secoes.index,
    )


def somar_fluxos(margens: pd.DataFrame, taxas: pd.DataFrame) -> pd.DataFrame:
    """Soma votos transferidos com a taxa aplicada em cada cidade."""
    n_mun = margens.groupby("municipio").size()
    fonte = fonte_por_municipio(n_mun, int(taxas["min_secoes"].iloc[0]))
    aplicadas = _taxas_aplicadas(taxas, fonte)
    totais = {
        origem: margens.groupby("municipio")[f"o_{origem}"].sum() for origem in ORIGENS
    }
    blocos = []
    for modelo, sub in aplicadas.groupby("modelo"):
        larga = sub.pivot_table(
            index="municipio", columns=["origem", "destino"], values="taxa"
        )
        celulas = []
        for origem in ORIGENS:
            votos_origem = 0.0
            acumulado = {destino: 0.0 for destino in DESTINOS}
            for mun, votos in totais[origem].items():
                votos_origem += float(votos)
                for destino in DESTINOS:
                    if (origem, destino) not in larga.columns:
                        continue
                    acumulado[destino] += float(votos) * float(larga.loc[mun, (origem, destino)])
            for destino, votos in acumulado.items():
                taxa = (votos / votos_origem) if votos_origem else 0.0
                se = _se_agregado(aplicadas, totais[origem], modelo, origem, destino)
                lo, hi = _limites(taxa, se)
                celulas.append(
                    {
                        "nivel": "estado_soma",
                        "municipio": "",
                        "modelo": modelo,
                        "origem": origem,
                        "destino": destino,
                        "taxa": taxa,
                        "se": se,
                        "taxa_lo": lo,
                        "taxa_hi": hi,
                        "confianca": CONFIANCA if pd.notna(se) else pd.NA,
                        "votos": votos,
                        "n_secoes": int(len(margens)),
                        "r2": pd.NA,
                        "convergencia": pd.NA,
                        "fonte": "soma",
                    }
                )
        blocos.append(pd.DataFrame(celulas))
    return pd.concat(blocos, ignore_index=True)


def _taxas_aplicadas(taxas: pd.DataFrame, fonte: pd.Series) -> pd.DataFrame:
    estado = taxas.loc[taxas["nivel"] == "estado"].copy()
    mun = taxas.loc[taxas["nivel"] == "municipio"].copy()
    partes = []
    for municipio, origem_fonte in fonte.items():
        bloco = estado.copy()
        if origem_fonte == "municipio":
            proprio = mun.loc[mun["municipio"].astype(str) == str(int(municipio))]
            if proprio.empty:
                origem_fonte = "estado"
            else:
                bloco = pd.concat([bloco, proprio], ignore_index=True)
                bloco = bloco.drop_duplicates(
                    ["modelo", "origem", "destino"], keep="last"
                )
        bloco["municipio"] = int(municipio)
        bloco["fonte"] = origem_fonte
        partes.append(bloco)
    if not partes:
        return taxas.iloc[0:0].copy()
    return pd.concat(partes, ignore_index=True)


def _limites(taxa, se) -> tuple:
    if taxa is None or se is None or pd.isna(taxa) or pd.isna(se):
        return pd.NA, pd.NA
    return (
        max(0.0, float(taxa) - _Z95 * float(se)),
        min(1.0, float(taxa) + _Z95 * float(se)),
    )


def _se_agregado(aplicadas: pd.DataFrame, votos_origem: pd.Series, modelo: str, origem: str, destino: str):
    """Erro da taxa somada. Cidades que herdam o estado compartilham o mesmo ajuste."""
    if "se" not in aplicadas.columns:
        return pd.NA
    sub = aplicadas.loc[
        (aplicadas["modelo"] == modelo)
        & (aplicadas["origem"] == origem)
        & (aplicadas["destino"] == destino)
    ]
    if sub.empty:
        return pd.NA
    total = float(votos_origem.sum())
    if total <= 0:
        return pd.NA
    var = 0.0
    herdadas = sub.loc[sub["fonte"] == "estado"]
    if not herdadas.empty:
        ses = pd.to_numeric(herdadas["se"], errors="coerce")
        if ses.isna().any():
            return pd.NA
        votos = float(sum(float(votos_origem.get(int(m), 0.0)) for m in herdadas["municipio"]))
        var += votos**2 * float(ses.iloc[0]) ** 2
    for _, linha in sub.loc[sub["fonte"] == "municipio"].iterrows():
        if pd.isna(linha["se"]):
            return pd.NA
        votos = float(votos_origem.get(int(linha["municipio"]), 0.0))
        var += votos**2 * float(linha["se"]) ** 2
    return var**0.5 / total


def _chamar_r(margens: pd.DataFrame, min_secoes: int) -> pd.DataFrame:
    rscript = rscript_path()
    with tempfile.TemporaryDirectory(prefix="transferencia_") as tmp:
        base = Path(tmp)
        entrada = base / "margens.csv"
        saida = base / "taxas.csv"
        margens.to_csv(entrada, index=False)
        subprocess.run(
            [
                str(rscript),
                "--vanilla",
                str(script_r()),
                str(entrada),
                str(saida),
                str(min_secoes),
                str(MAX_LINHAS_LPHOM),
            ],
            check=True,
        )
        taxas = pd.read_csv(saida)
    taxas["min_secoes"] = min_secoes
    taxas["municipio"] = taxas["municipio"].fillna("").astype(str).str.replace(r"\.0$", "", regex=True)
    return taxas


def _markdown(uf: str, margens: pd.DataFrame, taxas: pd.DataFrame, min_secoes: int) -> str:
    n_mun = margens.groupby("municipio").size()
    fonte = fonte_por_municipio(n_mun, min_secoes)
    proprias = int((fonte == "municipio").sum())
    herdadas = int((fonte == "estado").sum())
    estado = taxas.loc[taxas["nivel"] == "estado"]
    linhas = [
        f"# Transferência 1º→2º — {uf}",
        "",
        f"Seções: **{len(margens):,}**. Cidades: **{len(n_mun):,}**.",
        f"Matriz própria: **{proprias:,}** cidades com pelo menos {min_secoes} seções.",
        f"Matriz do estado: **{herdadas:,}** cidades abaixo disso.",
        "",
        "A seção não estima taxa. Ela entra na matriz da cidade, ou na do estado.",
        "A leitura do estado usa a soma dos votos transferidos nas cidades.",
        "",
        _nota_grao(taxas),
        "",
        "## Leitura",
        "",
        _leitura_estado(taxas),
        "",
        "## Taxa única do estado",
        "",
        _tabela_taxas(estado),
        "",
        "## Estado somado a partir das cidades",
        "",
        _tabela_taxas(taxas.loc[taxas["nivel"] == "estado_soma"]),
        "",
        "## Cidades em que os dois modelos divergem no 13 ou no 22",
        "",
    ]
    divergem = _divergencias(taxas)
    if divergem.empty:
        linhas.append("Nenhuma cidade com matriz própria diverge mais de 5 pontos nessas taxas.")
    else:
        linhas.append("| Cidade | Célula | Brown e Payne | lphom |")
        linhas.append("|---|---|---:|---:|")
        for _, r in divergem.iterrows():
            linhas.append(
                f"| {r['municipio']} | {r['origem']}→{r['destino']} | "
                f"{100 * r['brown_payne']:.1f}% | {100 * r['lphom']:.1f}% |"
            )
    linhas += [
        "",
        "Modelos: Brown e Payne (1986), em cada seção; lphom, cenário simultaneous.",
        f"O lphom usa a seção até {MAX_LINHAS_LPHOM:,} linhas. Acima disso, soma por zona.",
        "O intervalo do Brown e Payne é de 95%. Ele sai dos resíduos das seções em torno do ajuste.",
        "Uma célula presa em 0% ou 100% pode ficar sem intervalo.",
        "A R×C não entra neste comando.",
        "",
    ]
    return "\n".join(linhas)


def _nota_grao(taxas: pd.DataFrame) -> str:
    regra = (
        f"Brown e Payne usa cada seção. "
        f"O lphom usa a seção até {MAX_LINHAS_LPHOM:,} linhas. "
        "Acima disso, soma as seções da mesma zona."
    )
    if "grao" not in taxas.columns:
        return regra
    colunas = ["nivel", "municipio", "grao", "n_unidades", "n_secoes"]
    lp = taxas.loc[taxas["modelo"] == "lphom", colunas].dropna(subset=["grao"])
    lp = lp.drop_duplicates()
    if lp.empty:
        return regra
    frases = [regra]
    estado = lp.loc[lp["nivel"] == "estado"]
    if not estado.empty and str(estado.iloc[0]["grao"]) != "secao":
        linha = estado.iloc[0]
        frases.append(
            f"No estado, o lphom usou {linha['grao']}: "
            f"{int(linha['n_unidades'])} linhas, {int(linha['n_secoes'])} seções."
        )
    cidades = lp.loc[(lp["nivel"] == "municipio") & (lp["grao"].astype(str) != "secao")]
    if not cidades.empty:
        itens = [
            f"{str(r.municipio).removesuffix('.0')} ({r.grao}, {int(r.n_unidades)} linhas, {int(r.n_secoes)} seções)"
            for r in cidades.itertuples(index=False)
        ]
        frases.append("Cidades em que o lphom não usou a seção: " + "; ".join(itens) + ".")
    return " ".join(frases)


def _taxa(taxas: pd.DataFrame, nivel: str, origem: str, destino: str, modelo: str) -> float | None:
    linha = taxas.loc[
        (taxas["nivel"] == nivel)
        & (taxas["origem"] == origem)
        & (taxas["destino"] == destino)
        & (taxas["modelo"] == modelo),
        "taxa",
    ]
    if linha.empty or pd.isna(linha.iloc[0]):
        return None
    return float(linha.iloc[0])


def _leitura_estado(taxas: pd.DataFrame) -> str:
    pares = (
        ("13", "13", "ficaram no 13"),
        ("13", "22", "foram para o 22"),
        ("22", "22", "ficaram no 22"),
        ("22", "13", "foram para o 13"),
    )
    frases = []
    for origem, destino, verbo in pares:
        bp = _taxa(taxas, "estado_soma", origem, destino, "brown_payne")
        lp = _taxa(taxas, "estado_soma", origem, destino, "lphom")
        if bp is None or lp is None:
            continue
        bp_txt = _pct_modelo(taxas, "estado_soma", origem, destino, "brown_payne")
        nivel_bp = "Brown e Payne, 95%" if "(" in bp_txt else "Brown e Payne"
        frases.append(f"dos votos do {origem}, {bp_txt} ({nivel_bp}) e {_pct(lp)} (lphom) {verbo}")
    if not frases:
        return "Sem a soma das cidades."
    return "Somando as cidades: " + "; ".join(frases) + "."


def _tabela_taxas(taxas: pd.DataFrame) -> str:
    if taxas.empty:
        return "Sem taxas."
    linhas = [
        "| Origem | Destino | Brown e Payne | lphom |",
        "|---|---|---:|---:|",
    ]
    bp = taxas.loc[taxas["modelo"] == "brown_payne"].set_index(["origem", "destino"])
    lp = taxas.loc[taxas["modelo"] == "lphom"].set_index(["origem", "destino"])
    for origem in ORIGENS:
        for destino in DESTINOS:
            a = bp.loc[(origem, destino)] if (origem, destino) in bp.index else None
            b = lp.loc[(origem, destino), "taxa"] if (origem, destino) in lp.index else None
            linhas.append(
                f"| {origem} | {destino} | {_pct_linha(a)} | {_pct(b)} |"
            )
    if "r2" not in taxas.columns:
        return "\n".join(linhas)
    r2 = taxas.groupby("modelo")["r2"].first()
    if r2.notna().any():
        partes = [
            f"{modelo} {float(valor):.3f}"
            for modelo, valor in r2.items()
            if pd.notna(valor)
        ]
        linhas += ["", "R² das contagens: " + "; ".join(partes) + "."]
    return "\n".join(linhas)


def _pct(valor) -> str:
    if valor is None or pd.isna(valor):
        return "—"
    return f"{100 * float(valor):.1f}%"


def _pct_linha(linha) -> str:
    if linha is None:
        return "—"
    taxa = linha["taxa"] if isinstance(linha, pd.Series) else linha
    lo = linha["taxa_lo"] if isinstance(linha, pd.Series) and "taxa_lo" in linha.index else None
    hi = linha["taxa_hi"] if isinstance(linha, pd.Series) and "taxa_hi" in linha.index else None
    return _pct_intervalo(taxa, lo, hi)


def _pct_intervalo(taxa, lo, hi) -> str:
    ponto = _pct(taxa)
    if lo is None or hi is None or pd.isna(lo) or pd.isna(hi):
        return ponto
    return f"{ponto} ({100 * float(lo):.1f}–{100 * float(hi):.1f})"


def _pct_modelo(taxas: pd.DataFrame, nivel: str, origem: str, destino: str, modelo: str) -> str:
    linha = taxas.loc[
        (taxas["nivel"] == nivel)
        & (taxas["origem"] == origem)
        & (taxas["destino"] == destino)
        & (taxas["modelo"] == modelo)
    ]
    if linha.empty:
        return "—"
    return _pct_linha(linha.iloc[0])


def _divergencias(taxas: pd.DataFrame) -> pd.DataFrame:
    mun = taxas.loc[
        (taxas["nivel"] == "municipio")
        & (taxas["origem"].isin(["13", "22"]))
        & (taxas["destino"].isin(["13", "22"]))
    ]
    if mun.empty:
        return mun
    larga = mun.pivot_table(
        index=["municipio", "origem", "destino"], columns="modelo", values="taxa"
    ).reset_index()
    if not {"brown_payne", "lphom"}.issubset(larga.columns):
        return larga.iloc[0:0]
    larga = larga.loc[(larga["brown_payne"] - larga["lphom"]).abs() > 0.05]
    return larga.sort_values(["municipio", "origem", "destino"])


def _prever_secao(margens: pd.DataFrame, taxas: pd.DataFrame, min_secoes: int) -> pd.DataFrame:
    n_mun = margens.groupby("municipio").size()
    fonte = fonte_por_municipio(n_mun, min_secoes)
    aplicadas = _taxas_aplicadas(taxas, fonte)
    base = margens[["join_key", "municipio", "zona", "secao"]].copy()
    base["fonte"] = base["municipio"].map(fonte)
    for modelo, sub in aplicadas.groupby("modelo"):
        larga = sub.pivot_table(
            index="municipio", columns=["origem", "destino"], values="taxa"
        )
        for destino in DESTINOS:
            pred = []
            for _, row in margens.iterrows():
                total = 0.0
                linha = larga.loc[int(row["municipio"])]
                for origem in ORIGENS:
                    total += float(row[f"o_{origem}"]) * float(linha[(origem, destino)])
                pred.append(total)
            base[f"pred_{modelo}_{destino}"] = pred
    for destino in DESTINOS:
        base[f"d_{destino}"] = margens[f"d_{destino}"].to_numpy()
    return base


def run_transferencia(
    ufs: list[str],
    *,
    min_secoes: int = MIN_SECOES,
) -> list[Path]:
    """Estima as matrizes e grava Parquet + Markdown."""
    ensure_dirs()
    saidas: list[Path] = []
    for uf in ufs:
        uf = uf.upper()
        path = REPORTS_DIR / f"comparar_turnos_{uf}_1t_2t.parquet"
        if not path.exists():
            console.print(f"[red]Falta {path.name}[/red]")
            continue
        console.print(f"[cyan]Transferência[/cyan] {uf} · mínimo {min_secoes} seções por cidade")
        margens = montar_margens(pd.read_parquet(path))
        taxas = _chamar_r(margens, min_secoes)
        taxas.insert(0, "uf", uf)
        soma = somar_fluxos(margens, taxas)
        soma.insert(0, "uf", uf)
        soma["min_secoes"] = min_secoes
        tudo = pd.concat([taxas, soma], ignore_index=True)
        pq = REPORTS_DIR / f"transferencia_{uf}.parquet"
        md = REPORTS_DIR / f"transferencia_{uf}.md"
        secao = REPORTS_DIR / f"transferencia_secao_{uf}.parquet"
        tudo.to_parquet(pq, index=False)
        md.write_text(_markdown(uf, margens, tudo, min_secoes), encoding="utf-8")
        _prever_secao(margens, taxas, min_secoes).to_parquet(secao, index=False)
        saidas.extend([pq, md, secao])
        _imprimir(uf, tudo)
        console.print(f"[green]Relatório:[/green] {md}")
    pais = consolidar_pais()
    if pais is not None:
        saidas.append(pais)
        console.print(f"[green]País:[/green] {pais}")
    return saidas


def taxas_pais(partes: list[pd.DataFrame]) -> pd.DataFrame:
    """Soma os votos transferidos dos estados. A taxa nacional é essa soma."""
    soma = pd.concat(
        [p.loc[p["nivel"] == "estado_soma"] for p in partes if not p.empty],
        ignore_index=True,
    )
    if soma.empty or "votos" not in soma.columns:
        return soma.iloc[0:0].copy()
    linhas = []
    for (modelo, origem, destino), g in soma.groupby(["modelo", "origem", "destino"]):
        votos = float(pd.to_numeric(g["votos"], errors="coerce").fillna(0).sum())
        se = pd.NA
        if "se" in g.columns and votos > 0 and g["se"].notna().all():
            var = float(((g["votos"].astype(float) ** 2) * (g["se"].astype(float) ** 2)).sum())
            se = var**0.5 / votos
        linhas.append(
            {
                "uf": "BR",
                "nivel": "pais",
                "modelo": modelo,
                "origem": origem,
                "destino": destino,
                "votos": votos,
                "se": se,
            }
        )
    pais = pd.DataFrame(linhas)
    totais = pais.groupby(["modelo", "origem"])["votos"].transform("sum")
    pais["taxa"] = pais["votos"] / totais.replace(0, pd.NA)
    limites = pais.apply(lambda r: _limites(r["taxa"], r["se"]), axis=1, result_type="expand")
    pais["taxa_lo"] = limites[0]
    pais["taxa_hi"] = limites[1]
    pais["confianca"] = pais["se"].map(lambda se: CONFIANCA if pd.notna(se) else pd.NA)
    return pais


def consolidar_pais() -> Path | None:
    """Lê os parquets já gravados e escreve o consolidado nacional."""
    presentes: list[str] = []
    partes: list[pd.DataFrame] = []
    for uf in UFS:
        path = REPORTS_DIR / f"transferencia_{uf}.parquet"
        if not path.exists():
            continue
        presentes.append(uf)
        partes.append(pd.read_parquet(path))
    if not presentes:
        return None
    faltam = [uf for uf in UFS if uf not in presentes]
    pais = taxas_pais(partes)
    estados = pd.concat(
        [p.loc[p["nivel"] == "estado_soma"] for p in partes],
        ignore_index=True,
    )
    tudo = pd.concat([estados, pais], ignore_index=True)
    pq = REPORTS_DIR / "transferencia_BRASIL.parquet"
    md = REPORTS_DIR / "transferencia_BRASIL.md"
    tudo.to_parquet(pq, index=False)
    md.write_text(_markdown_pais(pais, estados, presentes, faltam), encoding="utf-8")
    return md


def _markdown_pais(
    pais: pd.DataFrame,
    estados: pd.DataFrame,
    presentes: list[str],
    faltam: list[str],
) -> str:
    linhas = [
        "# Transferência 1º→2º — país",
        "",
        f"Estados neste consolidado: **{len(presentes)}** de {len(UFS)} "
        f"({', '.join(presentes)}).",
    ]
    if faltam:
        linhas.append(f"Ainda sem matriz: {', '.join(faltam)}.")
        linhas.append(
            "A taxa abaixo soma só os estados já estimados. Não é o total nacional enquanto a lista não fechar."
        )
    else:
        linhas.append("A taxa abaixo soma os votos transferidos de todos os estados.")
    linhas += [
        "",
        "Cada estado usa a soma das suas cidades. O país soma esses votos, não a média das taxas.",
        "",
        "## País",
        "",
        _tabela_taxas(pais),
        "",
        "## Estado a estado",
        "",
        _tabela_estados(estados),
        "",
        "Modelos: Brown e Payne (1986); lphom, cenário simultaneous.",
        "",
    ]
    return "\n".join(linhas)


def _tabela_estados(estados: pd.DataFrame) -> str:
    if estados.empty:
        return "Sem estados."
    celulas = (("13", "13"), ("13", "22"), ("22", "13"), ("22", "22"))
    cabeca = ["UF"]
    for origem, destino in celulas:
        cabeca.append(f"{origem}→{destino} BP")
        cabeca.append(f"{origem}→{destino} lphom")
    linhas = [
        "| " + " | ".join(cabeca) + " |",
        "|" + "|".join(["---"] + ["---:"] * (len(cabeca) - 1)) + "|",
    ]
    for uf in [u for u in UFS if u in set(estados["uf"].astype(str))]:
        bloco = estados.loc[estados["uf"].astype(str) == uf]
        cols = [uf]
        for origem, destino in celulas:
            cols.append(_pct(_taxa(bloco, "estado_soma", origem, destino, "brown_payne")))
            cols.append(_pct(_taxa(bloco, "estado_soma", origem, destino, "lphom")))
        linhas.append("| " + " | ".join(cols) + " |")
    return "\n".join(linhas)


def _imprimir(uf: str, taxas: pd.DataFrame) -> None:
    estado = taxas.loc[taxas["nivel"] == "estado"]
    table = Table(title=f"Transferência {uf} — taxa do estado")
    table.add_column("Célula")
    table.add_column("Brown e Payne", justify="right")
    table.add_column("lphom", justify="right")
    for origem in ORIGENS:
        for destino in DESTINOS:
            linha = estado.loc[
                (estado["origem"] == origem) & (estado["destino"] == destino)
            ]
            vals = {r["modelo"]: r for _, r in linha.iterrows()}
            table.add_row(
                f"{origem}→{destino}",
                _pct_linha(vals.get("brown_payne")),
                _pct(None if "lphom" not in vals else vals["lphom"]["taxa"]),
            )
    console.print(table)
