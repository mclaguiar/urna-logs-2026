"""Tabela código TSE → nome do município (perfil eleitorado por seção)."""

from __future__ import annotations

import zipfile
from io import BytesIO
from pathlib import Path

import httpx
import pandas as pd
from rich.console import Console

from urna_logs.config import ANOMALIAS_REF_DIR, DATA_DIR, ensure_dirs

console = Console()

REF_DIR = DATA_DIR / "ref"
MUN_CACHE = REF_DIR / "municipios_tse.csv"

_URL = (
    "https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_eleitor_secao/"
    "perfil_eleitor_secao_2026_{uf}.zip"
)


def _ensure_ref() -> None:
    ensure_dirs()
    REF_DIR.mkdir(parents=True, exist_ok=True)


def _load_cache() -> pd.DataFrame:
    if not MUN_CACHE.exists():
        return pd.DataFrame(columns=["uf", "municipio", "nome"])
    return pd.read_csv(MUN_CACHE, dtype={"uf": str, "municipio": int, "nome": str})


def _save_cache(df: pd.DataFrame) -> None:
    _ensure_ref()
    out = df.drop_duplicates(["uf", "municipio"]).sort_values(["uf", "municipio"])
    out.to_csv(MUN_CACHE, index=False)


def _fetch_uf(uf: str) -> pd.DataFrame:
    uf = uf.upper()
    url = _URL.format(uf=uf)
    console.print(f"[cyan]Baixando nomes de municípios[/cyan] {uf}…")
    with httpx.Client(timeout=120.0, follow_redirects=True) as client:
        resp = client.get(url)
        resp.raise_for_status()
    with zipfile.ZipFile(BytesIO(resp.content)) as zf:
        csv_name = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
        with zf.open(csv_name) as fh:
            raw = pd.read_csv(
                fh,
                sep=";",
                encoding="latin-1",
                dtype=str,
                usecols=["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"],
            )
    raw["municipio"] = raw["CD_MUNICIPIO"].str.lstrip("0").replace("", "0").astype(int)
    out = (
        raw.rename(columns={"SG_UF": "uf", "NM_MUNICIPIO": "nome"})[["uf", "municipio", "nome"]]
        .drop_duplicates(["uf", "municipio"])
    )
    out["uf"] = out["uf"].str.upper()
    return out


_PERFIL_URL = (
    "https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_eleitor_secao/"
    "perfil_eleitor_secao_{ano}_{uf}.zip"
)


def perfil_zip_path(ano: int, uf: str) -> Path:
    return ANOMALIAS_REF_DIR / f"perfil_eleitor_secao_{int(ano)}_{uf.upper()}.zip"


def perfil_cache_path(ano: int, uf: str) -> Path:
    return ANOMALIAS_REF_DIR / f"perfil_{int(ano)}_{uf.upper()}.parquet"


def ensure_perfil(ano: int, uf: str, *, force: bool = False) -> pd.DataFrame:
    """Aptos e local de votação por seção. Não reescreve municipios_tse.csv."""
    uf = uf.upper()
    ANOMALIAS_REF_DIR.mkdir(parents=True, exist_ok=True)
    cache = perfil_cache_path(ano, uf)
    if cache.exists() and not force:
        return pd.read_parquet(cache)

    zpath = perfil_zip_path(ano, uf)
    if not zpath.exists() or force or zpath.stat().st_size < 1000:
        url = _PERFIL_URL.format(ano=int(ano), uf=uf)
        console.print(f"[cyan]Baixando perfil do eleitorado[/cyan] {ano} {uf}…")
        tmp = zpath.with_suffix(".zip.part")
        with httpx.Client(timeout=120.0, follow_redirects=True) as client:
            with client.stream("GET", url) as resp:
                resp.raise_for_status()
                with open(tmp, "wb") as fh:
                    for chunk in resp.iter_bytes():
                        fh.write(chunk)
        tmp.replace(zpath)

    with zipfile.ZipFile(zpath) as zf:
        csv_name = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
        payload = zf.read(csv_name)
    header = pd.read_csv(BytesIO(payload), sep=";", encoding="latin-1", nrows=0)
    cols = set(header.columns)
    wanted = [
        c
        for c in (
            "SG_UF",
            "CD_MUNICIPIO",
            "NM_MUNICIPIO",
            "NR_ZONA",
            "NR_SECAO",
            "NR_LOCAL_VOTACAO",
            "NM_LOCAL_VOTACAO",
            "QT_ELEITORES_PERFIL",
        )
        if c in cols
    ]
    raw = pd.read_csv(
        BytesIO(payload), sep=";", encoding="latin-1", dtype=str, usecols=wanted
    )
    if "QT_ELEITORES_PERFIL" not in raw.columns:
        raw["QT_ELEITORES_PERFIL"] = "0"
    raw["aptos_perfil"] = pd.to_numeric(raw["QT_ELEITORES_PERFIL"], errors="coerce").fillna(0)
    for col, dest in (
        ("CD_MUNICIPIO", "municipio"),
        ("NR_ZONA", "zona"),
        ("NR_SECAO", "secao"),
        ("NR_LOCAL_VOTACAO", "local"),
    ):
        if col in raw.columns:
            raw[dest] = (
                raw[col].astype(str).str.lstrip("0").replace("", "0").astype(int)
            )
        else:
            raw[dest] = 0
    nome_mun = raw["NM_MUNICIPIO"] if "NM_MUNICIPIO" in raw.columns else ""
    nome_local = raw["NM_LOCAL_VOTACAO"] if "NM_LOCAL_VOTACAO" in raw.columns else ""
    raw["nome_municipio"] = nome_mun
    raw["nome_local"] = nome_local
    out = (
        raw.groupby(["municipio", "zona", "secao"], as_index=False)
        .agg(
            local=("local", "first"),
            nome_municipio=("nome_municipio", "first"),
            nome_local=("nome_local", "first"),
            aptos_perfil=("aptos_perfil", "sum"),
        )
    )
    out.insert(0, "uf", uf)
    out.insert(1, "ano", int(ano))
    out.to_parquet(cache, index=False)
    console.print(f"[green]Perfil salvo:[/green] {cache.name} ({len(out):,} seções)")
    return out


def ensure_municipios(ufs: list[str]) -> pd.DataFrame:
    """Garante arquivo local com os municípios das UFs pedidas."""
    cache = _load_cache()
    missing = [u.upper() for u in ufs if u.upper() not in set(cache["uf"].unique())]
    if missing:
        frames = [cache] if not cache.empty else []
        for uf in missing:
            frames.append(_fetch_uf(uf))
        cache = pd.concat(frames, ignore_index=True)
        _save_cache(cache)
        console.print(f"[green]Municípios salvos em:[/green] {MUN_CACHE}")
    return cache
