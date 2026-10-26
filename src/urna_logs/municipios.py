"""Tabela código TSE → nome do município (perfil eleitorado por seção)."""

from __future__ import annotations

import zipfile
from io import BytesIO
from pathlib import Path

import httpx
import pandas as pd
from rich.console import Console

from urna_logs.config import DATA_DIR, ensure_dirs

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


def ensure_municipios(ufs: list[str]) -> pd.DataFrame:
    """Garante cache local com os municípios das UFs pedidas."""
    cache = _load_cache()
    missing = [u.upper() for u in ufs if u.upper() not in set(cache["uf"].unique())]
    if missing:
        frames = [cache] if not cache.empty else []
        for uf in missing:
            frames.append(_fetch_uf(uf))
        cache = pd.concat(frames, ignore_index=True)
        _save_cache(cache)
        console.print(f"[green]Cache municípios:[/green] {MUN_CACHE}")
    return cache
