"""Parser de arquivos .logjez / .jez das urnas."""

from __future__ import annotations

import io
import re
import zipfile
from dataclasses import dataclass
from datetime import datetime
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
_LINE_HOUR_B = re.compile(
    rb"(\d{2}/\d{2}/\d{2,4}|\d{8})[\t ]+(\d{2}):(\d{2}):(\d{2})\t"
)


def count_habilitado_hours_from_bytes(raw: bytes) -> list[int]:
    """
    Contagem 0–23h a partir de bytes de .log (sem decode completo).
    Procura o marcador ASCII e lê a hora no início da mesma linha.
    """
    counts = [0] * 24
    start = 0
    while True:
        i = raw.find(_HAB_MARKER_B, start)
        if i < 0:
            break
        # início da linha: último \\n antes do marcador (janela curta)
        line_start = raw.rfind(b"\n", max(0, i - 220), i) + 1
        chunk = raw[line_start : i + len(_HAB_MARKER_B)]
        # evita "Mesário ... habilitou" / outros — exige o texto exato já achado
        m = _LINE_HOUR_B.match(chunk)
        if m:
            counts[int(m.group(2))] += 1
        start = i + len(_HAB_MARKER_B)
    return counts


def _habilitado_hours_from_text(text: str, source: str) -> Iterator[LogEvent]:
    """Parse só linhas candidatas a habilitação (filtro barato)."""
    for line in text.splitlines():
        if "habilitado" not in line.lower():
            continue
        ev = parse_line(line, source=source)
        if ev and HABILITADO.search(ev.mensagem):
            yield ev


def count_habilitado_hours_from_jez_bytes(raw: bytes) -> tuple[list[int], set[str]]:
    """
    Contagem por hora + ids de urna (quando disponíveis) a partir de .jez/.log.
    Caminho rápido do modo curva — sem montar LogEvent.
    """
    counts = [0] * 24
    urnas: set[str] = set()

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
                        _add(count_habilitado_hours_from_bytes(data))
                        # id_ue: 3º campo TAB na 1ª linha de habilitação (opcional)
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
            _add(count_habilitado_hours_from_bytes(blob))

    _walk(raw)
    return counts, urnas


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
      (proxy de log ≈ biografia no BU)

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
