"""O que o boletim declara sobre a urna, lido do próprio arquivo.

Os nomes saem dos enumerados de bu.asn1. Uma urna muda de frase quando o
boletim ou o log mudam; o município não entra na conta.
"""

from __future__ import annotations

from urna_logs.anomalias.catalogo import FRASES
from urna_logs.bu_rdv import decode_bu

_CRITICOS = ("bu.dat", "rdv.dat", "log.jez")

_URNA = {
    "secao": "urna de seção",
    "contingencia": "urna de contingência",
    "contingenciaSecao": "urna de contingência que passou a ser de seção",
    "contingenciaEncerrandoSecao": "urna de contingência encerrando a seção",
}
_ARQUIVO = {
    "votacaoUE": "votação da urna",
    "votacaoRED": "recuperação de dados",
    "saMistaMRParcialCedula": "sistema de apuração mista com memória de resultado",
    "saMistaBUImpressoCedula": "sistema de apuração mista com boletim impresso",
    "saManual": "sistema de apuração manual",
    "saEletronica": "sistema de apuração eletrônica",
}
_BLOCO = {
    "dadosSecao": "bloco de seção",
    "dadosSA": "bloco do sistema de apuração",
}
_FASE = {
    "oficial": "oficial",
    "simulado": "simulado",
    "treinamento": "treinamento",
}
_ESCOLHA_SA = {
    "apuracaoEletronica": "apuração eletrônica",
    "apuracaoMistaBUAE": "apuração mista com boletim",
    "apuracaoMistaMR": "apuração mista com memória de resultado",
    "apuracaoTotalmenteManual": "apuração manual",
}
_TIPO_APURACAO = {
    "totalmenteManual": "totalmente manual",
    "totalmenteEletronica": "totalmente eletrônica",
    "mistaBU": "mista com boletim",
    "mistaMR": "mista com memória de resultado",
}
_MOTIVO = {
    "naoFoiPossivelReuperarResultado": "não foi possível recuperar o resultado",
    "urnaNaoChegouMidiaDefeituosa": "urna não chegou, mídia defeituosa",
    "urnaNaoChegouMidiaExtraviada": "urna não chegou, mídia extraviada",
    "urnaComDefeito": "urna com defeito",
    "urnaIndisponivelInicio": "urna indisponível no início",
    "urnaOutraSecao": "urna de outra seção",
    "urnaOutrasecao": "urna de outra seção",
    "urnaDataHoraIncorreta": "data ou hora incorreta",
    "urnaPreparadaIncorretamente": "urna preparada incorretamente",
    "urnaEncerradaComEleitoresNaFila": "urna encerrada com eleitores na fila",
    "naoObteveExitoContingencia": "contingência sem êxito",
    "indisponibilidadeUrnaContingencia": "urna de contingência indisponível",
    "indisponibilidadeFlashContingencia": "mídia de contingência indisponível",
    "problemaEnergiaEletrica": "problema de energia elétrica",
    "naoFoiPossivelTrocarUrna": "não foi possível trocar a urna",
    "naoFoiSolicitadaTrocaUrna": "troca de urna não solicitada",
    "outros": "outros",
}
_FRASES_CONTINGENCIA = {FRASES["contingencia_inicio"], FRASES["contingencia_modo"]}


def _rotulo(tabela: dict[str, str], valor: str, vazio: str) -> str:
    if not valor:
        return vazio
    return tabela.get(valor, valor)


def _texto_motivo(valor) -> str | None:
    if valor is None:
        return None
    if isinstance(valor, tuple) and len(valor) == 2 and isinstance(valor[1], dict):
        escolha, corpo = valor
        tipo = corpo.get("tipoapuracao", corpo.get("tipoApuracao"))
        motivo = corpo.get("motivoApuracao")
        partes = [
            _rotulo(_ESCOLHA_SA, str(escolha or ""), ""),
            _rotulo(_TIPO_APURACAO, str(tipo or ""), ""),
            _rotulo(_MOTIVO, str(motivo or ""), ""),
        ]
        texto = ", ".join(p for p in partes if p)
        return texto or None
    return str(valor)


def identidade_boletim(data: bytes) -> dict:
    """tipo_urna, tipo_arquivo, bloco, fase e motivo de SA, como o boletim traz."""
    bu = decode_bu(data)
    urna = bu["urna"]
    dados = bu.get("dadosSecaoSA")
    bloco = dados[0] if isinstance(dados, tuple) and dados else ""
    return {
        "tipo_urna": str(urna.get("tipoUrna") or ""),
        "tipo_arquivo": str(urna.get("tipoArquivo") or ""),
        "bloco": str(bloco),
        "fase": str(bu.get("fase") or ""),
        "motivo": _texto_motivo(urna.get("motivoUtilizacaoSA")),
    }


def texto_identidade(info: dict) -> str:
    urna = _rotulo(_URNA, info.get("tipo_urna") or "", "tipo de urna não informado")
    arquivo = _rotulo(_ARQUIVO, info.get("tipo_arquivo") or "", "tipo de arquivo não informado")
    bloco = _rotulo(_BLOCO, info.get("bloco") or "", "bloco não informado")
    fase = info.get("fase") or ""
    fase_txt = f", fase {_rotulo(_FASE, fase, fase)}" if fase else ""
    frase = f"O boletim declara {urna}, arquivo de {arquivo} e {bloco}{fase_txt}."
    if info.get("motivo"):
        frase += f" Motivo de uso do sistema de apuração no boletim: {info['motivo']}."
    return frase


def arquivos_em_falta(detalhe: str) -> list[str]:
    texto = str(detalhe or "")
    if "criticos:" in texto:
        texto = texto.split("criticos:", 1)[1]
    faltam = []
    for parte in texto.split(";"):
        if "=" not in parte:
            continue
        nome, estado = parte.split("=", 1)
        nome = nome.strip()
        if nome in _CRITICOS and estado.strip() != "ok":
            faltam.append(nome)
    return faltam


def motivo_trio(detalhe: str, n_fail: float) -> str:
    """O trio bu, rdv e log não fechou. Arquivo ausente não é hash divergente."""
    if n_fail > 0:
        return "O SHA-512 de um arquivo presente não é o hash gravado no .vsc."
    faltam = arquivos_em_falta(detalhe)
    if faltam:
        lista = ", ".join(faltam)
        return (
            f"Falta {lista} no pacote. O hash dos arquivos presentes fechou. "
            "A assinatura de hardware não foi conferida."
        )
    if detalhe:
        return "O trio bu, rdv e log não fechou contra o .vsc."
    return ""


def _texto_contingencia(mensagens: list[str]) -> str:
    n = sum(1 for msg in mensagens if msg in _FRASES_CONTINGENCIA)
    if n == 1:
        return (
            "O log contém 1 frase de procedimento de contingência "
            "ou de carga de urna de contingência."
        )
    if n > 1:
        return (
            f"O log contém {n} frases de procedimento de contingência "
            "ou de carga de urna de contingência."
        )
    return (
        "O log não contém as frases de procedimento de contingência "
        "nem de carga de urna de contingência."
    )


def _texto_geracao(nome: str, mensagens: list[str]) -> str:
    citadas = [msg for msg in mensagens if nome.lower() in msg.lower()]
    if not citadas:
        return f"O log presente não menciona {nome}."
    gerando = any("gerando" in msg.lower() for msg in citadas)
    termino = any("término" in msg.lower() or "termino" in msg.lower() for msg in citadas)
    inicio = any("início" in msg.lower() or "inicio" in msg.lower() for msg in citadas)
    if gerando and termino:
        return (
            f"O log registra a geração de {nome} até o término. "
            "Esse arquivo não está no pacote publicado."
        )
    if gerando and inicio:
        return f"O log registra o início da geração de {nome} e não o término."
    return f"O log menciona {nome}."


def complemento_pacote(
    faltam: list[str],
    identidade: dict | None,
    mensagens: list[str] | None,
    *,
    boletim_ilegivel: bool = False,
    log_ilegivel: bool = False,
) -> str:
    """Frase lida do boletim e, quando existe, do log. Independente do município."""
    partes: list[str] = []
    if boletim_ilegivel:
        partes.append("O boletim presente não pôde ser lido.")
    elif identidade:
        partes.append(texto_identidade(identidade))
    if log_ilegivel:
        partes.append("O log presente não pôde ser lido.")
    elif mensagens is not None:
        partes.append(_texto_contingencia(mensagens))
        for nome in faltam:
            if nome == "log.jez":
                continue
            partes.append(_texto_geracao(nome, mensagens))
    return " ".join(partes)
