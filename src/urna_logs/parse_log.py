"""Parser de arquivos .logjez / .jez das urnas."""

from __future__ import annotations

import io
import re
import zipfile
from dataclasses import dataclass
from datetime import datetime, time
from pathlib import Path
from typing import Iterator

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
        if self.dt is None:
            return None
        return self.dt.time() >= time(17, 0, 0)


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


def iter_log_text_from_jez(path: Path) -> Iterator[tuple[str, str]]:
    """Yields (source_label, text) from a .jez/.logjez container or plain .log."""
    name = path.name.lower()
    if name.endswith(".log"):
        yield path.name, _decode_log_bytes(path.read_bytes())
        return

    try:
        with zipfile.ZipFile(path) as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                inner = info.filename.lower()
                if inner.endswith(".jez") and not inner.endswith(".vsc"):
                    try:
                        with zipfile.ZipFile(io.BytesIO(zf.read(info))) as nested:
                            for ninfo in nested.infolist():
                                if ninfo.filename.lower().endswith(".log"):
                                    label = f"{path.name}:{info.filename}:{ninfo.filename}"
                                    yield label, _decode_log_bytes(nested.read(ninfo))
                    except zipfile.BadZipFile:
                        data = zf.read(info)
                        if b"\t" in data[:500] or b"INFO" in data[:500]:
                            yield f"{path.name}:{info.filename}", _decode_log_bytes(data)
                elif inner.endswith(".log") or inner.endswith(".dat"):
                    data = zf.read(info)
                    sample = data[:200]
                    if b"INFO" in sample or b"ALERTA" in sample or b"\t" in sample:
                        yield f"{path.name}:{info.filename}", _decode_log_bytes(data)
    except zipfile.BadZipFile:
        text = _decode_log_bytes(path.read_bytes())
        if "INFO" in text[:500] or "\t" in text[:200]:
            yield path.name, text


def iter_events_from_file(path: Path) -> Iterator[LogEvent]:
    for source, text in iter_log_text_from_jez(path):
        for line in text.splitlines():
            ev = parse_line(line, source=source)
            if ev:
                yield ev


def iter_events_from_zip(zip_path: Path) -> Iterator[LogEvent]:
    """Percorre ZIP do TSE (layout 2026 flat ou zips aninhados) e emite eventos."""
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = info.filename.lower()
            if name.endswith(("-log.jez", ".logjez")) or (
                name.endswith(".jez") and "log" in name
            ):
                yield from _events_from_jez_bytes(zf.read(info), info.filename)
            elif name.endswith(".zip"):
                nested_raw = zf.read(info)
                try:
                    with zipfile.ZipFile(io.BytesIO(nested_raw)) as nested:
                        for ninfo in nested.infolist():
                            nname = ninfo.filename.lower()
                            if nname.endswith(("-log.jez", ".logjez")) or (
                                nname.endswith(".jez") and "log" in nname
                            ):
                                yield from _events_from_jez_bytes(
                                    nested.read(ninfo),
                                    f"{info.filename}:{ninfo.filename}",
                                )
                except zipfile.BadZipFile:
                    continue


def classify_habilitacoes(events: Iterator[LogEvent]) -> Iterator[Habilitacao]:
    """
    Agrupa contexto imediatamente anterior a 'Eleitor foi habilitado'
    para classificar o tipo de habilitação.

    Tipos (2026):
    - biometrica: "Tipo de habilitação do eleitor [biométrica]"
    - sem_biometria: eleitor sem biometria cadastral
    - manual_falha: liberação via ano de nascimento + digital do mesário
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
        after = bool(ev.dt and ev.dt.time() >= time(17, 0, 0))
        yield Habilitacao(
            id_ue=ev.id_ue,
            source=ev.source,
            dt=ev.dt,
            after_17h=after,
            tipo=tipo,
            mensagem_tipo=msg_tipo,
        )
