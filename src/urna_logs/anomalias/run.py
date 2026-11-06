"""Orquestra o piloto: baixa o que falta, varre e grava CSV e o resumo numérico."""

from __future__ import annotations

import pandas as pd
from rich.console import Console

from urna_logs.anomalias.estatistica import (
    alertas_digitos,
    alertas_regressao,
    alertas_z,
    fingerprint,
    preparar,
)
from urna_logs.anomalias.integridade import (
    alertas_integridade,
    cache_ano,
    garantir_secao,
    sondar_zip,
)
from urna_logs.anomalias.logs import parse_data_hora_je, varrer_logs
from urna_logs.anomalias.textos import COMO, MODULO, SEVERIDADE
from urna_logs.config import ANOMALIAS_DIR, REPORTS_DIR, zip_path, zip_url
from urna_logs.download import download_zip
from urna_logs.municipios import ensure_perfil
from urna_logs.oficial import ensure_votacao_presidente_zip
from urna_logs.thresholds import (
    ANOMALIAS_VERSAO,
    RUIDO_RAZAO_HI,
    RUIDO_RAZAO_LO,
    FDR_Q,
    SEQ_INTERVALO_MIN,
)

console = Console()

_COLUNAS = [
    "uf", "ano", "turno", "municipio", "nome_municipio", "zona", "secao",
    "local", "nome_local", "join_key", "modulo", "teste", "candidato",
    "observado", "referencia", "esperados", "q", "severidade",
    "como_verificar", "membro", "url_zip",
]


def _ids(join_key: str) -> tuple[int, int, int]:
    partes = str(join_key or "").split(":")
    if len(partes) != 4:
        return 0, 0, 0
    try:
        return int(partes[1]), int(partes[2]), int(partes[3])
    except ValueError:
        return 0, 0, 0


def _completar(linha: dict, uf: str, ano: int, turno: int) -> dict:
    jk = linha.get("join_key") or ""
    mun, zona, secao = _ids(jk)
    if not linha.get("municipio"):
        linha["municipio"] = mun
    if not linha.get("zona"):
        linha["zona"] = zona
    if not linha.get("secao"):
        linha["secao"] = secao
    teste = linha["teste"]
    linha.update(
        {
            "uf": uf,
            "ano": int(ano),
            "turno": int(turno),
            "join_key": jk,
            "nome_municipio": linha.get("nome_municipio") or "",
            "nome_local": linha.get("nome_local") or "",
            "local": linha.get("local") or 0,
            "candidato": linha.get("candidato") or "",
            "modulo": MODULO.get(teste, ""),
            "esperados": linha.get("esperados", ""),
            "q": linha.get("q", ""),
            "severidade": SEVERIDADE.get(teste, "estatistico"),
            "como_verificar": COMO.get(teste, ""),
            "membro": linha.get("membro") or "",
            "url_zip": zip_url(uf, turno, ano),
        }
    )
    return linha


def alertas_de_log(logs: pd.DataFrame, base: pd.DataFrame) -> list[dict]:
    if logs.empty:
        return []
    cols = ["join_key", "bu_comparecimento", "municipio", "zona", "secao", "local"]
    presentes = [c for c in cols if c in base.columns]
    quadro = logs.merge(base[presentes], on="join_key", how="left", suffixes=("", "_secao"))
    linhas = []
    for rec in quadro.to_dict(orient="records"):
        comum = {
            "join_key": rec.get("join_key") or "",
            "municipio": rec.get("municipio") or 0,
            "zona": rec.get("zona") or 0,
            "secao": rec.get("secao") or 0,
            "local": rec.get("local") or 0,
            "membro": f"{rec.get('stem') or ''}-log.jez",
        }
        if int(rec.get("n_fora_janela") or 0) > 0:
            linhas.append({**comum, "teste": "voto_fora_janela", "observado": rec["n_fora_janela"], "referencia": "janela 8h–17h"})
        if int(rec.get("seq_curta") or 0) >= SEQ_INTERVALO_MIN:
            linhas.append({**comum, "teste": "intervalo_curto", "observado": rec["seq_curta"], "referencia": SEQ_INTERVALO_MIN})
        if int(rec.get("n_ajuste_hora") or 0) > 0:
            linhas.append({**comum, "teste": "ajuste_hora", "observado": rec["n_ajuste_hora"], "referencia": "dia do turno"})
        if int(rec.get("n_reinicio") or 0) > 0:
            linhas.append({**comum, "teste": "reinicio", "observado": rec["n_reinicio"], "referencia": "dia do turno"})
        if int(rec.get("n_contingencia") or 0) > 0:
            linhas.append({**comum, "teste": "contingencia", "observado": rec["n_contingencia"], "referencia": "dia do turno"})
        comp = rec.get("bu_comparecimento")
        if comp is not None and pd.notna(comp) and int(rec.get("n_votos_log") or 0) != int(comp):
            linhas.append(
                {
                    **comum,
                    "teste": "log_diferente_bu",
                    "observado": rec.get("n_votos_log"),
                    "referencia": int(comp),
                }
            )
    return linhas


def _ruido(n_2026: int, n_2022: float | None) -> str:
    if n_2022 is None or n_2022 == 0:
        return ""
    razao = n_2026 / n_2022
    if RUIDO_RAZAO_LO <= razao <= RUIDO_RAZAO_HI:
        return (
            "A contagem de 2026 no 2º turno fica entre 0,5 e 2 vezes a de 2022. "
            "O teste mede um padrão que já aparecia na linha de base."
        )
    return ""


_TESTES_RESUMO = (
    ("formato_nao_decodificado", "", "integridade"),
    ("arquivo_ausente", "", "integridade"),
    ("arquivo_corrompido", "", "integridade"),
    ("hash_divergente", "", "integridade"),
    ("assinatura_invalida", "", "integridade"),
    ("bu_rdv", "", "integridade"),
    ("bu_csv", "", "integridade"),
    ("voto_fora_janela", "", "logs"),
    ("intervalo_curto", "", "logs"),
    ("ajuste_hora", "", "logs"),
    ("reinicio", "", "logs"),
    ("contingencia", "", "logs"),
    ("log_diferente_bu", "", "logs"),
    ("sem_digital", "", "logs"),
    ("z_comparecimento", "", "estatistica"),
    ("z_candidato", "13", "estatistica"),
    ("z_candidato", "22", "estatistica"),
    ("fingerprint", "13", "estatistica"),
    ("fingerprint", "22", "estatistica"),
    ("ultimo_digito", "", "estatistica"),
    ("ultimo_digito", "13", "estatistica"),
    ("ultimo_digito", "22", "estatistica"),
    ("numero_redondo", "", "estatistica"),
    ("numero_redondo", "13", "estatistica"),
    ("numero_redondo", "22", "estatistica"),
    ("mebane", "", "estatistica"),
    ("mebane", "13", "estatistica"),
    ("mebane", "22", "estatistica"),
    ("residuo_2t", "13", "estatistica"),
    ("residuo_2t", "22", "estatistica"),
)


def _esperados(quadro: pd.DataFrame, grupo: pd.DataFrame, teste: str) -> float | None:
    """Soma o nulo de cada UF. Mebane é um teste por UF, com probabilidade FDR_Q."""
    if teste == "mebane":
        if quadro is None or quadro.empty or "uf" not in quadro.columns:
            return FDR_Q
        n_ufs = int(quadro["uf"].replace("", pd.NA).dropna().nunique())
        return FDR_Q * max(n_ufs, 1)
    if grupo is None or grupo.empty or "esperados" not in grupo.columns:
        return None
    parte = grupo[(grupo["ano"] == 2026) & (grupo["turno"] == 2)]
    if parte.empty:
        parte = grupo
    esp = pd.to_numeric(parte["esperados"], errors="coerce")
    tmp = parte.assign(_esp=esp).dropna(subset=["_esp"])
    if tmp.empty:
        return None
    if "uf" not in tmp.columns:
        return float(tmp["_esp"].iloc[0])
    return float(tmp.groupby("uf")["_esp"].first().sum())


def _resumo(alertas: pd.DataFrame) -> pd.DataFrame:
    quadro = alertas if alertas is not None else pd.DataFrame()
    linhas = []
    for teste, cand, modulo in _TESTES_RESUMO:
        if quadro.empty:
            grupo = quadro
        else:
            cand_s = quadro["candidato"].fillna("").astype(str).replace({"13.0": "13", "22.0": "22"})
            grupo = quadro[(quadro["teste"] == teste) & (cand_s == cand)]

        def _n(ano, turno, parte=grupo):
            if parte is None or parte.empty:
                return 0
            return int(((parte["ano"] == ano) & (parte["turno"] == turno)).sum())

        n26_2 = _n(2026, 2)
        n22_2 = _n(2022, 2)
        if teste == "fingerprint" and n26_2 == 0 and n22_2 == 0:
            nota = "Sem base de 2022 decodificada; o histograma não foi comparado."
        else:
            nota = _ruido(n26_2, n22_2)
        linhas.append(
            {
                "teste": teste,
                "candidato": cand,
                "modulo": modulo,
                "n_2026_1": _n(2026, 1),
                "n_2026_2": n26_2,
                "n_2022_1": _n(2022, 1),
                "n_2022_2": n22_2,
                "esperados_nulo": _esperados(quadro, grupo, teste),
                "ruido": nota,
                "exploratorio": teste == "mebane",
            }
        )
    return pd.DataFrame(linhas)


def _markdown(uf: str, resumo: pd.DataFrame, sonda: dict) -> str:
    linhas = [
        f"# Anomalias — {uf}",
        "",
        f"Versão dos limiares: {ANOMALIAS_VERSAO}.",
        "O código 22 de 2022 não é o mesmo candidato do código 22 de 2026. A comparação é a contagem de alertas do mesmo procedimento.",
        "",
        "## Sonda de formato",
        "",
    ]
    for chave, estado in sorted(sonda.items()):
        linhas.append(f"- {chave}: {estado}")
    linhas += ["", "## Falha verificável", ""]
    ver = resumo[resumo["modulo"] == "integridade"] if not resumo.empty else resumo
    linhas.append(_tabela(ver))
    linhas += ["", "## Padrão estatístico", ""]
    est = resumo[resumo["modulo"] != "integridade"] if not resumo.empty else resumo
    linhas.append(_tabela(est))
    linhas.append("")
    return "\n".join(linhas)


def _tabela(df: pd.DataFrame) -> str:
    if df is None or df.empty:
        return "0"
    cab = "| teste | candidato | 2026 1º | 2026 2º | 2022 1º | 2022 2º | esperados | linha de base |"
    sep = "|---|---|---:|---:|---:|---:|---:|---|"
    linhas = [cab, sep]
    for _, row in df.sort_values(["teste", "candidato"]).iterrows():
        esp = row["esperados_nulo"]
        esp_txt = "—" if pd.isna(esp) else f"{esp:.2f}"
        linhas.append(
            f"| {row['teste']} | {row['candidato'] or '—'} | {int(row['n_2026_1'])} | "
            f"{int(row['n_2026_2'])} | {int(row['n_2022_1'])} | {int(row['n_2022_2'])} | "
            f"{esp_txt} | {row['ruido']} |"
        )
    return "\n".join(linhas)


def _nomes(alertas: pd.DataFrame, perfil: pd.DataFrame) -> pd.DataFrame:
    if alertas.empty or perfil.empty:
        return alertas
    nomes = perfil.rename(columns={"nome_municipio": "nome_municipio_p", "nome_local": "nome_local_p"})
    chave = ["municipio", "zona", "secao"]
    out = alertas.merge(
        nomes[chave + ["nome_municipio_p", "nome_local_p", "local"]].drop_duplicates(chave),
        on=chave,
        how="left",
        suffixes=("", "_p"),
    )
    if "local_p" in out.columns:
        vazio = out["local"].fillna(0).astype(int) == 0
        out.loc[vazio, "local"] = out.loc[vazio, "local_p"]
        out = out.drop(columns=["local_p"])
    out["nome_municipio"] = out["nome_municipio_p"].fillna("")
    out["nome_local"] = out["nome_local_p"].fillna("")
    return out.drop(columns=["nome_municipio_p", "nome_local_p"], errors="ignore")


def _escrever_linhas(ufs: list[str], anos: list[int], quadro: pd.DataFrame) -> None:
    """Uma UF por vez, a partir do parquet de tempos. Só seções que entraram no alerta."""
    colunas = ["join_key", "ano", "turno", "t", "delta_s", "uf"]
    chaves: set[str] = set()
    if quadro is not None and not quadro.empty and "join_key" in quadro.columns:
        marca = quadro["join_key"].fillna("").astype(str)
        chaves = set(marca[marca.str.contains(":")])
    for uf in ufs:
        uf = uf.upper()
        partes = []
        for ano in anos:
            for turno in (1, 2):
                path = cache_ano(ano) / f"tempos_{uf}_{turno}t.parquet"
                if not path.exists():
                    continue
                tempo = pd.read_parquet(path)
                if "uf" not in tempo.columns:
                    tempo["uf"] = uf
                tempo = tempo[tempo["join_key"].isin(chaves)] if chaves else tempo.head(0)
                if not tempo.empty:
                    partes.append(tempo)
        destino = ANOMALIAS_DIR / f"linha_{uf}.csv"
        if partes:
            pd.concat(partes, ignore_index=True).to_csv(destino, index=False)
        else:
            pd.DataFrame(columns=colunas).to_csv(destino, index=False)


def run_anomalias(ufs: list[str], anos: list[int], *, force: bool = False) -> None:
    ANOMALIAS_DIR.mkdir(parents=True, exist_ok=True)
    alertas: list[dict] = []
    grades: list[pd.DataFrame] = []
    bases: dict[tuple[int, str, int], pd.DataFrame] = {}
    sonda_txt: dict[str, str] = {}
    notas: list[str] = []

    for ano in anos:
        ensure_votacao_presidente_zip(ano=ano)
        for uf in ufs:
            uf = uf.upper()
            perfil = ensure_perfil(ano, uf)
            for turno in (1, 2):
                download_zip(uf, turno, ano=ano)
                zpath = zip_path(uf, turno, ano)
                sonda = sondar_zip(zpath)
                for tipo, estado in sonda.items():
                    sonda_txt[f"{ano} {uf} {turno}º {tipo}"] = estado
                if sonda.get("bu") != "ok":
                    for tipo, estado in sonda.items():
                        if estado == "ok":
                            continue
                        alertas.append(
                            _completar(
                                {
                                    "teste": "formato_nao_decodificado",
                                    "observado": tipo,
                                    "referencia": estado,
                                    "join_key": "",
                                },
                                uf, ano, turno,
                            )
                        )
                    continue
                secoes, votos = garantir_secao(uf, turno, ano, force=force)
                base = preparar(secoes, votos)
                if not perfil.empty:
                    base = base.merge(
                        perfil[["municipio", "zona", "secao", "nome_municipio", "nome_local"]],
                        on=["municipio", "zona", "secao"],
                        how="left",
                    )
                bases[(ano, uf, turno)] = base
                for linha in alertas_integridade(
                    uf, turno, ano, secoes, votos, sonda=sonda, force=force
                ).to_dict(orient="records"):
                    alertas.append(_completar(linha, uf, ano, turno))
                for linha in alertas_z(base):
                    alertas.append(_completar(linha, uf, ano, turno))
                for linha in alertas_digitos(base, uf):
                    alertas.append(_completar(linha, uf, ano, turno))
                if sonda.get("log") == "ok":
                    fim = {
                        jk: parse_data_hora_je(valor)
                        for jk, valor in zip(base["join_key"], base.get("encerramento", []), strict=False)
                    }
                    logs, tempo = varrer_logs(uf, turno, ano, fim, force=force)
                    del tempo
                    for linha in alertas_de_log(logs, base):
                        alertas.append(_completar(linha, uf, ano, turno))
            if (ano, uf, 1) in bases and (ano, uf, 2) in bases:
                linhas, nota = alertas_regressao(bases[(ano, uf, 1)], bases[(ano, uf, 2)])
                notas.append(f"{ano} {uf}: {nota}")
                for linha in linhas:
                    alertas.append(_completar(linha, uf, ano, 2))

    for uf in ufs:
        uf = uf.upper()
        for turno in (1, 2):
            if (2026, uf, turno) not in bases or (2022, uf, turno) not in bases:
                continue
            for cod in ("13", "22"):
                grade, linhas = fingerprint(bases[(2026, uf, turno)], bases[(2022, uf, turno)], cod)
                if not grade.empty:
                    grade["ano"] = 2026
                    grade["turno"] = turno
                    grade["uf"] = uf
                    grades.append(grade)
                for linha in linhas:
                    alertas.append(_completar(linha, uf, 2026, turno))
                grade_r, linhas_r = fingerprint(bases[(2022, uf, turno)], bases[(2026, uf, turno)], cod)
                if not grade_r.empty:
                    grade_r["ano"] = 2022
                    grade_r["turno"] = turno
                    grade_r["uf"] = uf
                    grades.append(grade_r)
                for linha in linhas_r:
                    alertas.append(_completar(linha, uf, 2022, turno))

    quadro = pd.DataFrame(alertas)
    if not quadro.empty:
        for col in _COLUNAS:
            if col not in quadro.columns:
                quadro[col] = ""
        perfil_nomes = []
        for ano in anos:
            for uf in ufs:
                perfil_nomes.append(ensure_perfil(ano, uf))
        quadro = _nomes(quadro, pd.concat(perfil_nomes, ignore_index=True) if perfil_nomes else pd.DataFrame())
        quadro = quadro[_COLUNAS]
    resumo = _resumo(quadro)
    ANOMALIAS_DIR.mkdir(parents=True, exist_ok=True)
    quadro.to_csv(ANOMALIAS_DIR / "alertas.csv", index=False)
    resumo.to_csv(ANOMALIAS_DIR / "resumo.csv", index=False)
    if grades:
        pd.concat(grades, ignore_index=True).to_csv(ANOMALIAS_DIR / "fingerprint.csv", index=False)
    else:
        pd.DataFrame(columns=["bin_comp", "bin_share", "n_atual", "n_ref", "candidato", "ano", "turno", "uf"]).to_csv(
            ANOMALIAS_DIR / "fingerprint.csv", index=False
        )
    _escrever_linhas(ufs, anos, quadro)
    texto = _markdown("Brasil" if len(ufs) > 1 else ufs[0].upper(), resumo, sonda_txt)
    if notas:
        texto += "\n## Efeito fixo de local\n\n" + "\n".join(f"- {n}" for n in notas) + "\n"
    if len(ufs) > 1:
        destino = REPORTS_DIR / "anomalias_Brasil.md"
        destino.write_text(texto, encoding="utf-8")
        console.print(f"[green]Resumo:[/green] {destino}")
    for uf in ufs:
        uf = uf.upper()
        parte = quadro[quadro["uf"] == uf] if not quadro.empty and "uf" in quadro.columns else quadro
        sonda_uf = {k: v for k, v in sonda_txt.items() if f" {uf} " in k}
        notas_uf = [n for n in notas if f" {uf}:" in n]
        texto_uf = _markdown(uf, _resumo(parte), sonda_uf)
        if notas_uf:
            texto_uf += "\n## Efeito fixo de local\n\n" + "\n".join(f"- {n}" for n in notas_uf) + "\n"
        destino = REPORTS_DIR / f"anomalias_{uf}.md"
        destino.write_text(texto_uf, encoding="utf-8")
        console.print(f"[green]Resumo:[/green] {destino}")
