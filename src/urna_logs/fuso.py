"""Fusos locais das urnas e critério oficial de encerramento (≥17h)."""

from __future__ import annotations

from urna_logs.config import BRT_UTC_OFFSET, FUSO_UTC_OFFSET


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
    return hora_brasilia(int(hora_local), uf) >= 17
