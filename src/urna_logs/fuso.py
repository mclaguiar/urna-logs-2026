"""Fusos locais das urnas e critério oficial de encerramento (≥17h)."""

from __future__ import annotations

from datetime import date

from urna_logs.config import (
    BRT_UTC_OFFSET,
    DATA_TURNO_TOLERANCIA_DIAS,
    FUSO_UTC_OFFSET,
    HORA_ABERTURA_REF,
    HORA_ENCERRAMENTO_REF,
    data_pertence_ao_turno,
)

# Janelas de habilitação (relatório / secao)
JANELA_OFICIAL = "oficial"  # dia do turno, [8h, 17h) na ref.
JANELA_POS = "pos_encerramento"  # dia do turno, ≥17h
JANELA_FORA = "fora_previsto"  # dia do turno, <8h
JANELA_HISTORICO = "historico_outro_dia"  # outro dia no .jez (ex.: 1º no pacote 2º)


def fuso_offset(uf: str) -> int:
    """Offset UTC do relógio local da urna (metadado)."""
    return int(FUSO_UTC_OFFSET.get(uf.upper(), BRT_UTC_OFFSET))


def delta_local_para_brt(uf: str) -> int | None:
    """
    Horas a somar à hora local para obter horário de Brasília.
    None = não converter (exterior ZZ — vale horário local do posto).
    """
    if uf.upper() == "ZZ":
        return None
    return BRT_UTC_OFFSET - fuso_offset(uf)


def hora_brasilia(hora_local: int, uf: str) -> int:
    """Converte hora local do log → hora em Brasília (ZZ: identidade)."""
    delta = delta_local_para_brt(uf)
    if delta is None:
        return int(hora_local) % 24
    return (int(hora_local) + delta) % 24


def apos_encerramento_oficial(hora_local: int | None, uf: str) -> bool:
    """
    True se habilitação ≥ 17h no horário de Brasília
    (ZZ: ≥ 17h no horário local do posto).
    """
    if hora_local is None:
        return False
    return hora_brasilia(int(hora_local), uf) >= HORA_ENCERRAMENTO_REF


def _as_date(value: date | str | None) -> date | None:
    if value is None:
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)


def janela_habilitacao(
    hora_local: int | None,
    uf: str,
    *,
    data_evento: date | str | None,
    data_oficial: date | str | None,
    turno: int | None = None,
) -> str:
    """
    Classifica habilitação:
    - oficial / pos_encerramento / fora_previsto: data na janela do turno
      (dia oficial ± DATA_TURNO_TOLERANCIA_DIAS)
    - historico_outro_dia: fora dessa janela (ex.: 1º turno ainda no .jez do 2º)
    """
    d_ev = _as_date(data_evento)
    d_of = _as_date(data_oficial)
    if d_of is not None or turno is not None:
        if turno is not None:
            no_turno = data_pertence_ao_turno(d_ev, turno)
        else:
            # Compat: só dia exato se não houver turno; preferir turno=…
            tol = DATA_TURNO_TOLERANCIA_DIAS
            no_turno = (
                d_ev is not None
                and d_of is not None
                and abs((d_ev - d_of).days) <= tol
            )
        if not no_turno:
            return JANELA_HISTORICO
    if hora_local is None:
        return JANELA_FORA
    href = hora_brasilia(int(hora_local), uf)
    if href < HORA_ABERTURA_REF:
        return JANELA_FORA
    if href >= HORA_ENCERRAMENTO_REF:
        return JANELA_POS
    return JANELA_OFICIAL
