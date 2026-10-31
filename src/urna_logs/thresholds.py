"""
Limiares pré-registrados da auditoria (antes de escalar ao país).

Alterar estes valores exige registro no relatório de achados (versão / data).
Não ajustar ad hoc após ver UFs grandes.
"""

from __future__ import annotations

# --- Flags do comparativo 1º×2º (percentis dentro da UF) ---
# 2026.10.31-b: p95/p90/p75 marcavam ~5–25% por sinal e, no pós-17h do 2º
# turno, o percentil caía em 0 e a flag pegava a seção inteira.
# C passa a ser a cauda p99. B exige dois sinais de naturezas distintas.
P_FLAG_ABST = 0.99
P_FLAG_MARGEM = 0.99
P_FLAG_SEM_DIG = 0.99
P_FLAG_POS17 = 0.99

# --- Hierarquia de evidência (confluência Nível B) ---
# Naturezas independentes. A interseção sem digital × margem não entra
# de novo: ela já é a soma de flag_sem_digital e flag_margem.
CONFLUENCIA_FLAGS = (
    "flag_margem",
    "flag_abstencao",
    "flag_pos17",
    "flag_sem_digital",
)
CONFLUENCIA_MIN = 2  # mínimo de flags distintas para Nível B por confluência

# Versão do protocolo (subir quando limiares ou regras A/B/C mudarem)
PROTOCOLO_VERSAO = "2026.10.31-b"
PROTOCOLO_NOTA = (
    "A=inconsistência entre arquivos públicos; "
    "B=dois ou mais sinais independentes no p99 da UF; "
    "C=um sinal no p99 da UF. "
    "Sinais: |Δ abstenção|, |Δ margem|, % sem digital no 1º turno, "
    "% após 17h no 1º ou no 2º. "
    "A cauda só conta se o percentil é maior que zero e a série varia."
)
