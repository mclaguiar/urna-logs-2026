"""Download incremental (HTTP Range) dos ZIPs do TSE."""

from __future__ import annotations

import json
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import httpx
from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from urna_logs.config import (
    EXTRACT_DIR,
    EXT_LOG,
    ensure_dirs,
    zip_path,
    zip_url,
)

console = Console()
CHUNK = 1024 * 1024  # 1 MiB
STATE_NAME = "download_state.json"


@dataclass
class DownloadState:
    uf: str
    turno: int
    url: str
    path: str
    total_bytes: int | None = None
    downloaded_bytes: int = 0
    status: str = "pending"  # pending | partial | complete | failed
    error: str | None = None


def _state_file() -> Path:
    ensure_dirs()
    return Path(zip_path("XX", 1).parent) / STATE_NAME


def load_states() -> dict[str, DownloadState]:
    path = _state_file()
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {k: DownloadState(**v) for k, v in raw.items()}


def save_states(states: dict[str, DownloadState]) -> None:
    path = _state_file()
    path.write_text(
        json.dumps({k: asdict(v) for k, v in states.items()}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _key(uf: str, turno: int) -> str:
    return f"{uf.upper()}_{turno}"


def head_size(url: str, client: httpx.Client) -> int | None:
    try:
        r = client.head(url, follow_redirects=True)
        if r.status_code >= 400:
            # alguns CDNs não aceitam HEAD; tenta GET parcial
            r = client.get(url, headers={"Range": "bytes=0-0"}, follow_redirects=True)
            if r.status_code in (200, 206):
                cr = r.headers.get("Content-Range")
                if cr and "/" in cr:
                    return int(cr.split("/")[-1])
                return int(r.headers.get("Content-Length", 0)) or None
            return None
        length = r.headers.get("Content-Length")
        return int(length) if length else None
    except httpx.HTTPError:
        return None


def _fmt_bytes(n: int | None) -> str:
    if n is None:
        return "?"
    if n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.2f} GB"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f} MB"
    if n >= 1_000:
        return f"{n / 1_000:.1f} KB"
    return f"{n} B"


def download_zip(
    uf: str,
    turno: int,
    *,
    force: bool = False,
    timeout: float = 120.0,
    label: str = "",
) -> Path:
    """Baixa (ou retoma) o ZIP de uma UF/turno. Idempotente."""
    ensure_dirs()
    uf = uf.upper()
    url = zip_url(uf, turno)
    dest = zip_path(uf, turno)
    part = dest.with_suffix(dest.suffix + ".part")
    states = load_states()
    key = _key(uf, turno)
    state = states.get(key) or DownloadState(uf=uf, turno=turno, url=url, path=str(dest))
    prefix = f"{label} " if label else ""

    if dest.exists() and not force:
        state.status = "complete"
        state.downloaded_bytes = dest.stat().st_size
        state.total_bytes = dest.stat().st_size
        states[key] = state
        save_states(states)
        console.print(
            f"{prefix}[green]Já completo:[/green] {dest.name} "
            f"({_fmt_bytes(dest.stat().st_size)})"
        )
        return dest

    if force and dest.exists():
        console.print(f"{prefix}[yellow]--force:[/yellow] removendo {dest.name}")
        dest.unlink()
    if force and part.exists():
        part.unlink()

    console.print(f"{prefix}[cyan]Consultando[/cyan] tamanho em {url}")
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        total = head_size(url, client)
        state.total_bytes = total
        state.url = url
        state.path = str(dest)
        console.print(f"{prefix}Tamanho remoto: [bold]{_fmt_bytes(total)}[/bold]")

        existing = part.stat().st_size if part.exists() else 0
        if existing and total and existing >= total:
            part.rename(dest)
            state.status = "complete"
            state.downloaded_bytes = total
            states[key] = state
            save_states(states)
            console.print(f"{prefix}[green].part já completo — finalizado[/green]")
            return dest

        headers: dict[str, str] = {}
        mode = "wb"
        if existing > 0:
            headers["Range"] = f"bytes={existing}-"
            mode = "ab"
            console.print(
                f"{prefix}[cyan]Retomando[/cyan] {dest.name} "
                f"em {_fmt_bytes(existing)} / {_fmt_bytes(total)}"
            )
        else:
            console.print(f"{prefix}[cyan]Baixando[/cyan] {dest.name}…")

        try:
            with client.stream("GET", url, headers=headers) as resp:
                if resp.status_code == 416:
                    # range inválido — arquivo já completo no .part
                    if part.exists():
                        part.rename(dest)
                    state.status = "complete"
                    states[key] = state
                    save_states(states)
                    return dest
                if resp.status_code == 404:
                    state.status = "missing"
                    states[key] = state
                    save_states(states)
                    raise FileNotFoundError(
                        f"ZIP ainda não publicado no TSE: {dest.name} "
                        f"(UF={uf}, turno={turno}). URL: {url}"
                    )
                if resp.status_code not in (200, 206):
                    raise httpx.HTTPStatusError(
                        f"HTTP {resp.status_code} ao baixar {url}",
                        request=resp.request,
                        response=resp,
                    )

                # se servidor ignorou Range e devolveu 200, recomeça
                if existing > 0 and resp.status_code == 200:
                    console.print("[yellow]Servidor ignorou Range; reiniciando download[/yellow]")
                    existing = 0
                    mode = "wb"
                    part.unlink(missing_ok=True)

                content_length = resp.headers.get("Content-Length")
                remaining = int(content_length) if content_length else None
                if total is None and remaining is not None:
                    total = existing + remaining
                    state.total_bytes = total

                state.status = "partial"
                states[key] = state
                save_states(states)

                progress = Progress(
                    TextColumn("[bold blue]{task.fields[name]}"),
                    BarColumn(),
                    DownloadColumn(),
                    TransferSpeedColumn(),
                    TimeRemainingColumn(),
                    console=console,
                )
                task_total = total or (existing + (remaining or 0)) or None
                with progress, part.open(mode) as out:
                    task = progress.add_task("dl", total=task_total, name=dest.name, completed=existing)
                    for chunk in resp.iter_bytes(CHUNK):
                        out.write(chunk)
                        existing += len(chunk)
                        state.downloaded_bytes = existing
                        progress.update(task, completed=existing)

            part.rename(dest)
            state.status = "complete"
            state.downloaded_bytes = dest.stat().st_size
            state.error = None
            states[key] = state
            save_states(states)
            console.print(f"[green]Download OK:[/green] {dest.name} ({dest.stat().st_size:,} bytes)")
            return dest

        except Exception as exc:  # noqa: BLE001 — captura e persiste estado
            state.status = "failed" if not part.exists() else "partial"
            state.error = str(exc)
            state.downloaded_bytes = part.stat().st_size if part.exists() else 0
            states[key] = state
            save_states(states)
            raise


def download_many(ufs: Iterable[str], turno: int, *, force: bool = False) -> list[Path]:
    uf_list = [u.upper() for u in ufs]
    n = len(uf_list)
    console.print(
        f"[bold]Download[/bold] — {turno}º turno · {n} UF(s): {', '.join(uf_list)}"
    )
    paths: list[Path] = []
    for i, uf in enumerate(uf_list, start=1):
        console.print(f"\n[bold][{i}/{n}] {uf}[/bold]")
        paths.append(download_zip(uf, turno, force=force, label=f"[{i}/{n} {uf}]"))
    console.print(f"\n[green]Concluído:[/green] {len(paths)}/{n} arquivo(s)")
    return paths


def extract_logjez(zip_file: Path, uf: str, turno: int, *, only_logs: bool = True) -> Path:
    """Extrai .logjez (e opcionalmente tudo) do ZIP para data/extract/{uf}_{turno}/."""
    ensure_dirs()
    out_dir = EXTRACT_DIR / f"{uf.upper()}_{turno}t"
    out_dir.mkdir(parents=True, exist_ok=True)
    extracted = 0
    with zipfile.ZipFile(zip_file) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name_l = info.filename.lower()
            if only_logs and not name_l.endswith(EXT_LOG) and not name_l.endswith(".zip"):
                continue
            # zips aninhados: extrai temporariamente e reabre
            target = out_dir / Path(info.filename).name
            if name_l.endswith(".zip"):
                nested_bytes = zf.read(info)
                nested_path = out_dir / Path(info.filename).name
                nested_path.write_bytes(nested_bytes)
                with zipfile.ZipFile(nested_path) as nested:
                    for ninfo in nested.infolist():
                        if ninfo.is_dir():
                            continue
                        if only_logs and not ninfo.filename.lower().endswith(EXT_LOG):
                            continue
                        dest = out_dir / Path(ninfo.filename).name
                        if not dest.exists():
                            dest.write_bytes(nested.read(ninfo))
                            extracted += 1
                nested_path.unlink(missing_ok=True)
                continue
            if only_logs and not name_l.endswith(EXT_LOG):
                continue
            if not target.exists():
                target.write_bytes(zf.read(info))
                extracted += 1
    console.print(f"[green]Extraídos {extracted} logs[/green] → {out_dir}")
    return out_dir


def list_zip_members(zip_file: Path, limit: int = 50) -> tuple[list[str], int]:
    with zipfile.ZipFile(zip_file) as zf:
        names = zf.namelist()
    return names[:limit], len(names)
