"""
Limiares pré-registrados da auditoria (antes de escalar ao país).

Alterar estes valores exige nova rodada de `validar-fluxo` no piloto e
registro no relatório de achados (versão / data). Não ajustar ad hoc
após ver UFs grandes.
"""

from __future__ import annotations

# --- Flags do comparativo 1º×2º (percentis dentro da UF) ---
P_FLAG_ABST = 0.95
P_FLAG_MARGEM = 0.95
P_FLAG_SEM_DIG = 0.75
P_FLAG_POS17 = 0.90

# --- Duncan–Davis / fluxo ---
NARROW_WIDTH = 0.25  # (hi-lo)/origem ≤ isto → célula “estreita”
ELIM_FORCED_SHARE = 0.50  # limite inf. > 50% da origem Elim

# --- Validação do algoritmo ---
TOL_MARGEM_IPF = 2.0
TOL_BOUNDS = 2.0
TOL_RATE_SUM = 0.02
TOL_RESID_REL = 0.35
MIN_SECOES_VALIDAR = 50
IDENTIDADE_MIN_PCT = 0.995

# --- Hierarquia de evidência (confluência Nível B) ---
# Contam para confluência operacional: estas flags do comparativo
CONFLUENCIA_FLAGS = (
    "flag_margem",
    "flag_abstencao",
    "flag_pos17",
    "flag_sem_digital_x_margem",
)
CONFLUENCIA_MIN = 2  # mínimo de flags distintas para Nível B por confluência

# Versão do protocolo (subir quando limiares ou regras A/B/C mudarem)
PROTOCOLO_VERSAO = "2026.10.28-a"
PROTOCOLO_NOTA = (
    "A=inconsistência entre arquivos públicos; "
    "B=dois ou mais sinais no extremo da UF; "
    "C=sinal isolado ou saldo agregado da seção."
)
