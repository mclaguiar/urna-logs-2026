"""Falhas de arquivo, hash, assinatura, BU×RDV e BU×CSV.

2026 lê os relatórios já gravados. 2022 grava só em data/anomalias.
"""

from __future__ import annotations

import zipfile
from pathlib import Path

import pandas as pd
from rich.console import Console

from urna_logs.audit import audit_zip, results_to_frame, results_to_votos_frame
from urna_logs.bu_rdv import parse_bu_bytes, parse_rdv_bytes
from urna_logs.config import ANO, ANOMALIAS_DIR, REPORTS_DIR, zip_path
from urna_logs.oficial import load_oficial_votos
from urna_logs.parse_log import _events_from_jez_bytes
from urna_logs.verificar_vsc import _decode_vsc, _index_zip, verificar_stem
from urna_logs.zip_logs import read_member_from_open_zip

console = Console()

_ALERTAS_VAZIO = [
    "uf", "ano", "turno", "join_key", "municipio", "zona", "secao", "local",
    "teste", "observado", "referencia", "membro",
]


def cache_ano(ano: int) -> Path:
    dest = ANOMALIAS_DIR / str(int(ano))
    dest.mkdir(parents=True, exist_ok=True)
    return dest


def _secao_path(ano: int, uf: str, turno: int) -> Path:
    return cache_ano(ano) / f"secao_{uf.upper()}_{turno}t.parquet"


def _votos_path(ano: int, uf: str, turno: int) -> Path:
    return cache_ano(ano) / f"votos_{uf.upper()}_{turno}t.parquet"


def _vsc_path(ano: int, uf: str, turno: int) -> Path:
    return cache_ano(ano) / f"vsc_{uf.upper()}_{turno}t.parquet"


def escolher_amostra(nomes: list[str]) -> dict[str, str | None]:
    """Um membro de cada tipo. 2026 usa -bu.dat; 2022 usa .bu / .vscmr / .logjez."""

    def base(nome: str) -> str:
        return nome.replace("\\", "/").rsplit("/", 1)[-1].lower()

    def um(*sufixos: str, excluir: tuple[str, ...] = ()) -> str | None:
        for nome in nomes:
            atual = base(nome)
            if any(atual.endswith(item) for item in excluir):
                continue
            if any(atual.endswith(item) for item in sufixos):
                return nome
        return None

    return {
        "bu": um(".bu", "-bu.dat", excluir=(".imgbu", "-imgbu.dat", "-imgbusa.dat")),
        "rdv": um(".rdv", "-rdv.dat"),
        "vsc": um(".vscmr", "-vota.vsc"),
        "log": um(".logjez", "-log.jez"),
    }


def sondar_zip(zpath: Path) -> dict[str, str]:
    """Abre um arquivo de cada tipo. 'ok' ou o erro. Não varre a UF."""
    saida = {"bu": "ausente", "rdv": "ausente", "vsc": "ausente", "log": "ausente"}
    if not zpath.exists():
        return {k: "zip ausente" for k in saida}
    with zipfile.ZipFile(zpath) as zf:
        nomes = zf.namelist()
        amostra = escolher_amostra(nomes)
        bu, rdv, vsc, log = amostra["bu"], amostra["rdv"], amostra["vsc"], amostra["log"]
        if bu:
            try:
                tot = parse_bu_bytes(zf.read(bu), source=bu)
                saida["bu"] = "ok" if tot is not None else "sem presidente"
            except Exception as exc:  # noqa: BLE001
                saida["bu"] = f"{type(exc).__name__}: {exc}"[:240]
        if rdv:
            try:
                tot = parse_rdv_bytes(zf.read(rdv), source=rdv)
                saida["rdv"] = "ok" if tot is not None else "sem presidente"
            except Exception as exc:  # noqa: BLE001
                saida["rdv"] = f"{type(exc).__name__}: {exc}"[:240]
        if vsc:
            try:
                _decode_vsc(zf.read(vsc))
                saida["vsc"] = "ok"
            except Exception as exc:  # noqa: BLE001
                saida["vsc"] = f"{type(exc).__name__}: {exc}"[:240]
        if log:
            try:
                raw = read_member_from_open_zip(zf, log)
                if raw[:2] == b"7z":
                    saida["log"] = "7z; o leitor atual abre o logjez que é zip"
                else:
                    evento = next(_events_from_jez_bytes(raw, log), None)
                    saida["log"] = "ok" if evento is not None else "nenhuma linha no formato conhecido"
            except Exception as exc:  # noqa: BLE001
                saida["log"] = f"{type(exc).__name__}: {exc}"[:240]
    return saida


def tipos_vsc(row: dict) -> list[str]:
    if not row.get("tem_vsc") or not row.get("parse_ok"):
        erro = str(row.get("erro") or "").lower()
        if any(m in erro for m in ("parse", "badzip", "asn1", "decode")):
            return ["arquivo_corrompido"]
        return ["arquivo_ausente"]
    tipos: list[str] = []
    det = str(row.get("criticos_detalhe") or "")
    n_fail = row.get("n_hash_fail")
    try:
        n_fail = 0 if n_fail is None or pd.isna(n_fail) else int(n_fail)
    except (TypeError, ValueError):
        n_fail = 0
    if n_fail > 0 or "hash_fail" in det:
        tipos.append("hash_divergente")
    if "ausente_lista" in det or any(
        trecho in det for trecho in ("bu.dat=ausente", "rdv.dat=ausente", "log.jez=ausente")
    ):
        tipos.append("arquivo_ausente")
    cadeia = str(row.get("hw_cadeia") or "")
    if cadeia == "pendente":
        return tipos
    if cadeia == "falha" or row.get("hw_sig_ok") == False:
        tipos.append("assinatura_invalida")
    return tipos


def tipos_audit(row: dict) -> list[str]:
    erro = str(row.get("error") or "")
    if erro:
        if "ausente" in erro.lower():
            return ["arquivo_ausente"]
        return ["arquivo_corrompido"]
    if not row.get("ok"):
        return ["bu_rdv"]
    return []


def _codigo(n) -> str:
    if n is None or (isinstance(n, float) and pd.isna(n)) or n == "":
        return ""
    try:
        return str(int(float(n)))
    except (TypeError, ValueError):
        return str(n)


def _pivot(votos: pd.DataFrame) -> pd.DataFrame:
    if votos.empty:
        return pd.DataFrame(columns=["join_key", "votos_13", "votos_22", "branco", "nulo", "outros"])
    frame = votos.copy()
    frame["numero"] = frame["numero"].map(_codigo)
    def _rotulo(row: pd.Series) -> str:
        if row["tipo"] == "branco":
            return "branco"
        if row["tipo"] == "nulo":
            return "nulo"
        if row["tipo"] == "nominal" and row["numero"] in {"13", "22"}:
            return f"votos_{row['numero']}"
        return "outros"

    frame["coluna"] = frame.apply(_rotulo, axis=1)
    amplo = (
        frame.pivot_table(index="join_key", columns="coluna", values="votos_bu", aggfunc="sum", fill_value=0)
        .reset_index()
    )
    for col in ("votos_13", "votos_22", "branco", "nulo", "outros"):
        if col not in amplo.columns:
            amplo[col] = 0
    return amplo


def garantir_secao(uf: str, turno: int, ano: int, *, force: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    uf = uf.upper()
    destino = _secao_path(ano, uf, turno)
    votos_dest = _votos_path(ano, uf, turno)
    if destino.exists() and votos_dest.exists() and not force:
        return pd.read_parquet(destino), pd.read_parquet(votos_dest)
    zpath = zip_path(uf, turno, ano)
    resultados = audit_zip(zpath)
    secoes = results_to_frame(resultados, uf, turno)
    votos = results_to_votos_frame(resultados, uf, turno)
    secoes.to_parquet(destino, index=False)
    votos.to_parquet(votos_dest, index=False)
    console.print(f"[green]Seções:[/green] {destino.name} ({len(secoes):,})")
    return secoes, votos


def _vsc_2026(uf: str, turno: int) -> pd.DataFrame | None:
    path = REPORTS_DIR / f"verificar_vsc_{uf}_{turno}t.parquet"
    if path.exists():
        return pd.read_parquet(path)
    return None


def varrer_vsc(uf: str, turno: int, ano: int, *, force: bool = False) -> pd.DataFrame:
    uf = uf.upper()
    destino = _vsc_path(ano, uf, turno)
    if destino.exists() and not force:
        return pd.read_parquet(destino)
    if ano == ANO:
        pronto = _vsc_2026(uf, turno)
        if pronto is not None and not force:
            return pronto
    zpath = zip_path(uf, turno, ano)
    linhas = []
    with zipfile.ZipFile(zpath) as zf:
        por_stem = _index_zip(zf)
        for stem in sorted(por_stem):
            item = verificar_stem(zf, stem, por_stem[stem])
            linhas.append(
                {
                    "join_key": item.join_key or "",
                    "stem": item.stem,
                    "tem_vsc": item.tem_vsc,
                    "parse_ok": item.parse_ok,
                    "n_hash_fail": item.n_hash_fail,
                    "criticos_detalhe": item.criticos_detalhe,
                    "hw_sig_ok": item.hw_sig_ok,
                    "hw_cadeia": item.hw_cadeia,
                    "erro": item.erro,
                }
            )
    frame = pd.DataFrame(linhas)
    frame.to_parquet(destino, index=False)
    return frame


def _cruzar_2026(uf: str, turno: int) -> pd.DataFrame | None:
    path = REPORTS_DIR / f"cruzar_oficial_{uf}_{turno}t.parquet"
    if path.exists():
        return pd.read_parquet(path)
    return None


def secoes_bu_csv(uf: str, turno: int, ano: int, votos: pd.DataFrame) -> pd.DataFrame:
    """join_key das seções em que BU e CSV oficial não fecham."""
    if ano == ANO:
        pronto = _cruzar_2026(uf, turno)
        if pronto is not None and "ok" in pronto.columns:
            ruim = pronto.groupby("join_key")["ok"].all()
            return pd.DataFrame({"join_key": ruim.index[~ruim.to_numpy()]})
    oficial = load_oficial_votos(uf, turno, ano=ano)
    if votos.empty or oficial.empty:
        return pd.DataFrame(columns=["join_key"])
    base = votos.copy()
    base["votavel"] = [
        "95" if t == "branco" else "96" if t == "nulo" else _codigo(n)
        for t, n in zip(base["tipo"], base["numero"], strict=False)
    ]
    base = base[base["votavel"] != ""]
    somado = base.groupby(["join_key", "votavel"], as_index=False)["votos_bu"].sum()
    oficial = oficial.groupby(["join_key", "votavel"], as_index=False)["votos_oficial"].sum()
    merged = somado.merge(oficial, on=["join_key", "votavel"], how="outer")
    merged["votos_bu"] = merged["votos_bu"].fillna(0)
    merged["votos_oficial"] = merged["votos_oficial"].fillna(0)
    merged["ok"] = merged["votos_bu"] == merged["votos_oficial"]
    ruim = merged.groupby("join_key")["ok"].all()
    return pd.DataFrame({"join_key": ruim.index[~ruim.to_numpy()]})


def alertas_integridade(
    uf: str,
    turno: int,
    ano: int,
    secoes: pd.DataFrame,
    votos: pd.DataFrame,
    *,
    sonda: dict[str, str] | None = None,
    force: bool = False,
) -> pd.DataFrame:
    uf = uf.upper()
    linhas: list[dict] = []
    if sonda:
        for tipo, estado in sonda.items():
            if estado != "ok":
                linhas.append(
                    {
                        "uf": uf,
                        "ano": ano,
                        "turno": turno,
                        "join_key": "",
                        "municipio": 0,
                        "zona": 0,
                        "secao": 0,
                        "local": 0,
                        "teste": "formato_nao_decodificado",
                        "observado": tipo,
                        "referencia": estado,
                        "membro": "",
                    }
                )
    if sonda and sonda.get("vsc") not in (None, "ok"):
        vsc = pd.DataFrame()
    else:
        vsc = varrer_vsc(uf, turno, ano, force=force)
    if not vsc.empty:
        for rec in vsc.to_dict(orient="records"):
            for teste in tipos_vsc(rec):
                linhas.append(_linha_secao(uf, ano, turno, rec, teste, rec.get("erro") or rec.get("criticos_detalhe") or "", rec.get("hw_cadeia") or ""))
    if sonda and sonda.get("bu") not in (None, "ok"):
        pass
    elif not secoes.empty:
        for rec in secoes.to_dict(orient="records"):
            for teste in tipos_audit(rec):
                linhas.append(
                    _linha_secao(
                        uf, ano, turno, rec, teste,
                        rec.get("mismatches") or rec.get("error") or "",
                        rec.get("bu_total"),
                    )
                )
    if not (sonda and sonda.get("bu") not in (None, "ok")):
        diverg = secoes_bu_csv(uf, turno, ano, votos)
        conhecidas = (
            secoes.drop_duplicates("join_key").set_index("join_key")
            if not secoes.empty
            else pd.DataFrame()
        )
        for jk in diverg["join_key"]:
            if jk in conhecidas.index:
                rec = conhecidas.loc[jk].to_dict()
            else:
                rec = {"join_key": jk}
            linhas.append(_linha_secao(uf, ano, turno, rec, "bu_csv", "BU ≠ CSV", ""))
    if not linhas:
        return pd.DataFrame(columns=_ALERTAS_VAZIO)
    return pd.DataFrame(linhas)


def _linha_secao(uf, ano, turno, rec, teste, observado, referencia) -> dict:
    return {
        "uf": uf,
        "ano": int(ano),
        "turno": int(turno),
        "join_key": rec.get("join_key") or "",
        "municipio": int(rec.get("municipio") or 0),
        "zona": int(rec.get("zona") or 0),
        "secao": int(rec.get("secao") or 0),
        "local": int(rec.get("local") or 0),
        "teste": teste,
        "observado": observado,
        "referencia": referencia,
        "membro": f"{rec.get('stem') or ''}-bu.dat" if rec.get("stem") else "",
    }
