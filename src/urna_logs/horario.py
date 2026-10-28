"""Distribuição horária das habilitações (curva do dia + pós-17h)."""

from __future__ import annotations

import os
import re
import zipfile
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import date
from pathlib import Path
from typing import TypedDict

import pandas as pd
from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn, TimeElapsedColumn
from rich.table import Table

from urna_logs.audit import _index_zip_pairs, join_key
from urna_logs.config import (
    REPORTS_DIR,
    data_pertence_ao_turno,
    data_turno,
    ensure_dirs,
    zip_path,
)
from urna_logs.fuso import (
    JANELA_FORA,
    JANELA_HISTORICO,
    JANELA_OFICIAL,
    JANELA_POS,
    apos_encerramento_oficial,
    delta_local_para_brt,
    fuso_offset,
    hora_brasilia,
    janela_habilitacao,
)

# Reexport — testes e callers históricos importavam daqui
__all__ = [
    "apos_encerramento_oficial",
    "delta_local_para_brt",
    "fuso_offset",
    "hora_brasilia",
    "faixa_hora",
    "run_horario",
    "compute_horario_curva",
    "compute_horario_secao",
    "refresh_horario_brt",
]
from urna_logs.parse_log import (
    classify_habilitacoes,
    count_habilitado_hours_from_jez_bytes,
    iter_events_from_zip,
)

# Colunas da curva: contagem e % dentro da hora (não do dia).
TIPO_COLUNAS = (
    ("biometrica", "hab_biometrica", "pct_biometrica", "Com digital"),
    ("manual_falha", "hab_manual", "pct_manual", "Manual"),
    ("sem_biometria", "hab_sem_biometria", "pct_sem_biometria", "Sem biometria"),
    ("desconhecido", "hab_desconhecido", "pct_desconhecido", "Não classificada"),
)
from urna_logs.zip_logs import list_log_members, read_member_from_open_zip

console = Console()

_STEM_RE = re.compile(
    r"(?P<stem>o\d{5}(?P<uf>[a-z]{2})(?P<mun>\d{5})(?P<zona>\d{4})(?P<secao>\d{4}))",
    re.I,
)


def stem_from_source(source: str) -> str | None:
    m = _STEM_RE.search(source.replace("\\", "/").split("/")[-1])
    return m.group("stem").lower() if m else None


def join_key_from_stem(stem: str) -> str | None:
    m = _STEM_RE.fullmatch(stem.lower()) if stem else None
    if not m:
        m = _STEM_RE.search(stem or "")
    if not m:
        return None
    return join_key(
        m.group("uf"),
        int(m.group("mun")),
        int(m.group("zona")),
        int(m.group("secao")),
    )


def faixa_hora(hora: int | None, *, uf: str | None = None) -> str:
    """Faixas pelo horário de referência do encerramento (BRT, ou local se ZZ)."""
    if hora is None:
        return "sem_hora"
    h = hora_brasilia(int(hora), uf) if uf else int(hora)
    if h < 8:
        return "antes_08h"
    if h < 12:
        return "08_12h"
    if h < 17:
        return "12_17h"
    if h < 18:
        return "17_18h"
    if h < 19:
        return "18_19h"
    return "19h_mais"


class HorarioSummary(TypedDict, total=False):
    total_habilitacoes: int
    com_hora: int
    urnas: int
    secoes: int
    pct_apos_17h: float | None
    apos_17h_count: int
    pct_17_18: float | None
    pct_18_19: float | None
    pct_19_mais: float | None
    hora_pico: int | None
    habilitacoes_pico: int
    fuso_utc_offset: int
    delta_para_brt: int | None
    ref_encerramento: str
    modo: str
    data_oficial: str | None
    hab_oficial: int
    hab_pos_encerramento: int
    hab_fora_previsto: int
    hab_historico_outro_dia: int
    pct_oficial: float | None
    pct_fora_previsto: float | None


def _merge_tipo(
    dest: dict[str, list[list[int]]], src: dict[str, list[list[int]]]
) -> None:
    for day, hours in src.items():
        bucket = dest.get(day)
        if bucket is None:
            dest[day] = [[int(c) for c in row] for row in hours]
            continue
        for h, row in enumerate(hours):
            for t, c in enumerate(row):
                bucket[h][t] += int(c)


def _tipo_counts_do_dia(
    by_tipo: dict[str, list[list[int]]], uf: str, turno: int
) -> list[list[int]]:
    """24 horas × 4 tipos, só o dia oficial (histórico de outra data fica de fora)."""
    dia = data_turno(turno)
    dia_iso = dia.isoformat() if dia else None
    out = [[0, 0, 0, 0] for _ in range(24)]
    for day, hours in by_tipo.items():
        for h, row in enumerate(hours):
            if sum(row) <= 0:
                continue
            janela = janela_habilitacao(
                h, uf, data_evento=day, data_oficial=dia_iso, turno=turno
            )
            if janela == JANELA_HISTORICO:
                continue
            for t, c in enumerate(row):
                out[h][t] += int(c)
    return out


def _with_tipo_hora(
    por_hora: pd.DataFrame, counts_tipo: list[list[int]] | None
) -> pd.DataFrame:
    """Acrescenta contagem e % de cada tipo dentro da hora."""
    if counts_tipo is None:
        return por_hora
    out = por_hora.copy()
    habs = out["habilitacoes"].astype(int)
    for idx, (_nome, col, pct_col, _rotulo) in enumerate(TIPO_COLUNAS):
        vals = [
            int(counts_tipo[int(h)][idx]) if 0 <= int(h) < 24 else 0
            for h in out["hora"]
        ]
        out[col] = vals
        out[pct_col] = [
            round(100 * n / hab, 4) if hab else 0.0 for n, hab in zip(vals, habs)
        ]
    return out


def _merge_evento(
    dest: dict[str, list[int]], src: dict[str, list[int]]
) -> None:
    for day, pair in src.items():
        bucket = dest.get(day)
        if bucket is None:
            dest[day] = [int(pair[0]), int(pair[1])]
        else:
            bucket[0] += int(pair[0])
            bucket[1] += int(pair[1])


def _eventos_do_turno(
    by_evento: dict[str, list[int]], turno: int
) -> tuple[int, int]:
    """Votos computados e suspensões sem voto, só em datas deste turno."""
    from datetime import date as _date

    voto = suspenso = 0
    for day, pair in by_evento.items():
        try:
            d = _date.fromisoformat(day)
        except ValueError:
            continue
        if not data_pertence_ao_turno(d, turno):
            continue
        voto += int(pair[0])
        suspenso += int(pair[1])
    return voto, suspenso


def _merge_by_day(
    dest: dict[str, list[int]], src: dict[str, list[int]]
) -> None:
    for day, counts in src.items():
        bucket = dest.get(day)
        if bucket is None:
            dest[day] = list(counts)
        else:
            for h, c in enumerate(counts):
                bucket[h] += c


def _classify_by_day(
    by_day: dict[str, list[int]], uf: str, turno: int
) -> tuple[list[int], int, int, int, int]:
    """
    Só o dia oficial do turno entra nas métricas.
    historico_outro_dia = datas fora de DATA_TURNO ± tolerância (ex.: 1º no .jez do 2º).
    fora_previsto = <8h no dia oficial; oficial = [8,17); pos = ≥17h.
    """
    dia = data_turno(turno)
    dia_iso = dia.isoformat() if dia else None
    counts_dia = [0] * 24
    n_oficial = n_pos = n_fora = n_hist = 0
    for day, counts in by_day.items():
        for h, c in enumerate(counts):
            if c <= 0:
                continue
            janela = janela_habilitacao(
                h, uf, data_evento=day, data_oficial=dia_iso, turno=turno
            )
            if janela == JANELA_HISTORICO:
                n_hist += c
            elif janela == JANELA_FORA:
                n_fora += c
                counts_dia[h] += c
            elif janela == JANELA_POS:
                n_pos += c
                counts_dia[h] += c
            else:
                n_oficial += c
                counts_dia[h] += c
    return counts_dia, n_oficial, n_pos, n_fora, n_hist


def _by_day_frame(by_day: dict[str, list[int]], uf: str, turno: int) -> pd.DataFrame:
    dia = data_turno(turno)
    dia_iso = dia.isoformat() if dia else None
    rows: list[dict] = []
    for day in sorted(by_day):
        counts = by_day[day]
        total = sum(counts)
        for h, c in enumerate(counts):
            if c == 0:
                continue
            janela = janela_habilitacao(
                h, uf, data_evento=day, data_oficial=dia_iso, turno=turno
            )
            try:
                d_ev = date.fromisoformat(day) if isinstance(day, str) else day
            except ValueError:
                d_ev = None
            rows.append(
                {
                    "uf": uf,
                    "turno": turno,
                    "data": day,
                    "hora": h,
                    "habilitacoes": c,
                    "pct_no_dia": round(100 * c / total, 4) if total else 0.0,
                    "dia_do_turno": data_pertence_ao_turno(d_ev, turno),
                    "janela": janela,
                }
            )
    return pd.DataFrame(rows) if rows else pd.DataFrame(
        columns=[
            "uf",
            "turno",
            "data",
            "hora",
            "habilitacoes",
            "pct_no_dia",
            "dia_do_turno",
            "janela",
        ]
    )


def _summary_from_counts_local(
    counts_local: list[int],
    uf: str,
    *,
    urnas: int,
    secoes: int,
    modo: str,
    data_oficial: str | None = None,
    hab_oficial: int = 0,
    hab_pos_encerramento: int = 0,
    hab_fora_previsto: int = 0,
    hab_historico_outro_dia: int = 0,
) -> HorarioSummary:
    """Métricas só do dia oficial do turno (+ diagnóstico de histórico no .jez)."""
    # Total do turno = dia oficial (oficial + pós + <8h). Histórico NÃO entra.
    total = hab_oficial + hab_pos_encerramento + hab_fora_previsto
    if total <= 0:
        total = sum(counts_local)
    no_janela = hab_oficial + hab_pos_encerramento
    counts_ref = [0] * 24
    for h_local, c in enumerate(counts_local):
        counts_ref[hora_brasilia(h_local, uf)] += c
    apos = hab_pos_encerramento or sum(counts_ref[17:])
    f17, f18, f19 = counts_ref[17], counts_ref[18], sum(counts_ref[19:])
    hora_pico_local = (
        max(range(24), key=lambda h: counts_local[h]) if sum(counts_local) else None
    )
    ref = "local" if uf.upper() == "ZZ" else "brasilia"
    den = no_janela if no_janela else None
    return {
        "total_habilitacoes": int(total),
        "com_hora": int(total),
        "urnas": urnas,
        "secoes": secoes,
        "pct_apos_17h": round(100 * apos / den, 4) if den else None,
        "apos_17h_count": int(apos),
        "pct_17_18": round(100 * f17 / den, 4) if den else None,
        "pct_18_19": round(100 * f18 / den, 4) if den else None,
        "pct_19_mais": round(100 * f19 / den, 4) if den else None,
        "hora_pico": hora_pico_local,
        "habilitacoes_pico": counts_local[hora_pico_local]
        if hora_pico_local is not None
        else 0,
        "fuso_utc_offset": fuso_offset(uf),
        "delta_para_brt": delta_local_para_brt(uf),
        "ref_encerramento": ref,
        "modo": modo,
        "data_oficial": data_oficial,
        "hab_oficial": int(hab_oficial),
        "hab_pos_encerramento": int(hab_pos_encerramento),
        "hab_fora_previsto": int(hab_fora_previsto),
        "hab_historico_outro_dia": int(hab_historico_outro_dia),
        "pct_oficial": round(100 * hab_oficial / total, 4) if total else None,
        "pct_fora_previsto": round(100 * hab_fora_previsto / total, 4)
        if total
        else None,
    }


def annotate_por_hora(por_hora: pd.DataFrame, uf: str) -> pd.DataFrame:
    """Marca after_17h pelo critério oficial (BRT, exceto ZZ)."""
    out = por_hora.copy()
    out["hora_brasilia"] = out["hora"].map(lambda h: hora_brasilia(int(h), uf))
    out["after_17h"] = out["hora"].map(
        lambda h: apos_encerramento_oficial(int(h), uf)
    )
    return out


def _count_chunk(payload: tuple[str, list[str], str | None]) -> dict:
    """
    Processo filho: abre o ZIP **uma vez** e processa um lote de membros.
    Evita 1 ZipFile.open por log (matava UFs grandes tipo BA ~35k logs).
    payload = (zip_path, members, data_filtro ISO ou None).
    """
    from datetime import date as _date

    zpath_s, members, data_iso = payload
    data_filtro = _date.fromisoformat(data_iso) if data_iso else None
    counts = [0] * 24
    urnas: set[str] = set()
    stems: set[str] = set()
    by_day: dict[str, list[int]] = {}
    by_tipo: dict[str, list[list[int]]] = {}
    by_evento: dict[str, list[int]] = {}
    with zipfile.ZipFile(zpath_s) as zf:
        for member in members:
            raw = read_member_from_open_zip(zf, member)
            part, ids, days = count_habilitado_hours_from_jez_bytes(
                raw,
                data_filtro=data_filtro,
                by_tipo=by_tipo,
                by_evento=by_evento,
            )
            for h, c in enumerate(part):
                counts[h] += c
            urnas.update(ids)
            _merge_by_day(by_day, days)
            st = stem_from_source(member)
            if st:
                stems.add(st)
    return {
        "counts": counts,
        "total": sum(counts),
        "n_logs": len(members),
        "urnas": list(urnas),
        "stems": list(stems),
        "by_day": by_day,
        "by_tipo": by_tipo,
        "by_evento": by_evento,
    }


def _count_chunk_secao(payload: tuple[str, list[str], str | None, str, int]) -> dict:
    """
    Processo filho: stem → contagens por janela + curva do dia oficial.
    payload = (zip, members, data_oficial ISO|None, uf, turno).
    """
    zpath_s, members, data_iso, uf, turno = payload
    by_stem: dict[str, dict] = {}
    with zipfile.ZipFile(zpath_s) as zf:
        for member in members:
            raw = read_member_from_open_zip(zf, member)
            _part, _ids, days = count_habilitado_hours_from_jez_bytes(raw)
            st = stem_from_source(member)
            if not st:
                continue
            slot = by_stem.get(st)
            if slot is None:
                slot = {
                    "counts_dia": [0] * 24,
                    "oficial": 0,
                    "pos": 0,
                    "fora": 0,
                    "historico": 0,
                }
                by_stem[st] = slot
            for day, counts in days.items():
                for h, c in enumerate(counts):
                    if c <= 0:
                        continue
                    janela = janela_habilitacao(
                        h, uf, data_evento=day, data_oficial=data_iso, turno=turno
                    )
                    if janela == JANELA_HISTORICO:
                        slot["historico"] += c
                    elif janela == JANELA_FORA:
                        slot["fora"] += c
                        slot["counts_dia"][h] += c
                    elif janela == JANELA_POS:
                        slot["pos"] += c
                        slot["counts_dia"][h] += c
                    else:
                        slot["oficial"] += c
                        slot["counts_dia"][h] += c
    # progresso = só o dia do turno (não misturar histórico do outro turno)
    total = sum(
        int(s["oficial"]) + int(s["pos"]) + int(s["fora"]) for s in by_stem.values()
    )
    return {
        "by_stem": by_stem,
        "n_logs": len(members),
        "total": total,
    }


def _sum_bu_chunk(payload: tuple[str, list[str]]) -> dict:
    """Soma votos de presidente (nominal, branco, nulo e demais) num lote de BUs."""
    from urna_logs.bu_rdv import parse_bu_bytes

    zpath_s, names = payload
    nominal = branco = nulo = outros = urnas = erros = 0
    with zipfile.ZipFile(zpath_s) as zf:
        for name in names:
            try:
                tot = parse_bu_bytes(zf.read(name), source=name)
            except Exception:  # noqa: BLE001 — um BU ilegível não derruba a UF
                erros += 1
                continue
            if tot is None:
                erros += 1
                continue
            urnas += 1
            for (tipo, _numero), qtd in tot.votos.items():
                q = int(qtd)
                if tipo == "nominal":
                    nominal += q
                elif tipo == "branco":
                    branco += q
                elif tipo == "nulo":
                    nulo += q
                else:
                    outros += q
    return {
        "bu_nominal": nominal,
        "bu_branco": branco,
        "bu_nulo": nulo,
        "bu_outros": outros,
        "bu_urnas": urnas,
        "bu_erros": erros,
    }


def sum_votos_presidente_bu(
    uf: str, turno: int, *, workers: int | None = None
) -> dict | None:
    """
    Total de votos de presidente no BU da UF: nominais + brancos + nulos
    (e qualquer outro tipo do cargo). Um BU por urna, como na auditoria.
    """
    zpath = zip_path(uf, turno)
    if not zpath.exists():
        return None
    with zipfile.ZipFile(zpath) as zf:
        names = [
            files["bu"]
            for files in _index_zip_pairs(zf).values()
            if files.get("bu")
        ]
    if not names:
        return None
    n_workers = workers or min(8, max(1, (os.cpu_count() or 4)))
    lote = 400 if len(names) >= 64 else max(len(names), 1)
    chunks = _chunked_by_size(names, lote)
    use_pool = len(names) >= 64 and n_workers > 1 and len(chunks) > 1
    console.print(
        f"[dim]  {uf.upper()}: votos de presidente no BU · "
        f"{len(names):,} urnas[/dim]"
    )
    parts: list[dict] = []
    payloads = [(str(zpath), chunk) for chunk in chunks]
    if use_pool:
        with ProcessPoolExecutor(max_workers=n_workers) as pool:
            parts.extend(pool.map(_sum_bu_chunk, payloads))
    else:
        parts.extend(_sum_bu_chunk(p) for p in payloads)
    nominal = branco = nulo = outros = urnas = erros = 0
    for part in parts:
        nominal += part["bu_nominal"]
        branco += part["bu_branco"]
        nulo += part["bu_nulo"]
        outros += part["bu_outros"]
        urnas += part["bu_urnas"]
        erros += part["bu_erros"]
    return {
        "bu_votos_presidente": nominal + branco + nulo + outros,
        "bu_nominal": nominal,
        "bu_branco": branco,
        "bu_nulo": nulo,
        "bu_outros": outros,
        "bu_urnas": urnas,
        "bu_erros": erros,
    }


def _anexar_confronto_bu(
    summary: dict, uf: str, turno: int, *, workers: int | None = None
) -> dict:
    bu = sum_votos_presidente_bu(uf, turno, workers=workers)
    if not bu:
        return summary
    out = dict(summary)
    out.update(bu)
    out["delta_hab_menos_bu"] = int(out.get("total_habilitacoes") or 0) - int(
        bu["bu_votos_presidente"]
    )
    return out


def _nota_hab_sem_voto(summary: dict) -> list[str]:
    """Nota curta no resumo, só quando habilitações e votos do BU não fecham."""
    if summary.get("delta_hab_menos_bu") is None:
        return []
    delta = int(summary["delta_hab_menos_bu"])
    if delta == 0:
        return []
    if delta < 0:
        return [
            f"  - O BU registra **{-delta:,}** votos de presidente a mais do que as habilitações do log.",
        ]
    linhas = [
        f"  - **{delta:,}** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.",
    ]
    if summary.get("log_suspensos_sem_voto") is not None:
        suspensos = int(summary["log_suspensos_sem_voto"])
        resto = delta - suspensos
        linhas.append(
            f"  - **{suspensos:,}** com a frase «Eleitor foi suspenso e não confirmou nenhum voto»."
        )
        if resto > 0:
            linhas.append(
                f"  - **{resto:,}** sem essa frase; o voto também não foi computado."
            )
    return linhas


def _linhas_confronto_bu(summary: dict) -> list[str]:
    """Apontamento: habilitações do log × votos de presidente no BU."""
    if summary.get("bu_votos_presidente") is None:
        return []
    hab = int(summary.get("total_habilitacoes") or 0)
    votos = int(summary["bu_votos_presidente"])
    delta = int(summary.get("delta_hab_menos_bu", hab - votos))
    nominal = int(summary.get("bu_nominal") or 0)
    branco = int(summary.get("bu_branco") or 0)
    nulo = int(summary.get("bu_nulo") or 0)
    outros = int(summary.get("bu_outros") or 0)
    computados = summary.get("log_votos_computados")
    suspensos = summary.get("log_suspensos_sem_voto")
    linhas = [
        "",
        "## Habilitações × votos de presidente (BU)",
        "",
        "Apontamento. Cada habilitação no dia oficial deveria corresponder a um "
        "voto de presidente no boletim: nominal, branco ou nulo.",
        "",
        f"- Habilitações no log: **{hab:,}**",
    ]
    if computados is not None:
        linhas.append(
            f"- Votos computados no log (`O voto do eleitor foi computado`): "
            f"**{int(computados):,}**"
        )
    linhas += [
        f"- Votos de presidente no BU: **{votos:,}**",
        f"  - nominais **{nominal:,}** · brancos **{branco:,}** · nulos **{nulo:,}**",
    ]
    if outros:
        linhas.append(f"  - outros tipos do cargo: **{outros:,}**")
    if delta == 0:
        linhas += [
            "",
            "A diferença é **0**. Cada habilitação do dia tem um voto de presidente no BU.",
        ]
    elif delta > 0:
        linhas += [
            "",
            f"**{delta:+,}** são habilitações feitas em que o voto **não foi registrado**. "
            "A votação foi interrompida antes da confirmação. "
            "O boletim não recebe esse voto.",
        ]
        if computados is not None and int(computados) == votos:
            linhas.append(
                f"Os votos que o log marca como computados fecham com o BU "
                f"(**{int(computados):,}** = **{votos:,}**). "
                f"O {delta:+,} está fora dessa conta."
            )
        elif computados is not None:
            linhas.append(
                f"Votos computados no log (**{int(computados):,}**) e votos do BU "
                f"(**{votos:,}**) diferem em **{int(computados) - votos:+,}**."
            )
        if suspensos is not None:
            suspensos_n = int(suspensos)
            resto = delta - suspensos_n
            linhas.append(
                f"- **{suspensos_n:,}** — o mesário suspendeu o eleitor. "
                "O log diz «Eleitor foi suspenso e não confirmou nenhum voto»."
            )
            if resto > 0:
                linhas.append(
                    f"- **{resto:,}** — o voto também não foi registrado, "
                    "e o log não traz essa frase."
                )
            elif resto < 0:
                linhas.append(
                    f"- A frase de suspensão aparece **{-resto:,}** vezes "
                    "a mais do que essa diferença."
                )
    else:
        linhas += [
            "",
            f"**{delta:+,}**: o BU tem **{-delta:,}** votos de presidente "
            "a mais do que as habilitações do log.",
        ]
    erros = int(summary.get("bu_erros") or 0)
    if erros:
        linhas.append(f"BUs não lidos: **{erros:,}**.")
    return linhas


def _chunked_by_size(items: list[str], size: int) -> list[list[str]]:
    size = max(1, size)
    return [items[i : i + size] for i in range(0, len(items), size)]


def compute_horario_curva(
    uf: str,
    turno: int,
    *,
    workers: int | None = None,
    on_progress: Callable[[int, int, int, int, int], None] | None = None,
) -> tuple[pd.DataFrame, dict, pd.DataFrame]:
    """
    Modo rápido: agrega hora→contagem em lotes paralelos (1 ZipFile/lote).
    Filtra pelo dia oficial do turno; também devolve breakdown dia×hora.
    Não grava Parquet detalhado (1 linha/habilitação).

    on_progress(done_logs, total_logs, hab, lote_i, n_lotes) — opcional.
    """
    ensure_dirs()
    uf = uf.upper()
    zpath = zip_path(uf, turno)
    if not zpath.exists():
        raise FileNotFoundError(f"ZIP não encontrado: {zpath}")

    zip_mb = zpath.stat().st_size / (1024 * 1024)
    console.print(
        f"[dim]  {uf}: lendo índice do ZIP ({zip_mb:,.0f} MB)…[/dim]"
    )
    members = list_log_members(zpath)
    urnas: set[str] = set()
    stems: set[str] = set()
    by_day: dict[str, list[int]] = {}
    by_tipo: dict[str, list[list[int]]] = {}
    by_evento: dict[str, list[int]] = {}
    hab_so_far = 0
    logs_done = 0
    dia = data_turno(turno)
    data_iso = dia.isoformat() if dia else None

    n_workers = workers or min(8, max(1, (os.cpu_count() or 4)))
    # ~500 logs/lote → barra atualiza com frequência sem reabrir o ZIP demais
    lote_size = 500 if len(members) >= 64 else max(len(members), 1)
    chunks = _chunked_by_size(members, lote_size)
    n_lotes = len(chunks)
    use_pool = len(members) >= 64 and n_workers > 1 and n_lotes > 1

    console.print(
        f"[dim]  {uf}: {len(members):,} logs · {n_lotes} lote(s) "
        f"(~{lote_size}/lote) · "
        f"{'pool '+str(n_workers)+' workers' if use_pool else 'série'}"
        f"{' · dia oficial '+data_iso if data_iso else ''}[/dim]"
    )

    def _absorb(part: dict, lote_i: int) -> None:
        nonlocal hab_so_far, logs_done
        # counts brutos (todos os dias) só para progresso; curva vem de by_day
        urnas.update(part["urnas"])
        stems.update(part["stems"])
        _merge_by_day(by_day, part.get("by_day") or {})
        _merge_tipo(by_tipo, part.get("by_tipo") or {})
        _merge_evento(by_evento, part.get("by_evento") or {})
        logs_done += int(part["n_logs"])
        hab_so_far += int(part["total"])
        if on_progress:
            on_progress(logs_done, len(members), hab_so_far, lote_i, n_lotes)
        else:
            console.print(
                f"[dim]  {uf}: lote {lote_i}/{n_lotes} · "
                f"{logs_done:,}/{len(members):,} logs · "
                f"{hab_so_far:,} hab[/dim]"
            )

    # data_filtro=None → conta todos os dias; classificação na agregação
    payload_chunks = [(str(zpath), chunk, None) for chunk in chunks]
    if use_pool:
        with ProcessPoolExecutor(max_workers=n_workers) as pool:
            futures = {
                pool.submit(_count_chunk, payload): i
                for i, payload in enumerate(payload_chunks, start=1)
            }
            finished = 0
            for fut in as_completed(futures):
                finished += 1
                _absorb(fut.result(), finished)
    else:
        for i, payload in enumerate(payload_chunks, start=1):
            _absorb(_count_chunk(payload), i)

    counts_dia, n_oficial, n_pos, n_fora, n_hist = _classify_by_day(
        by_day, uf, turno
    )
    den = n_oficial + n_pos + n_fora
    por_hora = annotate_por_hora(
        pd.DataFrame(
            {
                "uf": uf,
                "turno": turno,
                "hora": list(range(24)),
                "habilitacoes": counts_dia,
                "pct": [
                    round(100 * c / den, 4) if den else 0.0 for c in counts_dia
                ],
            }
        ),
        uf,
    )
    summary = _summary_from_counts_local(
        counts_dia,
        uf,
        urnas=len(urnas),
        secoes=len(stems),
        modo="curva",
        data_oficial=data_iso,
        hab_oficial=n_oficial,
        hab_pos_encerramento=n_pos,
        hab_fora_previsto=n_fora,
        hab_historico_outro_dia=n_hist,
    )
    votos_log, suspensos = _eventos_do_turno(by_evento, turno)
    summary["log_votos_computados"] = votos_log
    summary["log_suspensos_sem_voto"] = suspensos
    por_hora = _with_tipo_hora(por_hora, _tipo_counts_do_dia(by_tipo, uf, turno))
    return por_hora, summary, _by_day_frame(by_day, uf, turno)


def compute_horario_secao(
    uf: str,
    turno: int,
    *,
    workers: int | None = None,
    on_progress: Callable[[int, int, int, int, int], None] | None = None,
) -> pd.DataFrame:
    """
    Agrega habilitações pós-17h por seção (`join_key`), sem Parquet 1-linha/hab.
    Mesmo scan em lotes do modo curva.
    """
    ensure_dirs()
    uf = uf.upper()
    zpath = zip_path(uf, turno)
    if not zpath.exists():
        raise FileNotFoundError(f"ZIP não encontrado: {zpath}")

    members = list_log_members(zpath)
    by_stem: dict[str, dict] = {}
    logs_done = 0
    hab_so_far = 0
    dia = data_turno(turno)
    data_iso = dia.isoformat() if dia else None

    n_workers = workers or min(8, max(1, (os.cpu_count() or 4)))
    lote_size = 500 if len(members) >= 64 else max(len(members), 1)
    chunks = _chunked_by_size(members, lote_size)
    n_lotes = len(chunks)
    use_pool = len(members) >= 64 and n_workers > 1 and n_lotes > 1

    console.print(
        f"[dim]  {uf} secao: {len(members):,} logs · {n_lotes} lote(s) · "
        f"{'pool '+str(n_workers) if use_pool else 'série'}"
        f"{' · dia oficial '+data_iso if data_iso else ''}[/dim]"
    )

    def _absorb(part: dict, lote_i: int) -> None:
        nonlocal logs_done, hab_so_far
        for st, slot in part["by_stem"].items():
            cur = by_stem.get(st)
            if cur is None:
                cur = {
                    "counts_dia": [0] * 24,
                    "oficial": 0,
                    "pos": 0,
                    "fora": 0,
                    "historico": 0,
                }
                by_stem[st] = cur
            for h, c in enumerate(slot["counts_dia"]):
                cur["counts_dia"][h] += c
            cur["oficial"] += int(slot["oficial"])
            cur["pos"] += int(slot["pos"])
            cur["fora"] += int(slot["fora"])
            cur["historico"] += int(slot.get("historico") or 0)
        logs_done += int(part["n_logs"])
        hab_so_far += int(part["total"])
        if on_progress:
            on_progress(logs_done, len(members), hab_so_far, lote_i, n_lotes)
        else:
            console.print(
                f"[dim]  {uf} secao: lote {lote_i}/{n_lotes} · "
                f"{logs_done:,}/{len(members):,} logs · {hab_so_far:,} hab[/dim]"
            )

    payload_chunks = [(str(zpath), chunk, data_iso, uf, turno) for chunk in chunks]
    if use_pool:
        with ProcessPoolExecutor(max_workers=n_workers) as pool:
            futures = {
                pool.submit(_count_chunk_secao, payload): i
                for i, payload in enumerate(payload_chunks, start=1)
            }
            finished = 0
            for fut in as_completed(futures):
                finished += 1
                _absorb(fut.result(), finished)
    else:
        for i, payload in enumerate(payload_chunks, start=1):
            _absorb(_count_chunk_secao(payload), i)

    rows: list[dict] = []
    for stem, slot in by_stem.items():
        jk = join_key_from_stem(stem)
        if not jk:
            continue
        oficial = int(slot["oficial"])
        pos = int(slot["pos"])
        fora = int(slot["fora"])
        hist = int(slot.get("historico") or 0)
        # Totais do turno = só o dia oficial (histórico fica à parte)
        no_janela = oficial + pos
        total_turno = no_janela + fora
        rows.append(
            {
                "uf": uf,
                "turno": turno,
                "stem": stem,
                "join_key": jk,
                "hab_total": total_turno,
                "hab_oficial": oficial,
                "hab_apos_17h": pos,
                "hab_fora_previsto": fora,
                "hab_historico_outro_dia": hist,
                "pct_apos_17h": round(100 * pos / no_janela, 4) if no_janela else None,
                "pct_fora_previsto": round(100 * fora / total_turno, 4)
                if total_turno
                else None,
            }
        )
    return pd.DataFrame(rows) if rows else pd.DataFrame(
        columns=[
            "uf",
            "turno",
            "stem",
            "join_key",
            "hab_total",
            "hab_oficial",
            "hab_apos_17h",
            "hab_fora_previsto",
            "hab_historico_outro_dia",
            "pct_apos_17h",
            "pct_fora_previsto",
        ]
    )


def write_horario_secao(df: pd.DataFrame, uf: str, turno: int) -> Path:
    ensure_dirs()
    path = REPORTS_DIR / f"horario_secao_{uf.upper()}_{turno}t.parquet"
    df.to_parquet(path, index=False)
    return path


def compute_horario(uf: str, turno: int) -> pd.DataFrame:
    """Modo detalhe: 1 linha por habilitação (mais lento; para cruzamentos finos)."""
    ensure_dirs()
    uf = uf.upper()
    zpath = zip_path(uf, turno)
    if not zpath.exists():
        raise FileNotFoundError(f"ZIP não encontrado: {zpath}")

    dia = data_turno(turno)
    rows: list[dict] = []
    for hab in classify_habilitacoes(iter_events_from_zip(zpath), uf=uf):
        stem = stem_from_source(hab.source)
        jk = join_key_from_stem(stem) if stem else None
        hora = hab.dt.hour if hab.dt is not None else None
        data_ev = hab.dt.date() if hab.dt is not None else None
        janela = janela_habilitacao(
            hora, uf, data_evento=data_ev, data_oficial=dia, turno=turno
        )
        rows.append(
            {
                "uf": uf,
                "turno": turno,
                "fuso_utc_offset": fuso_offset(uf),
                "delta_para_brt": delta_local_para_brt(uf),
                "id_ue": hab.id_ue,
                "stem": stem or "",
                "join_key": jk or "",
                "source": hab.source,
                "dt": hab.dt.isoformat(sep=" ") if hab.dt else None,
                "hora": hora,
                "hora_brasilia": hora_brasilia(hora, uf) if hora is not None else None,
                "faixa": faixa_hora(hora, uf=uf),
                "after_17h": hab.after_17h,
                "janela": janela,
                "tipo": hab.tipo,
            }
        )
    if not rows:
        return pd.DataFrame(
            columns=[
                "uf",
                "turno",
                "fuso_utc_offset",
                "delta_para_brt",
                "id_ue",
                "stem",
                "join_key",
                "source",
                "dt",
                "hora",
                "hora_brasilia",
                "faixa",
                "after_17h",
                "janela",
                "tipo",
            ]
        )
    return pd.DataFrame(rows)


def aggregate_por_hora(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or df["hora"].isna().all():
        return pd.DataFrame(
            columns=[
                "uf",
                "turno",
                "hora",
                "habilitacoes",
                "pct",
                "hora_brasilia",
                "after_17h",
            ]
        )
    uf = str(df["uf"].iloc[0]).upper()
    turno = int(df["turno"].iloc[0])
    total = int(df["hora"].notna().sum())
    counts = (
        df.dropna(subset=["hora"])
        .groupby("hora", as_index=False)
        .size()
        .rename(columns={"size": "habilitacoes"})
    )
    full = pd.DataFrame({"hora": list(range(24))})
    out = full.merge(counts, on="hora", how="left")
    out["habilitacoes"] = out["habilitacoes"].fillna(0).astype(int)
    out["pct"] = out["habilitacoes"].apply(
        lambda n: round(100 * n / total, 4) if total else 0.0
    )
    out["uf"] = uf
    out["turno"] = turno
    if "tipo" in df.columns:
        src = df.dropna(subset=["hora"])
        known = {nome for nome, _c, _p, _r in TIPO_COLUNAS}
        tmp = src.copy()
        tmp["tipo"] = tmp["tipo"].where(tmp["tipo"].isin(known), "desconhecido")
        counts_tipo = [[0, 0, 0, 0] for _ in range(24)]
        if not tmp.empty:
            for (hora, tipo), n in tmp.groupby(["hora", "tipo"]).size().items():
                h = int(hora)
                idx = next(i for i, (nome, *_rest) in enumerate(TIPO_COLUNAS) if nome == tipo)
                if 0 <= h < 24:
                    counts_tipo[h][idx] = int(n)
        return _with_tipo_hora(
            annotate_por_hora(out[["uf", "turno", "hora", "habilitacoes", "pct"]], uf),
            counts_tipo,
        )
    return annotate_por_hora(
        out[["uf", "turno", "hora", "habilitacoes", "pct"]], uf
    )


def summarize_horario(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "total_habilitacoes": 0,
            "com_hora": 0,
            "urnas": 0,
            "secoes": 0,
            "pct_apos_17h": None,
            "apos_17h_count": 0,
            "pct_17_18": None,
            "pct_18_19": None,
            "pct_19_mais": None,
            "hora_pico": None,
            "habilitacoes_pico": 0,
            "modo": "detalhe",
        }
    uf = str(df["uf"].iloc[0]).upper()
    turno = int(df["turno"].iloc[0]) if "turno" in df.columns else 0
    dia = data_turno(turno)
    com_hora = df[df["hora"].notna()]
    if "janela" in df.columns:
        n_oficial = int((df["janela"] == JANELA_OFICIAL).sum())
        n_pos = int((df["janela"] == JANELA_POS).sum())
        n_fora = int((df["janela"] == JANELA_FORA).sum())
        n_hist = int((df["janela"] == JANELA_HISTORICO).sum())
        dia_mask = df["janela"].isin([JANELA_OFICIAL, JANELA_POS, JANELA_FORA])
        counts_src = df.loc[dia_mask & df["hora"].notna()]
    else:
        n_oficial = n_pos = n_fora = n_hist = 0
        counts_src = com_hora
    counts = [0] * 24
    for h, n in counts_src.groupby("hora").size().items():
        counts[int(h)] = int(n)
    base = _summary_from_counts_local(
        counts,
        uf,
        urnas=int(df["id_ue"].nunique()),
        secoes=int(df.loc[df["join_key"] != "", "join_key"].nunique()),
        modo="detalhe",
        data_oficial=dia.isoformat() if dia else None,
        hab_oficial=n_oficial,
        hab_pos_encerramento=n_pos,
        hab_fora_previsto=n_fora,
        hab_historico_outro_dia=n_hist,
    )
    return base


def write_horario_reports(
    por_hora: pd.DataFrame,
    summary: dict,
    uf: str,
    turno: int,
    *,
    detail: pd.DataFrame | None = None,
    por_dia: pd.DataFrame | None = None,
) -> tuple[Path, ...]:
    ensure_dirs()
    uf = uf.upper()
    hora_csv = REPORTS_DIR / f"curva_horaria_{uf}_{turno}t.csv"
    summary_csv = REPORTS_DIR / f"horario_summary_{uf}_{turno}t.csv"
    md = REPORTS_DIR / f"horario_{uf}_{turno}t.md"
    outputs: list[Path] = []

    if detail is not None:
        detail_path = REPORTS_DIR / f"horario_{uf}_{turno}t.parquet"
        detail.to_parquet(detail_path, index=False)
        outputs.append(detail_path)

    if por_dia is not None and not por_dia.empty:
        dia_csv = REPORTS_DIR / f"curva_horaria_dia_{uf}_{turno}t.csv"
        por_dia.to_csv(dia_csv, index=False)
        outputs.append(dia_csv)

    por_hora.to_csv(hora_csv, index=False)
    pd.DataFrame([{**summary, "uf": uf, "turno": turno}]).to_csv(summary_csv, index=False)

    modo = summary.get("modo", "curva")
    ref = summary.get("ref_encerramento", "local" if uf == "ZZ" else "brasilia")
    data_f = summary.get("data_oficial")
    if ref == "local":
        criterio = "janela 8h–17h no **horário local** (exterior); ≥17h = pós-encerramento"
    else:
        delta = summary.get("delta_para_brt")
        extra = (
            f" (local +{delta}h → BRT)"
            if isinstance(delta, int) and delta
            else ""
        )
        criterio = f"janela **8h–17h Brasília**{extra}; ≥17h = pós-encerramento (fila)"
    lines = [
        f"# Curva horária — {uf} {turno}º turno",
        "",
        f"Modo: **{modo}**"
        + (" (agregado; sem Parquet detalhado)" if modo == "curva" else " (1 linha/habilitação)"),
        "",
        "Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).",
        "Não é horário do voto em cada cargo.",
        "",
        f"Relógio do log = **hora local** da urna "
        f"(metadado fuso UTC{summary.get('fuso_utc_offset', -3):+d}).",
        f"Critério: {criterio}.",
        "",
        "Métricas deste relatório = **somente o dia oficial deste turno**.",
        "Janelas no dia: **oficial** [8h,17h) · **pós-encerramento** ≥17h · "
        "**fora do previsto** &lt;8h.",
        "Eventos de **outra data** no `.jez` = histórico (não entram nos totais nem no comparativo 1º×2º).",
    ]
    if data_f:
        lines.append(f"Dia oficial deste turno: **{data_f}**.")
    hist = int(summary.get("hab_historico_outro_dia") or 0)
    lines += [
        "",
        "## Resumo (só o dia do turno)",
        "",
        f"- Habilitações no dia: **{summary['total_habilitacoes']:,}**",
    ]
    lines += _nota_hab_sem_voto(summary)
    lines += [
        f"- Oficial [8h,17h): **{summary.get('hab_oficial', 0):,}** "
        f"({summary.get('pct_oficial')}%)",
        f"- Pós-encerramento ≥17h: **{summary.get('hab_pos_encerramento', 0):,}** "
        f"(% entre oficial+pós: **{summary['pct_apos_17h']}**)",
        f"- Fora do previsto (&lt;8h no dia): **{summary.get('hab_fora_previsto', 0):,}** "
        f"({summary.get('pct_fora_previsto')}%)",
        f"- Seções: **{summary['secoes']:,}** · urnas: **{summary['urnas']:,}**",
        f"- Pico (hora local): **{summary['hora_pico']}h** "
        f"({summary['habilitacoes_pico']:,})",
        f"- Faixas ≥17h (ref. {ref}): 17–18h **{summary['pct_17_18']}** · "
        f"18–19h **{summary['pct_18_19']}** · 19h+ **{summary['pct_19_mais']}**",
    ]
    if hist:
        lines.append(
            f"- Histórico de **outras datas** no mesmo log (ignorado neste turno): "
            f"**{hist:,}** — ver seção abaixo / `curva_horaria_dia_*`"
        )
    lines += _linhas_confronto_bu(summary)
    tem_tipo = "hab_biometrica" in por_hora.columns
    if tem_tipo:
        total_dia = int(por_hora["habilitacoes"].sum())
        linhas_tipo = []
        for _nome, col, _pct, rotulo in TIPO_COLUNAS:
            n = int(por_hora[col].sum())
            pct_dia = round(100 * n / total_dia, 2) if total_dia else 0.0
            linhas_tipo.append(f"- {rotulo}: **{n:,}** ({pct_dia}% do dia)")
        lines += [
            "",
            "## Como foi a habilitação",
            "",
            "No **boletim (BU)** há três caminhos:",
            "",
            "- **Com digital:** a urna reconheceu a digital do eleitor.",
            "- **Biografia:** tinha digital cadastrada, o reconhecimento não fechou, "
            "e a liberação foi pelo ano de nascimento mais a digital do mesário.",
            "- **Sem biometria:** não tinha digital cadastrada, e a liberação foi a mesma "
            "(ano de nascimento mais a digital do mesário).",
            "",
            "Sem digital no BU = biografia + sem biometria.",
            "",
            "Neste relatório a fonte é o **log**, nas linhas anteriores a "
            "`Eleitor foi habilitado`:",
            "",
            "- **Com digital:** `Tipo de habilitação do eleitor [biométrica]`.",
            "- **Manual:** ano de nascimento conferido, pedido de habilitação manual "
            "ou digital do mesário. Em 2026 o log usa essas mesmas frases para "
            "biografia e para sem biometria, então os dois caminhos caem aqui.",
            "- **Sem biometria:** só entra se o log escrever "
            "`O eleitor não possui biometria` ou `Eleitor sem dados biométricos`. "
            "Quando essa frase não aparece, a coluna fica em zero e esses eleitores "
            "estão dentro de Manual.",
            "- **Não classificada:** a janela anterior não trouxe nenhum desses sinais.",
            "",
            "### Totais do dia",
            "",
        ] + linhas_tipo
    lines += [
        "",
        "## Distribuição horária (dia oficial · relógio local)",
        "",
    ]
    if tem_tipo:
        lines += [
            "Percentuais de tipo são **dentro da hora**.",
            "",
            "| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |",
            "|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    else:
        lines += [
            "| Hora local | Habilitações | % no dia | Janela |",
            "|---:|---:|---:|:---|",
        ]
    for _, row in por_hora.iterrows():
        if int(row["habilitacoes"]) == 0:
            continue
        h = int(row["hora"])
        if bool(row.get("after_17h")):
            janela = "pós-encerramento"
        elif hora_brasilia(h, uf) < 8:
            janela = "fora (<8h)"
        else:
            janela = "oficial"
        celulas = [
            f"{h:02d}h",
            f"{int(row['habilitacoes']):,}",
            f"{row['pct']}",
            janela,
        ]
        if tem_tipo:
            for _nome, col, pct_col, _rotulo in TIPO_COLUNAS:
                celulas.append(f"{int(row[col]):,}")
                celulas.append(f"{row[pct_col]}")
        lines.append("| " + " | ".join(celulas) + " |")
    if por_dia is not None and not por_dia.empty:
        outros = por_dia.loc[por_dia["janela"] == JANELA_HISTORICO] if "janela" in por_dia.columns else por_dia.iloc[0:0]
        if not outros.empty:
            lines += [
                "",
                "## Histórico no `.jez` (outras datas — não é deste turno)",
                "",
                "O pacote pode trazer o log acumulado. Estes totais **não** entram "
                "nas métricas acima nem no `comparar-turnos`.",
                "",
                "| Data | Habs |",
                "|---|---:|",
            ]
            for day, g in outros.groupby("data", sort=True):
                lines.append(f"| {day} | {int(g['habilitacoes'].sum()):,} |")
            lines.append("")
            lines.append("Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).")
    lines += [
        "",
        f"\\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.",
        "",
        "## Nota",
        "",
        "Janela legal: 8h–17h no dia do turno. Pós-17h = fila. "
        "Comparar 1º×2º só com métricas do respectivo dia oficial.",
        "",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")
    outputs.extend([hora_csv, summary_csv, md])
    return tuple(outputs)


def print_horario_summary(summary: dict, por_hora: pd.DataFrame, uf: str, turno: int) -> None:
    console.print(
        f"\n[bold]Horário — {uf.upper()} {turno}º turno[/bold] "
        f"[dim]({summary.get('modo', '?')})[/dim]"
    )
    table = Table()
    table.add_column("Métrica")
    table.add_column("Valor", justify="right")
    table.add_row("Habilitações", f"{summary['total_habilitacoes']:,}")
    table.add_row("Seções", f"{summary['secoes']:,}")
    table.add_row(
        "% ≥17h",
        f"{summary['pct_apos_17h']}%" if summary["pct_apos_17h"] is not None else "—",
    )
    table.add_row(
        "Pico",
        f"{summary['hora_pico']}h ({summary['habilitacoes_pico']:,})"
        if summary["hora_pico"] is not None
        else "—",
    )
    if summary.get("bu_votos_presidente") is not None:
        delta = int(summary.get("delta_hab_menos_bu") or 0)
        table.add_row(
            "Votos pres. BU",
            f"{int(summary['bu_votos_presidente']):,}",
        )
        table.add_row("Log − BU", f"{delta:+,}")
        if summary.get("log_votos_computados") is not None:
            table.add_row(
                "Votos computados",
                f"{int(summary['log_votos_computados']):,}",
            )
        if summary.get("log_suspensos_sem_voto") is not None:
            table.add_row(
                "Suspensos sem voto",
                f"{int(summary['log_suspensos_sem_voto']):,}",
            )
    if "hab_biometrica" in por_hora.columns:
        total_dia = int(por_hora["habilitacoes"].sum())
        for _nome, col, _pct, rotulo in TIPO_COLUNAS:
            n = int(por_hora[col].sum())
            pct_dia = round(100 * n / total_dia, 2) if total_dia else 0.0
            table.add_row(rotulo, f"{n:,} ({pct_dia}%)")
    console.print(table)

    top = Table(title="Horas com mais fluxo")
    top.add_column("Hora")
    top.add_column("N", justify="right")
    top.add_column("%", justify="right")
    tem_tipo = "pct_biometrica" in por_hora.columns
    if tem_tipo:
        top.add_column("biom %", justify="right")
        top.add_column("manual %", justify="right")
    ranked = por_hora.sort_values("habilitacoes", ascending=False).head(8)
    for _, row in ranked.iterrows():
        if int(row["habilitacoes"]) == 0:
            continue
        cells = [f"{int(row['hora']):02d}h", f"{int(row['habilitacoes']):,}", f"{row['pct']}"]
        if tem_tipo:
            cells.extend([f"{row['pct_biometrica']}", f"{row['pct_manual']}"])
        top.add_row(*cells)
    console.print(top)


def refresh_horario_brt(uf: str, turno: int) -> list[Path] | None:
    """
    Reescreve summary/% ≥17h e after_17h a partir da curva horária local
    já existente (sem reabrir o ZIP).
    """
    uf = uf.upper()
    hora_path = REPORTS_DIR / f"curva_horaria_{uf}_{turno}t.csv"
    if not hora_path.exists():
        legacy = REPORTS_DIR / f"horario_por_hora_{uf}_{turno}t.csv"
        if legacy.exists():
            hora_path = legacy
    summary_path = REPORTS_DIR / f"horario_summary_{uf}_{turno}t.csv"
    if not hora_path.exists() or not summary_path.exists():
        return None

    por_hora = pd.read_csv(hora_path)
    if "hora" not in por_hora.columns or "habilitacoes" not in por_hora.columns:
        return None

    counts = [0] * 24
    for _, row in por_hora.iterrows():
        h = int(row["hora"])
        if 0 <= h < 24:
            counts[h] = int(row["habilitacoes"])

    old = pd.read_csv(summary_path).iloc[0].to_dict()
    summary = _summary_from_counts_local(
        counts,
        uf,
        urnas=int(old.get("urnas") or 0),
        secoes=int(old.get("secoes") or 0),
        modo=str(old.get("modo") or "curva"),
    )
    # preserva totais se o summary antigo tinha com_hora distinto
    if "total_habilitacoes" in old and pd.notna(old["total_habilitacoes"]):
        summary["total_habilitacoes"] = int(old["total_habilitacoes"])
    if "com_hora" in old and pd.notna(old["com_hora"]):
        summary["com_hora"] = int(old["com_hora"])
    for key in (
        "bu_votos_presidente",
        "bu_nominal",
        "bu_branco",
        "bu_nulo",
        "bu_outros",
        "bu_urnas",
        "bu_erros",
        "log_votos_computados",
        "log_suspensos_sem_voto",
    ):
        if key in old and pd.notna(old[key]):
            summary[key] = int(old[key])
    if summary.get("bu_votos_presidente") is not None:
        summary["delta_hab_menos_bu"] = int(summary["total_habilitacoes"]) - int(
            summary["bu_votos_presidente"]
        )

    base = por_hora.copy()
    if "uf" not in base.columns:
        base["uf"] = uf
    if "turno" not in base.columns:
        base["turno"] = turno
    if "pct" not in base.columns:
        tot = int(base["habilitacoes"].sum())
        base["pct"] = base["habilitacoes"].apply(
            lambda n: round(100 * int(n) / tot, 4) if tot else 0.0
        )
    keep = ["uf", "turno", "hora", "habilitacoes", "pct"]
    keep += [col for _n, col, pct, _r in TIPO_COLUNAS if col in base.columns and pct in base.columns]
    keep += [pct for _n, col, pct, _r in TIPO_COLUNAS if col in base.columns and pct in base.columns]
    annotated = annotate_por_hora(base[keep], uf)
    return list(write_horario_reports(annotated, summary, uf, turno))


def consolidate_horario(ufs: list[str], turno: int) -> tuple[Path, Path] | None:
    horas: list[pd.DataFrame] = []
    sums: list[pd.DataFrame] = []
    for uf in ufs:
        uf = uf.upper()
        hp = REPORTS_DIR / f"curva_horaria_{uf}_{turno}t.csv"
        if not hp.exists():
            hp = REPORTS_DIR / f"horario_por_hora_{uf}_{turno}t.csv"
        sp = REPORTS_DIR / f"horario_summary_{uf}_{turno}t.csv"
        if hp.exists():
            horas.append(pd.read_csv(hp))
        if sp.exists():
            sums.append(pd.read_csv(sp))
    if not horas:
        return None
    h_out = REPORTS_DIR / f"curva_horaria_MULTI_{turno}t.csv"
    s_out = REPORTS_DIR / f"horario_summary_MULTI_{turno}t.csv"
    pd.concat(horas, ignore_index=True).to_csv(h_out, index=False)
    if sums:
        pd.concat(sums, ignore_index=True).to_csv(s_out, index=False)
    return h_out, s_out


def run_horario_secao(
    ufs: list[str],
    turno: int,
    *,
    force: bool = False,
    workers: int | None = None,
) -> list[Path]:
    """Gera `horario_secao_{UF}_{turno}t.parquet` (pós-17h por join_key)."""
    outputs: list[Path] = []
    for i, uf in enumerate(ufs, start=1):
        uf = uf.upper()
        out = REPORTS_DIR / f"horario_secao_{uf}_{turno}t.parquet"
        if out.exists() and not force:
            console.print(f"[dim]Já existe horário seção {uf} (use --force)[/dim]")
            outputs.append(out)
            continue
        console.print(
            f"\n[bold][{i}/{len(ufs)}] Horário por seção {uf} {turno}º[/bold]"
        )
        try:
            df = compute_horario_secao(uf, turno, workers=workers)
        except FileNotFoundError as exc:
            console.print(f"[red]Pulando {uf}:[/red] {exc}")
            continue
        path = write_horario_secao(df, uf, turno)
        console.print(
            f"[green]Horário seção:[/green] {path} ({len(df):,} seções)"
        )
        outputs.append(path)
    return outputs


def run_horario(
    ufs: list[str],
    turno: int,
    *,
    detalhe: bool = False,
    force: bool = False,
    workers: int | None = None,
    por_secao: bool = False,
) -> list[Path]:
    outputs: list[Path] = []
    done: list[str] = []
    if por_secao:
        outputs.extend(run_horario_secao(ufs, turno, force=force, workers=workers))
        # ainda atualiza curva UF se pedido no mesmo comando
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("UFs", total=len(ufs))
        for uf in ufs:
            uf = uf.upper()
            progress.update(task, description=f"Horário {uf}")
            summary_path = REPORTS_DIR / f"horario_summary_{uf}_{turno}t.csv"
            hora_path = REPORTS_DIR / f"curva_horaria_{uf}_{turno}t.csv"
            legacy_hora = REPORTS_DIR / f"horario_por_hora_{uf}_{turno}t.csv"
            if (
                not force
                and summary_path.exists()
                and (hora_path.exists() or legacy_hora.exists())
            ):
                # Reanota pós-17h em BRT sem reparsear o ZIP (contagens locais intactas)
                refreshed = refresh_horario_brt(uf, turno)
                if refreshed:
                    console.print(
                        f"[dim]Já existe — reanotado BRT {uf} (use --force p/ reparse)[/dim]"
                    )
                    outputs.extend(refreshed)
                else:
                    console.print(f"[dim]Já existe — pulando {uf} (use --force)[/dim]")
                done.append(uf)
                progress.advance(task)
                continue

            console.print(
                f"\n[bold]Horário {uf} {turno}º turno[/bold] "
                f"[dim]({'detalhe' if detalhe else 'curva'})[/dim]"
            )
            try:
                if detalhe:
                    df = compute_horario(uf, turno)  # classify já recebe uf
                    por_hora = aggregate_por_hora(df)
                    summary = summarize_horario(df)
                    summary = _anexar_confronto_bu(
                        summary, uf, turno, workers=workers
                    )
                    paths = write_horario_reports(
                        por_hora, summary, uf, turno, detail=df
                    )
                else:

                    def _on_prog(
                        done_logs: int,
                        total_logs: int,
                        hab: int,
                        lote_i: int,
                        n_lotes: int,
                    ) -> None:
                        progress.update(
                            task,
                            description=(
                                f"{uf} {done_logs:,}/{total_logs:,} logs "
                                f"· lote {lote_i}/{n_lotes} · {hab:,} hab"
                            ),
                        )

                    por_hora, summary, por_dia = compute_horario_curva(
                        uf, turno, workers=workers, on_progress=_on_prog
                    )
                    summary = _anexar_confronto_bu(
                        summary, uf, turno, workers=workers
                    )
                    paths = write_horario_reports(
                        por_hora, summary, uf, turno, por_dia=por_dia
                    )
            except FileNotFoundError as exc:
                console.print(f"[red]Pulando {uf}:[/red] {exc}")
                progress.advance(task)
                continue

            print_horario_summary(summary, por_hora, uf, turno)
            outputs.extend(paths)
            console.print(f"[green]Relatório:[/green] {paths[-1]}")
            done.append(uf)
            progress.advance(task)

    # consolida todas as UFs do turno que tenham CSV (não só as desta rodada)
    all_ufs = sorted(
        {
            p.name.replace("curva_horaria_", "")
            .replace("horario_por_hora_", "")
            .replace(f"_{turno}t.csv", "")
            for p in list(REPORTS_DIR.glob(f"curva_horaria_*_{turno}t.csv"))
            + list(REPORTS_DIR.glob(f"horario_por_hora_*_{turno}t.csv"))
            if "MULTI" not in p.name and not p.name.startswith("curva_horaria_dia_")
        }
    )
    if len(all_ufs) > 1:
        cons = consolidate_horario(all_ufs, turno)
        if cons:
            console.print(f"\n[green]Curva multi-UF:[/green] {cons[0]} ({len(all_ufs)} UFs)")
            outputs.extend(cons)
    return outputs
