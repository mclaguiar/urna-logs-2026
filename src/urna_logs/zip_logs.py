"""Leitura de membros de log (.logjez/.jez) dentro dos ZIPs do TSE."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path


def is_log_member(name: str) -> bool:
    n = name.lower()
    return n.endswith(("-log.jez", ".logjez")) or (n.endswith(".jez") and "log" in n)


def list_log_members(zip_path: Path) -> list[str]:
    """Membros de log no ZIP TSE (flat ou `outer:inner`)."""
    members: list[str] = []
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = info.filename
            if is_log_member(name):
                members.append(name)
            elif name.lower().endswith(".zip"):
                try:
                    with zipfile.ZipFile(io.BytesIO(zf.read(info))) as nested:
                        for ninfo in nested.infolist():
                            if is_log_member(ninfo.filename):
                                members.append(f"{name}:{ninfo.filename}")
                except zipfile.BadZipFile:
                    continue
    return members


def read_member_from_open_zip(zf: zipfile.ZipFile, member: str) -> bytes:
    """Lê membro; suporte a `outer.zip:inner` com ZIP já aberto."""
    if ":" in member:
        outer, _, inner = member.partition(":")
        with zipfile.ZipFile(io.BytesIO(zf.read(outer))) as nested:
            return nested.read(inner)
    return zf.read(member)
