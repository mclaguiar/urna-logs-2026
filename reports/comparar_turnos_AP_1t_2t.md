# Comparativo 1º × 2º turno — AP

Status: **esqueleto (aguardando 2º)**

2º turno ainda não disponível (sem `audit_presidente_AP_2t.parquet`). Esqueleto gravado; rode de novo quando o CDN publicar.

## Disponibilidade

- 1º turno (audit): sim · 1,914 seções
- 2º turno (audit): não · 0 seções

## Métricas (quando ambos existirem)

- Seções em ambos: **0**
- Só no 1º: **1,914** · só no 2º: **0**

## Pós-17h (quando `horario` existir nos dois turnos)

- % ≥17h no 1º: **5.3647**
- % ≥17h no 2º: **None**
- Δ (2º − 1º): **None**

## Limites

- Comparação é **agregada por seção** (`join_key`).
- Não dá para saber *quem* mudou de candidato entre turnos (sigilo do voto).
- “Migração” = mudança dos totais da seção (finalistas, eliminados, abstenção).

## Próximos campos (quando 2º existir)

- Votos dos finalistas 1º→2º e margem
- Saldo aparente dos votos de quem ficou fora no 1º
- Brancos/nulos 1º→2º
- Cruzar seções com alto % pós-17h × Δ de resultado
