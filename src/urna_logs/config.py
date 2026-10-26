from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
EXTRACT_DIR = DATA_DIR / "extract"
REPORTS_DIR = PROJECT_ROOT / "reports"

ANO = 2026

UFS = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA",
    "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN",
    "RO", "RR", "RS", "SC", "SE", "SP", "TO", "ZZ",
]

# Offset UTC do relógio local da urna (aproximado).
# Referência oficial abertura/encerramento: horário de Brasília (UTC−3),
# exceto exterior (ZZ) = horário local do posto (Res. TSE 23.751/2026).
# AC UTC−5 → fecha ~15h local; AM/MT/MS/RO/RR UTC−4 → ~16h local.
# AM oeste (UTC−5) tratado como −4 no agregado estadual.
FUSO_UTC_OFFSET = {
    "AC": -5,
    "AM": -4,
    "RR": -4,
    "RO": -4,
    "MT": -4,
    "MS": -4,
    "AP": -3,
    "ZZ": -3,
}

BRT_UTC_OFFSET = -3

URL_TEMPLATE = (
    "https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes{ano}/arqurnatot/"
    "bu_imgbu_logjez_rdv_vscmr_{ano}_{turno}t_{uf}.zip"
)

EXT_LOG = (".logjez", ".jez")
EXT_BU = (".bu",)


def zip_url(uf: str, turno: int, ano: int = ANO) -> str:
    return URL_TEMPLATE.format(ano=ano, turno=turno, uf=uf.upper())


def zip_path(uf: str, turno: int, ano: int = ANO) -> Path:
    name = f"bu_imgbu_logjez_rdv_vscmr_{ano}_{turno}t_{uf.upper()}.zip"
    return RAW_DIR / name


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
