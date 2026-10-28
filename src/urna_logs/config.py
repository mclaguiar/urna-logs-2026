from __future__ import annotations

from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
EXTRACT_DIR = DATA_DIR / "extract"
REPORTS_DIR = PROJECT_ROOT / "reports"

ANO = 2026

# Dia oficial da votação (relógio do log = data local da urna).
# Pacotes do 2º frequentemente trazem histórico do 1º no mesmo .jez —
# datas fora da tolerância do dia oficial são "historico_outro_dia" (desprezadas
# nas métricas do turno; ex.: 04/10 dentro do ZIP …_2t_*).
DATA_TURNO: dict[int, date] = {
    1: date(2026, 10, 4),
    2: date(2026, 10, 25),
}
# ±N dias em torno de DATA_TURNO ainda contam como “deste turno”
# (folga de relógio / virada de dia / desencargo). 04/10 vs 25/10 fica bem fora.
DATA_TURNO_TOLERANCIA_DIAS = 3

# Janela oficial de votação (horário de Brasília; ZZ = local do posto).
# ≥17h no dia do turno = pós-encerramento (fila). No dia: <8h = fora do previsto.
HORA_ABERTURA_REF = 8
HORA_ENCERRAMENTO_REF = 17


def data_turno(turno: int) -> date | None:
    return DATA_TURNO.get(int(turno))


def data_pertence_ao_turno(
    data_evento: date | None,
    turno: int,
    *,
    tolerancia_dias: int | None = None,
) -> bool:
    """True se a data do log está na janela do dia oficial deste turno."""
    if data_evento is None:
        return False
    d_of = data_turno(turno)
    if d_of is None:
        return False
    tol = (
        DATA_TURNO_TOLERANCIA_DIAS
        if tolerancia_dias is None
        else int(tolerancia_dias)
    )
    return abs((data_evento - d_of).days) <= tol

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
