"""Medidas do log por seção. As frases vêm de eventos_log.md."""

from __future__ import annotations

import zipfile
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from rich.console import Console

from urna_logs.anomalias.catalogo import FRASES
from urna_logs.anomalias.integridade import cache_ano
from urna_logs.config import (
    HORA_ABERTURA_REF,
    HORA_ENCERRAMENTO_REF,
    data_pertence_ao_turno,
    data_turno,
    zip_path,
)
from urna_logs.fuso import delta_local_para_brt
from urna_logs.parse_log import _events_from_jez_bytes
from urna_logs.thresholds import INTERVALO_MIN_S, SEQ_INTERVALO_MIN
from urna_logs.verificar_vsc import join_key_from_stem
from urna_logs.zip_logs import list_log_members, read_member_from_open_zip

console = Console()


def sequencia_curta(deltas: list[float], piso: float = INTERVALO_MIN_S) -> int:
    """Maior sequência de intervalos consecutivos abaixo do piso."""
    melhor = 0
    atual = 0
    for delta in deltas:
        if delta < piso:
            atual += 1
            if atual > melhor:
                melhor = atual
        else:
            atual = 0
    return melhor


def alerta_intervalo(deltas: list[float]) -> bool:
    return sequencia_curta(deltas) >= SEQ_INTERVALO_MIN


def parse_data_hora_je(valor) -> datetime | None:
    if valor is None or (isinstance(valor, float) and pd.isna(valor)):
        return None
    texto = str(valor).strip()
    if len(texto) >= 15 and texto[8] == "T":
        try:
            return datetime.strptime(texto[:15], "%Y%m%dT%H%M%S")
        except ValueError:
            return None
    return None


def fora_da_janela(
    dt_local: datetime | None,
    uf: str,
    turno: int,
    ano: int,
    fim_local: datetime | None = None,
) -> bool:
    """Voto no dia do turno, fora de 8h–17h de Brasília, ou depois do encerramento do BU."""
    if dt_local is None:
        return False
    if not data_pertence_ao_turno(dt_local.date(), turno, ano=ano):
        return False
    horas = delta_local_para_brt(uf)
    delta = timedelta(hours=0 if horas is None else horas)
    brt = dt_local + delta
    dia = data_turno(turno, ano)
    if dia is None:
        return False
    inicio = datetime(dia.year, dia.month, dia.day, HORA_ABERTURA_REF)
    fim = datetime(dia.year, dia.month, dia.day, HORA_ENCERRAMENTO_REF)
    if fim_local is not None:
        fim_brt = fim_local + delta
        if fim_brt > fim:
            fim = fim_brt
    return brt < inicio or brt > fim


def _stem(membro: str) -> str:
    nome = Path(membro.split(":")[-1]).name
    return nome.split("-")[0].lower()


def _no_dia(dt: datetime | None, turno: int, ano: int) -> bool:
    if dt is None:
        return False
    return data_pertence_ao_turno(dt.date(), turno, ano=ano)


def varrer_logs(
    uf: str,
    turno: int,
    ano: int,
    fim_por_secao: dict[str, datetime | None],
    *,
    force: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    uf = uf.upper()
    destino = cache_ano(ano) / f"logs_{uf}_{turno}t.parquet"
    tempos = cache_ano(ano) / f"tempos_{uf}_{turno}t.parquet"
    if destino.exists() and tempos.exists() and not force:
        return pd.read_parquet(destino), pd.DataFrame()

    zpath = zip_path(uf, turno, ano)
    frase_voto = FRASES["voto_computado"]
    frase_hora = FRASES["ajuste_hora"]
    frase_reinicio = FRASES["reinicio"]
    frases_conting = {FRASES["contingencia_inicio"], FRASES["contingencia_modo"]}
    linhas = []
    marcas = []
    membros = sorted(list_log_members(zpath))
    console.print(f"[cyan]Logs[/cyan] {ano} {uf} {turno}º · {len(membros):,} arquivos")
    with zipfile.ZipFile(zpath) as zf:
        for i, membro in enumerate(membros, start=1):
            if i == 1 or i % 400 == 0 or i == len(membros):
                console.print(f"[dim]  {i:,}/{len(membros):,}[/dim]")
            stem = _stem(membro)
            jk = join_key_from_stem(stem) or ""
            raw = read_member_from_open_zip(zf, membro)
            votos: list[datetime] = []
            ajuste = reinicio = contingencia = 0
            for ev in _events_from_jez_bytes(raw, membro):
                msg = ev.mensagem.strip()
                if msg == frase_voto and _no_dia(ev.dt, turno, ano) and ev.dt is not None:
                    votos.append(ev.dt)
                elif msg == frase_hora and _no_dia(ev.dt, turno, ano):
                    ajuste += 1
                elif msg == frase_reinicio and _no_dia(ev.dt, turno, ano):
                    reinicio += 1
                elif msg in frases_conting and _no_dia(ev.dt, turno, ano):
                    contingencia += 1
            votos.sort()
            deltas = [(b - a).total_seconds() for a, b in zip(votos, votos[1:])]
            fora = sum(
                1
                for dt in votos
                if fora_da_janela(dt, uf, turno, ano, fim_por_secao.get(jk))
            )
            linhas.append(
                {
                    "uf": uf,
                    "ano": ano,
                    "turno": turno,
                    "join_key": jk,
                    "stem": stem,
                    "n_votos_log": len(votos),
                    "n_fora_janela": fora,
                    "seq_curta": sequencia_curta(deltas),
                    "n_ajuste_hora": ajuste,
                    "n_reinicio": reinicio,
                    "n_contingencia": contingencia,
                }
            )
            anterior = None
            for dt in votos:
                delta = None if anterior is None else (dt - anterior).total_seconds()
                marcas.append(
                    {
                        "join_key": jk,
                        "ano": ano,
                        "turno": turno,
                        "t": dt.isoformat(sep=" "),
                        "delta_s": delta,
                    }
                )
                anterior = dt
    frame = pd.DataFrame(linhas)
    tempo = pd.DataFrame(marcas)
    frame.to_parquet(destino, index=False)
    tempo.to_parquet(tempos, index=False)
    return frame, tempo
