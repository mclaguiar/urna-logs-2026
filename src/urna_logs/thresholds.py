"""
Limiares pré-registrados da auditoria (antes de escalar ao país).

Alterar estes valores exige registro no relatório de achados (versão / data).
Não ajustar ad hoc após ver UFs grandes.
"""

from __future__ import annotations

# --- Flags do comparativo 1º×2º (percentis dentro da UF) ---
P_FLAG_ABST = 0.95
P_FLAG_MARGEM = 0.95
P_FLAG_SEM_DIG = 0.75
P_FLAG_POS17 = 0.90

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
PROTOCOLO_VERSAO = "2026.10.31-a"
PROTOCOLO_NOTA = (
    "A=inconsistência entre arquivos públicos; "
    "B=dois ou mais sinais no extremo da UF; "
    "C=sinal isolado do comparativo."
)
