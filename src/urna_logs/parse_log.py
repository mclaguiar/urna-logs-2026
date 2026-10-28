"""Parser de arquivos .logjez / .jez das urnas."""

from __future__ import annotations

import io
import re
import zipfile
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterator

from urna_logs.fuso import apos_encerramento_oficial
from urna_logs.zip_logs import is_log_member, list_log_members

# Reexport para callers que importavam daqui
__all__ = [
    "LogEvent",
    "Habilitacao",
    "parse_line",
    "list_log_members",
    "iter_events_from_zip",
    "classify_habilitacoes",
    "count_habilitado_hours_from_bytes",
    "count_habilitado_hours_from_jez_bytes",
    "_habilitado_hours_from_text",
]

# Formato documentado pelo TSE (campos TAB):
# Data Hora Severidade ID_UE Aplicativo Mensagem MAC
# Em 2026 a data e hora vêm separadas por espaço no mesmo campo visual,
# e os demais campos por TAB: "DD/MM/YYYY HH:MM:SS\\tINFO\\t..."
LINE_RE = re.compile(
    r"^(?P<data>\d{2}/\d{2}/\d{2,4}|\d{8})"
    r"[\t ]+"
    r"(?P<hora>\d{2}:\d{2}:\d{2}|\d{6})"
    r"\t(?P<severidade>[A-Z]+)"
    r"\t(?P<id_ue>\d+)"
    r"\t(?P<aplicativo>[A-Z0-9_\-]+)"
    r"\t(?P<mensagem>.*)"
    r"\t(?P<mac>[0-9A-Fa-f]+)\s*$"
)

HAB_BIO = re.compile(r"Tipo de habilita[cç][aã]o do eleitor\s*\[biom", re.I)
HAB_MANUAL = re.compile(
    r"Tipo de habilita[cç][aã]o do eleitor\s*\[(?!biom)",
    re.I,
)
# Evitar falso positivo em "Eleitor sem atividade por N segundos"
SEM_BIO = re.compile(
    r"(O eleitor n[aã]o possui biometria|Eleitor sem dados biom[eé]tricos)",
    re.I,
)
HABILITADO = re.compile(r"Eleitor foi habilitado", re.I)
PEDIDO_MANUAL = re.compile(
    r"(Solicita[cç][aã]o de dado pessoal do eleitor para habilita[cç][aã]o manual)",
    re.I,
)
# Biografia: o log muitas vezes não grava "habilitação manual", só a conferência do ano.
ANO_IGUAL = re.compile(
    r"Ano de nascimento digitado\s+.{1,6}igual ao do cadastro",
    re.I,
)
MESARIO_HABILITOU = re.compile(r"Mes[aá]rio .+ habilitou o eleitor", re.I)
DIGITAL_MESARIO = re.compile(
    r"(Solicita digital do mes[aá]rio|Capturada a digital do mes[aá]rio)",
    re.I,
)
VOTO_CONFIRMADO = re.compile(r"(Voto confirmado|voto computado|Fim da vota)", re.I)


@dataclass(slots=True)
class LogEvent:
    data: str
    hora: str
    severidade: str
    id_ue: str
    aplicativo: str
    mensagem: str
    mac: str
    source: str
    dt: datetime | None = None

    @property
    def after_17h(self) -> bool | None:
        """≥17h no relógio **local** do log (sem conversão de fuso)."""
        if self.dt is None:
            return None
        return self.dt.hour >= 17

    def apos_17h_oficial(self, uf: str) -> bool | None:
        """≥17h no critério oficial (Brasília; ZZ = local do posto)."""
        if self.dt is None:
            return None
        return apos_encerramento_oficial(self.dt.hour, uf)


@dataclass(slots=True)
class Habilitacao:
    id_ue: str
    source: str
    dt: datetime | None
    after_17h: bool
    tipo: str  # biometrica | sem_biometria | manual_falha | desconhecido
    mensagem_tipo: str


def _parse_dt(data: str, hora: str) -> datetime | None:
    try:
        if "/" in data:
            parts = data.split("/")
            if len(parts[2]) == 2:
                data = f"{parts[0]}/{parts[1]}/20{parts[2]}"
            d = datetime.strptime(data, "%d/%m/%Y")
        else:
            d = datetime.strptime(data, "%Y%m%d")
        if ":" in hora:
            t = datetime.strptime(hora, "%H:%M:%S").time()
        else:
            t = datetime.strptime(hora, "%H%M%S").time()
        return datetime.combine(d.date(), t)
    except ValueError:
        return None


def parse_line(line: str, source: str = "") -> LogEvent | None:
    line = line.rstrip("\n\r")
    if not line or line.startswith("#"):
        return None
    m = LINE_RE.match(line)
    if not m:
        return None
    g = m.groupdict()
    dt = _parse_dt(g["data"], g["hora"])
    return LogEvent(
        data=g["data"],
        hora=g["hora"],
        severidade=g["severidade"],
        id_ue=g["id_ue"],
        aplicativo=g["aplicativo"],
        mensagem=g["mensagem"],
        mac=g["mac"],
        source=source,
        dt=dt,
    )


def _decode_log_bytes(raw: bytes) -> str:
    for enc in ("latin-1", "cp1252", "utf-8"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", errors="replace")


def _events_from_jez_bytes(raw: bytes, source: str) -> Iterator[LogEvent]:
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as jez:
            for info in jez.infolist():
                if info.is_dir():
                    continue
                name = info.filename.lower()
                if name.endswith((".log", ".dat")):
                    text = _decode_log_bytes(jez.read(info))
                    src = f"{source}:{info.filename}"
                    for line in text.splitlines():
                        ev = parse_line(line, source=src)
                        if ev:
                            yield ev
                elif name.endswith(".jez") and not name.endswith(".vsc"):
                    try:
                        yield from _events_from_jez_bytes(
                            jez.read(info), f"{source}:{info.filename}"
                        )
                    except zipfile.BadZipFile:
                        continue
    except zipfile.BadZipFile:
        text = _decode_log_bytes(raw)
        for line in text.splitlines():
            ev = parse_line(line, source=source)
            if ev:
                yield ev


# Marcador em bytes (ASCII) — evita decode+lower de cada linha no modo curva.
_HAB_MARKER_B = b"Eleitor foi habilitado"
_VOTO_COMPUTADO_B = b"O voto do eleitor foi computado"
_SUSPENSO_SEM_VOTO_B = (
    b"n\xe3o confirmou nenhum voto",
    b"nao confirmou nenhum voto",
)
_LINE_HOUR_B = re.compile(
    rb"(\d{2}/\d{2}/\d{2,4}|\d{8})[\t ]+(\d{2}):(\d{2}):(\d{2})\t"
)

# Índices de tipo na curva (mesma ordem de classify_habilitacoes).
TIPO_BIOMETRICA = 0
TIPO_MANUAL = 1
TIPO_SEM_BIOMETRIA = 2
TIPO_DESCONHECIDO = 3
TIPO_NOMES = ("biometrica", "manual_falha", "sem_biometria", "desconhecido")

# Janela imediatamente anterior à habilitação (o tipo cabe em poucas linhas).
_TIPO_LOOKBACK = 8192
_MARK_TIPO = b"Tipo de habilita"
_MARK_BIOM = b"[biom"
_MARK_SEM = (b"possui biometria", b"sem dados biom")
_MARK_MANUAL = (
    b"habilita\xe7\xe3o manual",
    b"habilitacao manual",
    b"digital do mes",
    b"habilitou o eleitor",
    b"Ano de nascimento digitado \xe9 igual",
    b"Ano de nascimento digitado e igual",
)


def tipo_habilitacao_bytes(raw: bytes, start: int, end: int) -> int:
    """
    Classifica o trecho [start, end) anterior a 'Eleitor foi habilitado'.

    A marca mais próxima de biométrica ou sem biometria ganha.
    Manual (biografia) só conta se nenhuma das duas aparecer.
    """
    if start < 0:
        start = 0
    if start >= end:
        return TIPO_DESCONHECIDO
    bio_pos = -1
    pos = start
    while pos < end:
        j = raw.find(_MARK_TIPO, pos, end)
        if j < 0:
            break
        if raw.find(_MARK_BIOM, j, min(end, j + 72)) >= 0:
            bio_pos = j
        pos = j + len(_MARK_TIPO)
    sem_pos = -1
    for needle in _MARK_SEM:
        j = raw.rfind(needle, start, end)
        if j > sem_pos:
            sem_pos = j
    if bio_pos >= 0 or sem_pos >= 0:
        return TIPO_BIOMETRICA if bio_pos >= sem_pos else TIPO_SEM_BIOMETRIA
    for needle in _MARK_MANUAL:
        if raw.find(needle, start, end) >= 0:
            return TIPO_MANUAL
    if raw.find(_MARK_TIPO, start, end) >= 0:
        return TIPO_MANUAL
    return TIPO_DESCONHECIDO


def _empty_tipo_dia() -> list[list[int]]:
    return [[0, 0, 0, 0] for _ in range(24)]


def _parse_date_b(raw: bytes) -> date | None:
    """Interpreta o grupo de data do log (dd/mm/aaaa, dd/mm/aa ou yyyymmdd)."""
    try:
        s = raw.decode("ascii")
    except UnicodeDecodeError:
        return None
    if len(s) == 8 and s.isdigit():
        return date(int(s[0:4]), int(s[4:6]), int(s[6:8]))
    parts = s.split("/")
    if len(parts) != 3:
        return None
    d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
    if y < 100:
        y += 2000
    try:
        return date(y, m, d)
    except ValueError:
        return None


def count_eventos_dia_from_bytes(
    raw: bytes, by_evento: dict[str, list[int]]
) -> None:
    """
    Acumula, por data ISO, [votos computados, suspensões sem voto confirmado].
    A suspensão é a frase «não confirmou nenhum voto».
    """
    markers = ((_VOTO_COMPUTADO_B, 0),) + tuple(
        (m, 1) for m in _SUSPENSO_SEM_VOTO_B
    )
    for marker, idx in markers:
        start = 0
        while True:
            i = raw.find(marker, start)
            if i < 0:
                break
            ls = raw.rfind(b"\n", max(0, i - 240), i) + 1
            m = _LINE_HOUR_B.match(raw[ls : i + len(marker)])
            if m:
                d = _parse_date_b(m.group(1))
                if d is not None:
                    key = d.isoformat()
                    bucket = by_evento.get(key)
                    if bucket is None:
                        bucket = [0, 0]
                        by_evento[key] = bucket
                    bucket[idx] += 1
            start = i + len(marker)


def count_habilitado_hours_from_bytes(
    raw: bytes,
    *,
    data_filtro: date | None = None,
    by_day: dict[str, list[int]] | None = None,
    by_tipo: dict[str, list[list[int]]] | None = None,
) -> list[int]:
    """
    Contagem 0–23h a partir de bytes de .log (sem decode completo).
    Conta todos os dias em `counts`, salvo se `data_filtro` restringir.
    Se `by_day` for passado, sempre acumula ISO date → [24] (todos os dias).
    Se `by_tipo` for passado, ISO date → 24 horas × 4 tipos
    (biometrica, manual, sem_biometria, desconhecido), também todos os dias.
    """
    counts = [0] * 24
    start = 0
    prev_end = 0
    while True:
        i = raw.find(_HAB_MARKER_B, start)
        if i < 0:
            break
        line_start = raw.rfind(b"\n", max(0, i - 220), i) + 1
        chunk = raw[line_start : i + len(_HAB_MARKER_B)]
        m = _LINE_HOUR_B.match(chunk)
        if m:
            hour = int(m.group(2))
            d = _parse_date_b(m.group(1))
            if by_day is not None and d is not None:
                key = d.isoformat()
                bucket = by_day.get(key)
                if bucket is None:
                    bucket = [0] * 24
                    by_day[key] = bucket
                bucket[hour] += 1
            if by_tipo is not None and d is not None and 0 <= hour < 24:
                key = d.isoformat()
                tipos = by_tipo.get(key)
                if tipos is None:
                    tipos = _empty_tipo_dia()
                    by_tipo[key] = tipos
                look = max(prev_end, line_start - _TIPO_LOOKBACK)
                tipos[hour][tipo_habilitacao_bytes(raw, look, line_start)] += 1
            if data_filtro is None or d == data_filtro:
                counts[hour] += 1
        prev_end = i + len(_HAB_MARKER_B)
        start = prev_end
    return counts


def _habilitado_hours_from_text(text: str, source: str) -> Iterator[LogEvent]:
    """Parse só linhas candidatas a habilitação (filtro barato)."""
    for line in text.splitlines():
        if "habilitado" not in line.lower():
            continue
        ev = parse_line(line, source=source)
        if ev and HABILITADO.search(ev.mensagem):
            yield ev


def count_habilitado_hours_from_jez_bytes(
    raw: bytes,
    *,
    data_filtro: date | None = None,
    by_tipo: dict[str, list[list[int]]] | None = None,
    by_evento: dict[str, list[int]] | None = None,
) -> tuple[list[int], set[str], dict[str, list[int]]]:
    """
    Contagem por hora + ids de urna + breakdown dia×hora a partir de .jez/.log.
    `counts` respeita `data_filtro` (dia oficial do turno); `by_day` traz todos os dias.
    `by_tipo`, se passado, acumula dia → 24h × tipo de habilitação.
    `by_evento`, se passado, acumula dia → [votos computados, suspensões sem voto].
    """
    counts = [0] * 24
    urnas: set[str] = set()
    by_day: dict[str, list[int]] = {}

    def _add(part: list[int]) -> None:
        for h, c in enumerate(part):
            counts[h] += c

    def _walk(blob: bytes) -> None:
        try:
            with zipfile.ZipFile(io.BytesIO(blob)) as jez:
                for info in jez.infolist():
                    if info.is_dir():
                        continue
                    name = info.filename.lower()
                    data = jez.read(info)
                    if name.endswith((".log", ".dat")):
                        _add(
                            count_habilitado_hours_from_bytes(
                                data,
                                data_filtro=data_filtro,
                                by_day=by_day,
                                by_tipo=by_tipo,
                            )
                        )
                        if by_evento is not None:
                            count_eventos_dia_from_bytes(data, by_evento)
                        j = data.find(_HAB_MARKER_B)
                        if j >= 0:
                            ls = data.rfind(b"\n", max(0, j - 220), j) + 1
                            fields = data[ls:j].split(b"\t")
                            if len(fields) >= 3 and fields[2].isdigit():
                                urnas.add(fields[2].decode("ascii", errors="ignore"))
                    elif name.endswith(".jez") and not name.endswith(".vsc"):
                        try:
                            _walk(data)
                        except zipfile.BadZipFile:
                            continue
        except zipfile.BadZipFile:
            _add(
                count_habilitado_hours_from_bytes(
                    blob,
                    data_filtro=data_filtro,
                    by_day=by_day,
                    by_tipo=by_tipo,
                )
            )
            if by_evento is not None:
                count_eventos_dia_from_bytes(blob, by_evento)

    _walk(raw)
    return counts, urnas, by_day


def iter_events_from_zip(zip_path: Path) -> Iterator[LogEvent]:
    """Percorre ZIP do TSE (layout 2026 flat ou zips aninhados) e emite eventos."""
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = info.filename
            if is_log_member(name):
                yield from _events_from_jez_bytes(zf.read(info), name)
            elif name.lower().endswith(".zip"):
                nested_raw = zf.read(info)
                try:
                    with zipfile.ZipFile(io.BytesIO(nested_raw)) as nested:
                        for ninfo in nested.infolist():
                            if is_log_member(ninfo.filename):
                                yield from _events_from_jez_bytes(
                                    nested.read(ninfo),
                                    f"{name}:{ninfo.filename}",
                                )
                except zipfile.BadZipFile:
                    continue


def classify_habilitacoes(
    events: Iterator[LogEvent], *, uf: str = "SP"
) -> Iterator[Habilitacao]:
    """
    Agrupa contexto imediatamente anterior a 'Eleitor foi habilitado'
    para classificar o tipo de habilitação.

    Tipos (2026):
    - biometrica: "Tipo de habilitação do eleitor [biométrica]"
    - sem_biometria: eleitor sem biometria cadastral
    - manual_falha: liberação via ano de nascimento + digital do mesário
      (proxy de log ≈ biografia no BU). Inclui
      "Ano de nascimento digitado é igual ao do cadastro".

    `after_17h` usa critério oficial (Brasília; ZZ = local) via `uf`.
    Default `uf=SP` (= BRT) preserva testes sem fuso.
    """
    window: list[LogEvent] = []
    for ev in events:
        window.append(ev)
        if len(window) > 50:
            window.pop(0)
        if not HABILITADO.search(ev.mensagem):
            continue
        tipo = "desconhecido"
        msg_tipo = ""
        for prev in reversed(window[:-1]):
            if prev.id_ue != ev.id_ue:
                continue
            if HABILITADO.search(prev.mensagem):
                break
            if HAB_BIO.search(prev.mensagem):
                tipo = "biometrica"
                msg_tipo = prev.mensagem
                break
            if SEM_BIO.search(prev.mensagem):
                tipo = "sem_biometria"
                msg_tipo = prev.mensagem
                break
            if (
                PEDIDO_MANUAL.search(prev.mensagem)
                or HAB_MANUAL.search(prev.mensagem)
                or MESARIO_HABILITOU.search(prev.mensagem)
                or DIGITAL_MESARIO.search(prev.mensagem)
                or ANO_IGUAL.search(prev.mensagem)
            ):
                tipo = "manual_falha"
                msg_tipo = prev.mensagem
                continue
        hora = ev.dt.hour if ev.dt is not None else None
        yield Habilitacao(
            id_ue=ev.id_ue,
            source=ev.source,
            dt=ev.dt,
            after_17h=apos_encerramento_oficial(hora, uf),
            tipo=tipo,
            mensagem_tipo=msg_tipo,
        )
