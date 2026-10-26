"""Decodificação ASN.1 de BU e RDV (schemas oficiais TSE 2026)."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

import asn1tools

CARGO_PRESIDENTE = "presidente"

# Mapeia TipoVoto do RDV para o do BU (e se a digitação entra na chave)
_RDV_TIPO_MAP: dict[str, tuple[str, bool]] = {
    "legenda": ("legenda", True),
    "nominal": ("nominal", True),
    "branco": ("branco", False),
    "nulo": ("nulo", False),
    "brancoAposSuspensao": ("branco", False),
    "nuloAposSuspensao": ("nulo", False),
    "nuloPorRepeticao": ("nulo", False),
    "nuloCargoSemCandidato": ("cargoSemCandidato", False),
    "nuloAposSuspensaoCargoSemCandidato": ("cargoSemCandidato", False),
}


def _spec_dir() -> Path:
    return Path(__file__).resolve().parent / "spec"


@lru_cache(maxsize=1)
def _bu_codec():
    return asn1tools.compile_files(str(_spec_dir() / "bu.asn1"), codec="ber")


@lru_cache(maxsize=1)
def _rdv_codec():
    return asn1tools.compile_files(str(_spec_dir() / "rdv.asn1"), codec="ber")


def _choice_value(value: Any) -> Any:
    if isinstance(value, tuple) and len(value) == 2:
        return value[1]
    return value


def _cargo_name(codigo_cargo: Any) -> str:
    return str(_choice_value(codigo_cargo))


def _normalize_legenda(digitacao: str | None) -> str | None:
    """BU agrega legenda pelo nº do partido (2 dígitos); RDV guarda a digitação crua."""
    if digitacao is None:
        return None
    s = str(digitacao)
    return s[:2] if len(s) >= 2 else s


def normalize_rdv_voto(tipo: str, digitacao: str | None) -> tuple[str, str | None]:
    mapped, keep_dig = _RDV_TIPO_MAP.get(tipo, (tipo, True))
    if not keep_dig:
        return mapped, None
    if mapped == "legenda":
        return mapped, _normalize_legenda(digitacao)
    return mapped, str(digitacao) if digitacao is not None else None


@dataclass(slots=True)
class SecaoId:
    municipio: int
    zona: int
    local: int
    secao: int

    def key(self) -> str:
        return f"{self.municipio:05d}-{self.zona:04d}-{self.local:04d}-{self.secao:04d}"


@dataclass
class TotaisPresidente:
    """Totais do cargo presidente em uma urna."""

    secao: SecaoId
    source: str
    comparecimento: int | None = None
    aptos: int | None = None
    # (tipo, numero_ou_None) -> quantidade
    votos: Counter = field(default_factory=Counter)
    # detalhamento do BU (quando disponível)
    sem_biometria: int | None = None
    bio: int | None = None
    biografia: int | None = None  # habilitação por ano de nascimento
    abertura: str | None = None
    encerramento: str | None = None

    @property
    def total(self) -> int:
        return int(sum(self.votos.values()))


def decode_bu(data: bytes) -> dict:
    codec = _bu_codec()
    envelope = codec.decode("EntidadeEnvelopeGenerico", bytearray(data))
    return codec.decode("EntidadeBoletimUrna", envelope["conteudo"])


def decode_rdv(data: bytes) -> dict:
    return _rdv_codec().decode("EntidadeResultadoRDV", bytearray(data))


def _secao_from_ident(ident: dict) -> SecaoId:
    mz = ident["municipioZona"]
    return SecaoId(
        municipio=int(mz["municipio"]),
        zona=int(mz["zona"]),
        local=int(ident["local"]),
        secao=int(ident["secao"]),
    )


def extract_presidente_from_bu(bu: dict, source: str = "") -> TotaisPresidente | None:
    ident = bu["identificacaoSecao"]
    secao = _secao_from_ident(ident)
    votos: Counter = Counter()
    comparecimento: int | None = None
    aptos: int | None = None
    found = False

    for res_el in bu.get("resultadosVotacaoPorEleicao", []):
        for rv in res_el.get("resultadosVotacao", []):
            for tot in rv.get("totaisVotosCargo", []):
                if _cargo_name(tot["codigoCargo"]) != CARGO_PRESIDENTE:
                    continue
                found = True
                comparecimento = int(rv["qtdComparecimento"])
                aptos = int(res_el["qtdEleitoresAptos"])
                for vv in tot.get("votosVotaveis", []):
                    tipo = str(vv["tipoVoto"])
                    ident_v = vv.get("identificacaoVotavel")
                    numero = str(ident_v["codigo"]) if ident_v else None
                    votos[(tipo, numero)] += int(vv["quantidadeVotos"])

    if not found:
        return None

    det = bu.get("detalhamentoComparecimento") or {}
    dados = bu.get("dadosSecaoSA")
    abertura = encerramento = None
    if isinstance(dados, tuple) and dados[0] == "dadosSecao":
        abertura = dados[1].get("dataHoraAbertura")
        encerramento = dados[1].get("dataHoraEncerramento")

    return TotaisPresidente(
        secao=secao,
        source=source,
        comparecimento=comparecimento,
        aptos=aptos,
        votos=votos,
        sem_biometria=det.get("qtdEleitoresCompareceramSemBiometria"),
        bio=det.get("qtdEleitoresHabilitadosPorBiometria"),
        biografia=det.get("qtdEleitoresHabilitadosPorBiografia"),
        abertura=abertura,
        encerramento=encerramento,
    )


def extract_presidente_from_rdv(rdv_root: dict, source: str = "") -> TotaisPresidente | None:
    body = rdv_root["rdv"]
    secao = _secao_from_ident(body["identificacao"])
    votos: Counter = Counter()
    found = False

    eleicoes = body["eleicoes"]
    ele_list = _choice_value(eleicoes)
    for el in ele_list:
        for vc in el.get("votosCargos", []):
            if _cargo_name(vc["idCargo"]) != CARGO_PRESIDENTE:
                continue
            found = True
            for voto in vc.get("votos", []):
                tipo, numero = normalize_rdv_voto(
                    str(voto["tipoVoto"]), voto.get("digitacao")
                )
                votos[(tipo, numero)] += 1

    if not found:
        return None

    return TotaisPresidente(
        secao=secao,
        source=source,
        comparecimento=int(sum(votos.values())),
        votos=votos,
    )


def parse_bu_bytes(data: bytes, source: str = "") -> TotaisPresidente | None:
    return extract_presidente_from_bu(decode_bu(data), source=source)


def parse_rdv_bytes(data: bytes, source: str = "") -> TotaisPresidente | None:
    return extract_presidente_from_rdv(decode_rdv(data), source=source)
