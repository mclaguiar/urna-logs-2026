"""
Verificação de `-vota.vsc` (assinatura da mídia de resultado).

Sem `--nivel`, confere os dois: hashes do ZIP e assinatura de hardware.
`--nivel 1` fica só nos hashes. `--nivel 2` fica só na assinatura de hardware.
`--nivel 0` é só cobertura (parse do `.vsc`, sem hash nem assinatura).

  0 — cobertura: stem com BU/RDV/log tem `.vsc`
  1 — hashes SHA-512 dos arquivos **presentes** no ZIP = hashes do `.vsc`
      (arquivos listados na assinatura mas ausentes no pacote público =
      `ausente_pacote`, esperado: TSE não publica jufa/wsq/mr.ver etc.)
  2 — hardware, pelo par declarado em `origemAssinaturaHW`:
      UE2020/UE2022 + eddsa: Ed521 e AC UE2020/UE2022
      UE2013/UE2015 + ecdsa: ECDSA P-521; sem a AC URNA fixada a cadeia
      fica pendente e o nível permanece 1
      requer `ecpy` (opcional, `pip install -e ".[hw]"`)

Par fora da tabela, ou certificado de outro algoritmo, é falha. Não há
segunda tentativa. Não valida chave SW da cerimônia.
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

from urna_logs.config import DATA_DIR, REPORTS_DIR, ensure_dirs, zip_path

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


def _nomes_no_zip(zf: zipfile.ZipFile) -> set[str]:
    """A lista de membros é a mesma para todas as urnas deste ZIP."""
    cache: dict[tuple[int, str], set[str]] = getattr(_nomes_no_zip, "cache", {})
    chave = (id(zf), zf.filename or "")
    nomes = cache.get(chave)
    if nomes is None:
        if len(cache) > 4:
            cache.clear()
        nomes = set(zf.namelist())
        cache[chave] = nomes
        _nomes_no_zip.cache = cache  # type: ignore[attr-defined]
    return nomes


def join_key_from_stem(stem: str) -> str | None:
    m = _STEM_ONLY_RE.fullmatch(stem.lower())
    if not m:
        return None
    return (
        f"{m.group('uf').upper()}:{m.group('mun')}:"
        f"{m.group('zona')}:{m.group('secao')}"
    )


# O sistema de apuração (SA) publica boletim, log e assinatura com outro sufixo.
_ALIAS_SUFIXO = {
    "sa.vsc": "vota.vsc",
    "busa.dat": "bu.dat",
    "logsa.jez": "log.jez",
}


def _index_zip(zf: zipfile.ZipFile) -> dict[str, dict[str, str]]:
    """stem → {sufixo: member_name}. `-sa.vsc` entra como `vota.vsc`."""
    by_stem: dict[str, dict[str, str]] = defaultdict(dict)
    for name in zf.namelist():
        base = Path(name).name
        m = _FILE_RE.match(base)
        if not m:
            continue
        stem = m.group("stem").lower()
        suf = m.group("sufixo").lower()
        by_stem[stem][_ALIAS_SUFIXO.get(suf, suf)] = name
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
    hw_cadeia: str = ""  # ok | pendente | falha | "" se não tentou
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
    names_in_zip = _nomes_no_zip(zf)
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


# O boletim e o log do sistema de apuração não terminam em bu.dat / log.jez.
_CRITICO_NOMES = {
    "bu.dat": ("bu.dat", "busa.dat"),
    "rdv.dat": ("rdv.dat",),
    "log.jez": ("log.jez", "logsa.jez"),
}


def _criticos_status(detalhe: dict[str, str], stem: str) -> tuple[bool, str]:
    parts = []
    ok = True
    chaves = {Path(k).name.lower(): v for k, v in detalhe.items()}
    for suf in CRITICOS:
        st = None
        for nome in _CRITICO_NOMES[suf]:
            st = chaves.get(f"{stem}-{nome}".lower())
            if st == "ok":
                break
        if st is None:
            st = "ausente_lista"
        if st != "ok":
            ok = False
        parts.append(f"{suf}={st}")
    return ok, ";".join(parts)


def _try_hw_signatures(
    ent: dict, zf: zipfile.ZipFile, arquivos: list[dict]
) -> tuple[bool | None, str, str]:
    """Assinatura HW pelo par modelo/algoritmo declarado no `.vsc`."""
    del zf
    ausente = 'ecpy ausente; assinatura HW não executada (pip install -e ".[hw]")'
    try:
        from urna_logs.vsc_hw import verificar_hw
    except ImportError:
        return None, "", ausente
    try:
        return verificar_hw(ent, arquivos)
    except ImportError:
        return None, "", ausente


def verificar_stem(
    zf: zipfile.ZipFile,
    stem: str,
    members: dict[str, str],
    *,
    nivel: int | None = None,
) -> VscStemResult:
    """`nivel` None confere hashes e assinatura HW. 1 ou 2 fazem só aquele nível."""
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
    faz_hash = nivel is None or nivel == 1
    faz_hw = nivel is None or nivel >= 2
    if faz_hash:
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

    if faz_hw and (not faz_hash or res.nivel_ok >= 1):
        hw_ok, cadeia, hw_msg = _try_hw_signatures(ent, zf, arquivos)
        res.hw_sig_ok = hw_ok
        res.hw_cadeia = cadeia
        res.hw_sig_msg = hw_msg
        if hw_ok is True and cadeia == "ok":
            res.nivel_ok = 2
        elif hw_ok is False and not res.erro:
            res.erro = hw_msg

    return res


def run_verificar_vsc(
    ufs: list[str],
    turno: int = 1,
    *,
    nivel: int | None = None,
    limit: int | None = None,
) -> list[Path]:
    """
    Varre ZIP(s) e grava Parquet/MD/CSV de verificação `.vsc`.
    """
    ensure_dirs()
    outputs: list[Path] = []
    all_rows: list[dict] = []
    if _pede_hw(nivel):
        try:
            import ecpy.eddsa  # noqa: F401
        except ImportError:
            console.print(
                "[yellow]ecpy ausente:[/yellow] nível 2 não será executado. "
                'Instale com pip install -e ".[hw]".'
            )

    for uf in ufs:
        uf = uf.upper()
        zpath = zip_path(uf, turno)
        if not zpath.exists():
            console.print(f"[red]ZIP ausente:[/red] {zpath}")
            continue

        console.print(
            f"[cyan]Verificar .vsc[/cyan] {uf} {turno}º · "
            f"{_rotulo_nivel(nivel)} · {zpath.name}"
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
                r = verificar_stem(zf, stem, by_stem[stem], nivel=nivel)
                vsc_nome = by_stem[stem].get("vota.vsc", "")
                rows.append(
                    {
                        "uf": uf,
                        "turno": turno,
                        "stem": r.stem,
                        "midia": (
                            # Valor antigo: o arquivo é o BU de SA, urna de contingência.
                            "secao_agregada"
                            if vsc_nome.lower().endswith("-sa.vsc")
                            else "vota"
                        ),
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
                        "hw_cadeia": r.hw_cadeia,
                        "hw_sig_msg": r.hw_sig_msg,
                        "nivel_ok": r.nivel_ok,
                        "erro": r.erro,
                    }
                )

        df = pd.DataFrame(rows)
        tag = f"{uf}_{turno}t"
        pq = REPORTS_DIR / f"verificar_vsc_{tag}.parquet"
        if nivel == 2:
            df = _preservar_hashes(df, pq)
        all_rows.extend(df.to_dict(orient="records"))
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


_COLS_HASH = (
    "auto_hash_sw_ok",
    "auto_hash_hw_ok",
    "n_presentes",
    "n_hash_ok",
    "n_hash_fail",
    "n_ausente_pacote",
    "criticos_ok",
    "criticos_detalhe",
)


def _preservar_hashes(df: pd.DataFrame, anterior: Path) -> pd.DataFrame:
    """Nível 2 regrava a assinatura e mantém o hash já conferido no relatório."""
    if df.empty or not anterior.exists():
        return df
    antigo = pd.read_parquet(anterior)
    cols = [c for c in _COLS_HASH if c in antigo.columns and c in df.columns]
    if "stem" not in antigo.columns or not cols:
        return df
    base = df.drop(columns=cols).merge(antigo[["stem", *cols]], on="stem", how="left")
    hash_ok = (
        base["criticos_ok"].fillna(False).astype(bool)
        & (pd.to_numeric(base["n_hash_fail"], errors="coerce").fillna(0) == 0)
        & base["auto_hash_hw_ok"].fillna(False).astype(bool)
    )
    hw_ok = (base["hw_sig_ok"] == True) & (base["hw_cadeia"].astype(str) == "ok")
    nivel = base["nivel_ok"].fillna(0).astype(int)
    base["nivel_ok"] = nivel.where(~hash_ok, nivel.clip(lower=1)).where(~hw_ok, 2)
    return base


def _rotulo_nivel(nivel: int | None) -> str:
    if nivel is None:
        return "níveis 1+2"
    return f"nível {nivel}"


def _pede_hw(nivel: int | None) -> bool:
    return nivel is None or nivel >= 2


def _hw_contagens(df: pd.DataFrame) -> dict[str, int]:
    alg = df["alg_hw"].astype(str)
    nivel2 = df["nivel_ok"] >= 2
    cadeia = df["hw_cadeia"] if "hw_cadeia" in df.columns else None
    pendente = int((cadeia == "pendente").sum()) if cadeia is not None else 0
    return {
        "ed521": int((nivel2 & alg.eq("4")).sum()),
        "ecdsa": int((nivel2 & alg.eq("2")).sum()),
        "pendente": pendente,
        "falhou": int((df["hw_sig_ok"] == False).sum()),
    }


def _print_summary(uf: str, turno: int, df: pd.DataFrame, nivel: int | None) -> None:
    n = len(df)
    hw = _hw_contagens(df)
    table = Table(title=f"Verificar .vsc — {uf} {turno}º ({_rotulo_nivel(nivel)})")
    table.add_column("Métrica")
    table.add_column("Valor", justify="right")
    table.add_row("Stems", f"{n:,}")
    table.add_row("Com .vsc", f"{int(df['tem_vsc'].sum()):,}")
    table.add_row("Parse OK", f"{int(df['parse_ok'].sum()):,}")
    table.add_row("Nível ≥1 (hashes)", f"{int((df['nivel_ok'] >= 1).sum()):,}")
    if nivel == 2 and int(df["n_hash_ok"].fillna(0).sum()) == 0:
        table.add_row("Hashes do ZIP", "não conferidos")
    if _pede_hw(nivel):
        table.add_row("Nível 2 Ed521", f"{hw['ed521']:,}")
        table.add_row("Nível 2 ECDSA", f"{hw['ecdsa']:,}")
        table.add_row("ECDSA cadeia pendente", f"{hw['pendente']:,}")
        table.add_row("Assinatura HW falhou", f"{hw['falhou']:,}")
    table.add_row("Críticos OK", f"{int(df['criticos_ok'].fillna(False).sum()):,}")
    table.add_row("Hash fail (qualquer)", f"{int((df['n_hash_fail'] > 0).sum()):,}")
    table.add_row("Sem .vsc", f"{int((~df['tem_vsc']).sum()):,}")
    console.print(table)


def _falhas(df: pd.DataFrame) -> pd.DataFrame:
    return df[
        (df["n_hash_fail"] > 0)
        | (df["criticos_ok"] == False)
        | (~df["tem_vsc"])
        | (df["hw_sig_ok"] == False)
    ]


def pacote_das_falhas(
    uf: str, turno: int, faltam_por_stem: dict[str, list[str]]
) -> dict[str, tuple[str, str]]:
    """stem → (sufixos no ZIP, frase lida do boletim e do log).

    A frase sai do arquivo. Reprocessar com outro boletim ou outro log troca o texto.
    """
    from urna_logs.identidade_bu import complemento_pacote, identidade_boletim
    from urna_logs.parse_log import _events_from_jez_bytes

    faltam_por_stem = {str(s).lower(): list(v) for s, v in faltam_por_stem.items()}
    stems = set(faltam_por_stem)
    vazio = {s: ("", "") for s in stems}
    zpath = zip_path(uf, turno)
    if not stems or not zpath.exists():
        return vazio
    membros: dict[str, dict[str, str]] = {s: {} for s in stems}
    with zipfile.ZipFile(zpath) as zf:
        for name in zf.namelist():
            base = Path(name).name
            achado = _FILE_RE.match(base)
            if not achado:
                continue
            stem = achado.group("stem").lower()
            if stem not in membros:
                continue
            sufixo = achado.group("sufixo").lower()
            membros[stem][_ALIAS_SUFIXO.get(sufixo, sufixo)] = name
        saida: dict[str, tuple[str, str]] = {}
        for stem in stems:
            info = membros.get(stem, {})
            sufixos = ", ".join(sorted(Path(n).name.split("-", 1)[-1] for n in info.values()))
            if not sufixos:
                sufixos = "nenhum arquivo deste stem no ZIP"
            faltam = faltam_por_stem.get(stem, [])
            identidade = None
            boletim_ilegivel = False
            bu = info.get("bu.dat")
            if bu:
                try:
                    identidade = identidade_boletim(zf.read(bu))
                except Exception:
                    boletim_ilegivel = True
            mensagens = None
            log_ilegivel = False
            log = info.get("log.jez")
            if log:
                try:
                    mensagens = [
                        ev.mensagem.strip()
                        for ev in _events_from_jez_bytes(zf.read(log), log)
                    ]
                except Exception:
                    log_ilegivel = True
            frase = complemento_pacote(
                faltam,
                identidade,
                mensagens,
                boletim_ilegivel=boletim_ilegivel,
                log_ilegivel=log_ilegivel,
            )
            saida[stem] = (sufixos, frase)
    return saida


def _nome_municipio(uf: str) -> dict[str, str]:
    caminho = DATA_DIR / "ref" / "municipios_tse.csv"
    if not caminho.exists():
        return {}
    tabela = pd.read_csv(caminho, dtype=str)
    nomes: dict[str, str] = {}
    for _, row in tabela.iterrows():
        if str(row["uf"]).upper() != uf.upper():
            continue
        codigo = str(row["municipio"]).strip()
        if codigo.isdigit():
            nomes[str(int(codigo))] = str(row["nome"])
    return nomes


def _votos_por_secao(uf: str, turno: int) -> tuple[dict[str, dict], dict[str, dict]]:
    """join_key → totais do boletim e da seção (comparecimento, aptos)."""
    votos: dict[str, dict] = {}
    secoes: dict[str, dict] = {}
    votos_pq = REPORTS_DIR / f"audit_presidente_votos_{uf}_{turno}t.parquet"
    secoes_pq = REPORTS_DIR / f"audit_presidente_{uf}_{turno}t.parquet"
    if votos_pq.exists():
        frame = pd.read_parquet(votos_pq)
        for _, row in frame.iterrows():
            chave = str(row["join_key"])
            item = votos.setdefault(
                chave, {"13": 0, "22": 0, "branco": 0, "nulo": 0, "bu_rdv": True}
            )
            qtd = int(row["votos_bu"])
            tipo = str(row["tipo"])
            if tipo == "nominal" and str(row["numero"]) in ("13", "22"):
                item[str(row["numero"])] = qtd
            elif tipo in ("branco", "nulo"):
                item[tipo] = qtd
            if int(row["votos_rdv"]) != qtd:
                item["bu_rdv"] = False
    if secoes_pq.exists():
        frame = pd.read_parquet(secoes_pq, columns=["join_key", "bu_comparecimento", "aptos"])
        for _, row in frame.iterrows():
            secoes[str(row["join_key"])] = {
                "comparecimento": int(row["bu_comparecimento"]),
                "aptos": int(row["aptos"]) if pd.notna(row["aptos"]) else None,
            }
    return votos, secoes


def _texto_votacao(
    chave: str,
    votos: dict[str, dict],
    secoes: dict[str, dict],
    *,
    rdv_no_pacote: bool = True,
) -> str:
    urna = votos.get(chave)
    secao = secoes.get(chave)
    if urna is None and secao is None:
        return "Votação de presidente não está no relatório da auditoria."
    partes: list[str] = []
    if secao is not None:
        aptos = secao["aptos"]
        aptos_txt = f" de {aptos} aptos" if aptos is not None else ""
        partes.append(f"Comparecimento {secao['comparecimento']}{aptos_txt}.")
    elif secao is not None and secao["comparecimento"] == 0:
        partes.append("Boletim sem votos de presidente.")
    if urna is not None:
        partes.append(
            f"Nominal 13: {urna['13']}. Nominal 22: {urna['22']}. "
            f"Branco: {urna['branco']}. Nulo: {urna['nulo']}."
        )
        if not rdv_no_pacote:
            partes.append("O RDV não está no pacote, então os totais não foram comparados.")
        elif urna["bu_rdv"]:
            partes.append("BU e RDV com os mesmos totais.")
        else:
            partes.append("BU e RDV divergem em algum total.")
    return " ".join(partes)


def _motivo(row: pd.Series) -> str:
    from urna_logs.identidade_bu import motivo_trio

    erro = str(row.get("erro") or "")
    if erro == "sem_vota.vsc":
        return "Não há -vota.vsc nem -sa.vsc."
    detalhe = str(row.get("criticos_detalhe") or "")
    if not detalhe and "criticos:" in erro:
        detalhe = erro
    trio = motivo_trio(detalhe, float(row.get("n_hash_fail") or 0))
    if trio:
        return trio
    if row.get("hw_sig_ok") == False:
        msg = str(row.get("hw_sig_msg") or erro)
        return f"Assinatura de hardware não fechou ({msg})."
    if erro:
        return erro
    return "A verificação não fechou."


def _linhas_pendencias(uf: str, turno: int, fails: pd.DataFrame) -> list[str]:
    if fails.empty:
        return ["## Pendências", "", "Nenhuma.", ""]
    from urna_logs.identidade_bu import arquivos_em_falta

    nomes = _nome_municipio(uf)
    votos, secoes = _votos_por_secao(uf, turno)
    faltam_por = {}
    for _, row in fails.iterrows():
        detalhe = str(row.get("criticos_detalhe") or "")
        if not detalhe and "criticos:" in str(row.get("erro") or ""):
            detalhe = str(row.get("erro") or "")
        faltam_por[str(row["stem"]).lower()] = arquivos_em_falta(detalhe)
    pacote = pacote_das_falhas(uf, turno, faltam_por)
    linhas = [
        "## Urnas que a verificação não fechou",
        "",
        "Arquivo ausente no pacote não é assinatura inválida: a conta não chegou a conferir a assinatura.",
        "",
    ]
    for _, row in fails.sort_values(["join_key", "stem"]).iterrows():
        partes = str(row["join_key"]).split(":")
        if len(partes) == 4:
            codigo = str(int(partes[1])) if partes[1].isdigit() else partes[1]
            zona = str(int(partes[2])) if partes[2].isdigit() else partes[2]
            secao = str(int(partes[3])) if partes[3].isdigit() else partes[3]
            nome = nomes.get(codigo, "")
            cidade = f"{nome} ({codigo})" if nome else f"município {codigo}"
            lugar = f"{cidade}, zona {zona}, seção {secao}"
        else:
            lugar = f"chave `{row['join_key']}`"
        sufixos, complemento = pacote.get(str(row["stem"]).lower(), ("", ""))
        pacote_txt = f" No ZIP: {sufixos}." if sufixos else ""
        extra = f" {complemento}" if complemento else ""
        rdv_no_pacote = "rdv.dat" not in faltam_por.get(str(row["stem"]).lower(), [])
        linhas.append(
            f"- {lugar}. Urna `{row['stem']}`. {_motivo(row)}{extra}{pacote_txt} "
            f"{_texto_votacao(str(row['join_key']), votos, secoes, rdv_no_pacote=rdv_no_pacote)}"
        )
    linhas.append("")
    return linhas


def _linhas_agregadas(uf: str, turno: int, df: pd.DataFrame) -> list[str]:
    if "midia" not in df.columns:
        return []
    grupo = df[df["midia"] == "secao_agregada"]
    if grupo.empty:
        return []
    nomes = _nome_municipio(uf)
    votos, secoes = _votos_por_secao(uf, turno)
    fechou = int((grupo["nivel_ok"] >= 2).sum())
    linhas = [
        "## Sistema de apuração",
        "",
        "O sufixo `sa` é o boletim do sistema de apuração, não um arquivo de seção com o nome trocado. "
        "No boletim, a urna é de contingência e o bloco é o de SA: junta, turma e, quando existe, "
        "o número interno da urna de origem que não pôde ser usada.",
        "",
        f"{len(grupo)} urnas publicam `-sa.vsc`, `-busa.dat` e `-logsa.jez` "
        f"no lugar de `-vota.vsc`, `-bu.dat` e `-log.jez`. "
        f"Assinatura de hardware fechou em {fechou}.",
        "",
    ]
    for _, row in grupo.sort_values(["join_key", "stem"]).iterrows():
        partes = str(row["join_key"]).split(":")
        if len(partes) == 4:
            codigo = str(int(partes[1])) if partes[1].isdigit() else partes[1]
            zona = str(int(partes[2])) if partes[2].isdigit() else partes[2]
            secao = str(int(partes[3])) if partes[3].isdigit() else partes[3]
            nome = nomes.get(codigo, "")
            cidade = f"{nome} ({codigo})" if nome else f"município {codigo}"
            lugar = f"{cidade}, zona {zona}, seção {secao}"
        else:
            lugar = f"chave `{row['join_key']}`"
        estado = (
            "Assinatura fechou."
            if int(row["nivel_ok"]) >= 2
            else _motivo(row)
        )
        linhas.append(
            f"- {lugar}. Urna `{row['stem']}`. {estado} "
            f"{_texto_votacao(str(row['join_key']), votos, secoes)}"
        )
    linhas.append("")
    return linhas


def _markdown_uf(uf: str, turno: int, df: pd.DataFrame, nivel: int | None) -> str:
    n = len(df)
    n_vsc = int(df["tem_vsc"].sum())
    n1 = int((df["nivel_ok"] >= 1).sum())
    hw = _hw_contagens(df)
    n_fail = int((df["n_hash_fail"] > 0).sum())
    n_crit = int(df["criticos_ok"].fillna(False).sum())
    lines = [
        f"# Verificar `.vsc` — {uf} {turno}º turno",
        "",
        f"Nível solicitado: **{_rotulo_nivel(nivel)}** "
        "(omitir = hashes e assinatura HW; 1 = só hashes; 2 = só assinatura HW).",
        "",
        "## Resumo",
        "",
        f"- Stems no ZIP: **{n:,}**",
        f"- Com `-vota.vsc`: **{n_vsc:,}**",
        f"- Nível ≥1 (auto-hash + hashes dos arquivos presentes + críticos): **{n1:,}**",
        f"- Nível 2 Ed521 (UE2020/UE2022, AC UE2020 ou UE2022): **{hw['ed521']:,}**",
        f"- Nível 2 ECDSA (UE2013/UE2015, cadeia AC URNA): **{hw['ecdsa']:,}**",
        f"- ECDSA cadeia pendente (assinatura ok, AC URNA não fixada): **{hw['pendente']:,}**",
        f"- Assinatura HW falhou: **{hw['falhou']:,}**",
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
        "- Nível 2 segue o par declarado em `origemAssinaturaHW`. "
        "UE2020/UE2022 com `eddsa`: Ed521 e AC UE2020 ou UE2022. "
        "UE2013/UE2015 com `ecdsa`: ECDSA P-521; a mensagem dos arquivos é "
        "SHA-512 do hash gravado. O certificado da urna é conferido com a "
        "AC URNA publicada em http://acurna.tse.jus.br/crt/acurna.crt "
        "(válido até 2026-07-18; a conta confere a assinatura, não a data). "
        "Certificado de outro algoritmo é falha, sem segunda tentativa. "
        "Não valida a chave de software da cerimônia.",
        "",
    ]
    lines += _linhas_pendencias(uf, turno, _falhas(df))
    lines += _linhas_agregadas(uf, turno, df)
    lines += [
        "## Arquivos",
        "",
        f"- `verificar_vsc_{uf}_{turno}t.parquet`",
        f"- `verificar_vsc_{uf}_{turno}t.csv`",
        "",
    ]
    return "\n".join(lines)
