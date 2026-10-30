"""
Verificação de `-vota.vsc` (assinatura da mídia de resultado).

Níveis:
  0 — cobertura: stem com BU/RDV/log tem `.vsc`
  1 — hashes SHA-512 dos arquivos **presentes** no ZIP = hashes do `.vsc`
      (arquivos listados na assinatura mas ausentes no pacote público =
      `ausente_pacote`, esperado: TSE não publica jufa/wsq/mr.ver etc.)
  2 — assinatura de hardware (cert embutido); requer `ecpy` (opcional)

Spec: `spec/assinatura.asn1` (TSE 2026). Não valida chave SW da cerimônia.
"""

from __future__ import annotations

import hashlib
import re
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import asn1tools
import pandas as pd
from rich.console import Console
from rich.table import Table

from urna_logs.config import REPORTS_DIR, ensure_dirs, zip_path

console = Console()

_FILE_RE = re.compile(
    r"^(?P<stem>o\d{5}(?P<uf>[a-z]{2})(?P<mun>\d{5})(?P<zona>\d{4})(?P<secao>\d{4}))"
    r"-(?P<sufixo>.+)$",
    re.I,
)
_STEM_ONLY_RE = re.compile(
    r"^o\d{5}(?P<uf>[a-z]{2})(?P<mun>\d{5})(?P<zona>\d{4})(?P<secao>\d{4})$",
    re.I,
)

# Arquivos críticos do pacote público — devem existir e bater hash
CRITICOS = ("bu.dat", "rdv.dat", "log.jez")


def _spec_dir() -> Path:
    return Path(__file__).resolve().parent / "spec"


@lru_cache(maxsize=1)
def _assinatura_codec():
    return asn1tools.compile_files(
        str(_spec_dir() / "assinatura.asn1"), codec="ber", numeric_enums=True
    )


def join_key_from_stem(stem: str) -> str | None:
    m = _STEM_ONLY_RE.fullmatch(stem.lower())
    if not m:
        return None
    return (
        f"{m.group('uf').upper()}:{m.group('mun')}:"
        f"{m.group('zona')}:{m.group('secao')}"
    )


def _index_zip(zf: zipfile.ZipFile) -> dict[str, dict[str, str]]:
    """stem → {sufixo: member_name}."""
    by_stem: dict[str, dict[str, str]] = defaultdict(dict)
    for name in zf.namelist():
        base = Path(name).name
        m = _FILE_RE.match(base)
        if not m:
            continue
        stem = m.group("stem").lower()
        suf = m.group("sufixo").lower()
        by_stem[stem][suf] = name
    return by_stem


def _sha512(data: bytes) -> bytes:
    return hashlib.sha512(data).digest()


def _decode_vsc(raw: bytes) -> dict:
    return _assinatura_codec().decode("EntidadeAssinaturaEcourna", bytearray(raw))


def _arquivos_assinados(ent: dict, campo: str = "assinaturaHW") -> list[dict]:
    bloco = ent[campo]
    payload = bloco["conteudoAutoAssinado"]
    assin = _assinatura_codec().decode("Assinatura", payload)
    return list(assin["arquivosAssinados"])


def _auto_hash_ok(ent: dict, campo: str) -> bool:
    bloco = ent[campo]
    payload = bloco["conteudoAutoAssinado"]
    expected = bloco["autoAssinado"]["assinatura"]["hash"]
    return _sha512(payload) == expected


@dataclass
class VscStemResult:
    stem: str
    join_key: str | None
    tem_vsc: bool = False
    parse_ok: bool = False
    auto_hash_sw_ok: bool | None = None
    auto_hash_hw_ok: bool | None = None
    modelo_hw: str | None = None
    alg_hw: str | None = None
    n_assinados: int = 0
    n_presentes: int = 0
    n_hash_ok: int = 0
    n_hash_fail: int = 0
    n_ausente_pacote: int = 0
    criticos_ok: bool | None = None
    criticos_detalhe: str = ""
    hw_sig_ok: bool | None = None  # None = não tentado / sem ecpy
    hw_sig_msg: str = ""
    erro: str = ""
    nivel_ok: int = 0  # maior nível que passou (0/1/2)


def _verificar_hashes(
    zf: zipfile.ZipFile,
    arquivos: list[dict],
    *,
    by_name: dict[str, str] | None = None,
) -> tuple[int, int, int, int, dict[str, str]]:
    """
    Retorna (presentes, hash_ok, hash_fail, ausente, detalhe_por_nome).
    detalhe: ok | hash_fail | ausente_pacote
    """
    presentes = hash_ok = hash_fail = ausente = 0
    detalhe: dict[str, str] = {}
    names_in_zip = set(zf.namelist())
    for item in arquivos:
        nome = str(item["nomeArquivo"])
        expected = item["assinatura"]["hash"]
        member = nome if nome in names_in_zip else None
        if member is None and by_name:
            member = by_name.get(Path(nome).name.lower())
        if member is None:
            ausente += 1
            detalhe[nome] = "ausente_pacote"
            continue
        presentes += 1
        raw = zf.read(member)
        if _sha512(raw) == expected:
            hash_ok += 1
            detalhe[nome] = "ok"
        else:
            hash_fail += 1
            detalhe[nome] = "hash_fail"
    return presentes, hash_ok, hash_fail, ausente, detalhe


def _criticos_status(detalhe: dict[str, str], stem: str) -> tuple[bool, str]:
    parts = []
    ok = True
    for suf in CRITICOS:
        nome = f"{stem}-{suf}"
        # chave pode ser só o basename
        st = None
        for k, v in detalhe.items():
            if k.lower().endswith(suf) or Path(k).name.lower() == nome.lower():
                st = v
                break
        if st is None:
            st = "ausente_lista"
        if st != "ok":
            ok = False
        parts.append(f"{suf}={st}")
    return ok, ";".join(parts)


def _try_hw_signatures(
    ent: dict, zf: zipfile.ZipFile, arquivos: list[dict]
) -> tuple[bool | None, str]:
    """
    Nível 2: stub honesto — Ed521/ECPy dos scripts TSE ainda não embutido.
    Confirma presença de certificadoDigital no HW.
    """
    del zf, arquivos  # reservado para verify completo
    info = ent["assinaturaHW"]["informacaoChave"]
    origem = ent.get("origemAssinaturaHW") or {}
    modelo = origem.get("modeloEquipamento")
    alg = origem.get("algoritmoAssinatura")
    if isinstance(info, tuple) and info[0] == "certificadoDigital":
        n = len(info[1]) if info[1] is not None else 0
        return None, (
            f"certificadoDigital presente ({n} bytes) modelo={modelo} alg={alg}; "
            "verify crypto HW = scripts TSE + ECPy (nível 2 completo pendente)"
        )
    return False, f"sem certificadoDigital HW (info={info!r})"


def verificar_stem(
    zf: zipfile.ZipFile,
    stem: str,
    members: dict[str, str],
    *,
    nivel_max: int = 1,
) -> VscStemResult:
    jk = join_key_from_stem(stem)
    res = VscStemResult(stem=stem, join_key=jk)
    vsc_member = members.get("vota.vsc")
    if not vsc_member:
        res.erro = "sem_vota.vsc"
        return res
    res.tem_vsc = True
    res.nivel_ok = 0
    try:
        raw = zf.read(vsc_member)
        ent = _decode_vsc(raw)
        res.parse_ok = True
    except Exception as e:
        res.erro = f"parse: {e}"
        return res

    res.auto_hash_sw_ok = _auto_hash_ok(ent, "assinaturaSW")
    res.auto_hash_hw_ok = _auto_hash_ok(ent, "assinaturaHW")
    origem = ent.get("origemAssinaturaHW") or {}
    res.modelo_hw = str(origem.get("modeloEquipamento"))
    res.alg_hw = str(origem.get("algoritmoAssinatura"))

    arquivos = _arquivos_assinados(ent, "assinaturaHW")
    res.n_assinados = len(arquivos)
    # mapa basename → member
    by_name = {Path(v).name.lower(): v for v in members.values()}
    presentes, h_ok, h_fail, ausente, detalhe = _verificar_hashes(
        zf, arquivos, by_name=by_name
    )
    res.n_presentes = presentes
    res.n_hash_ok = h_ok
    res.n_hash_fail = h_fail
    res.n_ausente_pacote = ausente
    crit_ok, crit_det = _criticos_status(detalhe, stem)
    res.criticos_ok = crit_ok
    res.criticos_detalhe = crit_det

    if (
        res.auto_hash_hw_ok
        and res.auto_hash_sw_ok
        and h_fail == 0
        and crit_ok
    ):
        res.nivel_ok = 1
    elif h_fail == 0 and crit_ok:
        res.nivel_ok = 1 if res.auto_hash_hw_ok else 0
        if not res.auto_hash_hw_ok:
            res.erro = "auto_hash_hw_fail"
    else:
        if h_fail:
            res.erro = f"hash_fail={h_fail}"
        elif not crit_ok:
            res.erro = f"criticos:{crit_det}"

    if nivel_max >= 2 and res.nivel_ok >= 1:
        hw_ok, hw_msg = _try_hw_signatures(ent, zf, arquivos)
        res.hw_sig_ok = hw_ok
        res.hw_sig_msg = hw_msg
        if hw_ok is True:
            res.nivel_ok = 2

    return res


def run_verificar_vsc(
    ufs: list[str],
    turno: int = 1,
    *,
    nivel: int = 1,
    limit: int | None = None,
) -> list[Path]:
    """
    Varre ZIP(s) e grava Parquet/MD/CSV de verificação `.vsc`.
    """
    ensure_dirs()
    outputs: list[Path] = []
    all_rows: list[dict] = []

    for uf in ufs:
        uf = uf.upper()
        zpath = zip_path(uf, turno)
        if not zpath.exists():
            console.print(f"[red]ZIP ausente:[/red] {zpath}")
            continue

        console.print(
            f"[cyan]Verificar .vsc[/cyan] {uf} {turno}º · nível≤{nivel} · {zpath.name}"
        )
        rows: list[dict] = []
        with zipfile.ZipFile(zpath) as zf:
            by_stem = _index_zip(zf)
            stems = sorted(by_stem)
            if limit:
                stems = stems[: int(limit)]
            for i, stem in enumerate(stems, 1):
                if i == 1 or i % 500 == 0 or i == len(stems):
                    console.print(
                        f"[dim]  {uf}: {i:,}/{len(stems):,} stems[/dim]"
                    )
                r = verificar_stem(zf, stem, by_stem[stem], nivel_max=nivel)
                rows.append(
                    {
                        "uf": uf,
                        "turno": turno,
                        "stem": r.stem,
                        "join_key": r.join_key or "",
                        "tem_vsc": r.tem_vsc,
                        "parse_ok": r.parse_ok,
                        "auto_hash_sw_ok": r.auto_hash_sw_ok,
                        "auto_hash_hw_ok": r.auto_hash_hw_ok,
                        "modelo_hw": r.modelo_hw,
                        "alg_hw": r.alg_hw,
                        "n_assinados": r.n_assinados,
                        "n_presentes": r.n_presentes,
                        "n_hash_ok": r.n_hash_ok,
                        "n_hash_fail": r.n_hash_fail,
                        "n_ausente_pacote": r.n_ausente_pacote,
                        "criticos_ok": r.criticos_ok,
                        "criticos_detalhe": r.criticos_detalhe,
                        "hw_sig_ok": r.hw_sig_ok,
                        "hw_sig_msg": r.hw_sig_msg,
                        "nivel_ok": r.nivel_ok,
                        "erro": r.erro,
                    }
                )

        df = pd.DataFrame(rows)
        all_rows.extend(rows)
        tag = f"{uf}_{turno}t"
        pq = REPORTS_DIR / f"verificar_vsc_{tag}.parquet"
        csv = REPORTS_DIR / f"verificar_vsc_{tag}.csv"
        md = REPORTS_DIR / f"verificar_vsc_{tag}.md"
        df.to_parquet(pq, index=False)
        df.to_csv(csv, index=False)
        md.write_text(_markdown_uf(uf, turno, df, nivel), encoding="utf-8")
        outputs.extend([pq, csv, md])
        _print_summary(uf, turno, df, nivel)
        console.print(f"[green]Relatório:[/green] {md}")

    if len(ufs) > 1 and all_rows:
        multi = pd.DataFrame(all_rows)
        out = REPORTS_DIR / f"verificar_vsc_MULTI_{turno}t.parquet"
        multi.to_parquet(out, index=False)
        outputs.append(out)
    return outputs


def _print_summary(uf: str, turno: int, df: pd.DataFrame, nivel: int) -> None:
    n = len(df)
    table = Table(title=f"Verificar .vsc — {uf} {turno}º (nível≤{nivel})")
    table.add_column("Métrica")
    table.add_column("Valor", justify="right")
    table.add_row("Stems", f"{n:,}")
    table.add_row("Com .vsc", f"{int(df['tem_vsc'].sum()):,}")
    table.add_row("Parse OK", f"{int(df['parse_ok'].sum()):,}")
    table.add_row("Nível ≥1 (hashes)", f"{int((df['nivel_ok'] >= 1).sum()):,}")
    table.add_row("Críticos OK", f"{int(df['criticos_ok'].fillna(False).sum()):,}")
    table.add_row("Hash fail (qualquer)", f"{int((df['n_hash_fail'] > 0).sum()):,}")
    table.add_row("Sem .vsc", f"{int((~df['tem_vsc']).sum()):,}")
    console.print(table)


def _markdown_uf(uf: str, turno: int, df: pd.DataFrame, nivel: int) -> str:
    n = len(df)
    n_vsc = int(df["tem_vsc"].sum())
    n1 = int((df["nivel_ok"] >= 1).sum())
    n_fail = int((df["n_hash_fail"] > 0).sum())
    n_crit = int(df["criticos_ok"].fillna(False).sum())
    lines = [
        f"# Verificar `.vsc` — {uf} {turno}º turno",
        "",
        f"Nível solicitado: **≤{nivel}** (0=cobertura, 1=hashes, 2=HW crypto se disponível).",
        "",
        "## Resumo",
        "",
        f"- Stems no ZIP: **{n:,}**",
        f"- Com `-vota.vsc`: **{n_vsc:,}**",
        f"- Nível ≥1 (auto-hash + hashes dos arquivos presentes + críticos): **{n1:,}**",
        f"- Críticos (bu/rdv/log) OK: **{n_crit:,}**",
        f"- Algum hash presente falhou: **{n_fail:,}**",
        "",
        "Arquivos listados na assinatura mas **ausentes** no ZIP público "
        "(jufa, wsq*, mr.ver, …) contam como `ausente_pacote` — esperado no CDN.",
        "",
        "## Método",
        "",
        "- Spec ASN.1: `urna_logs/spec/assinatura.asn1` (TSE 2026)",
        "- Hash: SHA-512 do conteúdo = campo `AssinaturaDigital.hash`",
        "- Nível 2 (HW): opcional; requer ECPy/Ed521 como nos scripts oficiais",
        "",
    ]
    fails = df[(df["n_hash_fail"] > 0) | (df["criticos_ok"] == False) | (~df["tem_vsc"])]
    if not fails.empty:
        lines += ["## Falhas / pendências (até 40)", ""]
        for _, r in fails.head(40).iterrows():
            lines.append(
                f"- `{r['stem']}` jk=`{r['join_key']}` nivel_ok={r['nivel_ok']} "
                f"erro=`{r['erro']}` criticos=`{r['criticos_detalhe']}`"
            )
        lines.append("")
    else:
        lines += ["## Falhas", "", "Nenhuma no critério nível 1.", ""]
    lines += [
        "## Arquivos",
        "",
        f"- `verificar_vsc_{uf}_{turno}t.parquet`",
        f"- `verificar_vsc_{uf}_{turno}t.csv`",
        "",
    ]
    return "\n".join(lines)
