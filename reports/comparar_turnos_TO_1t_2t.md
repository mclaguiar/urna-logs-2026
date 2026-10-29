# Comparativo 1º × 2º turno — TO

Status: **pronto**

Comparativo 1º×2º preenchido (finalistas 13×22; saldo agregado por seção — não é migração eleitor a eleitor).

## Disponibilidade

- 1º turno (audit): sim · 4,384 seções
- 2º turno (audit): sim · 4,384 seções
- Finalistas (nominais no 2º): **13** e **22**
- Margem = votos(13) − votos(22)

## Métricas

- Seções em ambos: **4,384**
- Só no 1º: **0** · só no 2º: **0**
- Δ comparecimento (soma seções ambos): **-10433**
- Δ abstenção (pp, aptos ambos): **0.8839**
- % sem digital 1º→2º: **8.1229** → **7.7281** (Δ **-0.3948**)

## Pós-17h (UF)

- % ≥17h no 1º: **1.5536**
- % ≥17h no 2º: **0.019**
- Δ (2º − 1º): **-1.5346**

## Flags de anomalia (percentis na UF)

- `|Δ abstenção|` ≥ p95: **224**
- `|Δ margem|` ≥ p95: **234**
- alto % sem digital 1º × `|Δ margem|`: **61**
- cauda pós-17h atípica: **4384**
- só em um turno: **0**

## Seções que mais movem a margem (13−22)

| join_key | Δ margem | Δ abst | % sem dig 1º | %≥17h 2º | flags |
|---|---:|---:|---:|---:|---|
| `TO:73440:0029:0706` | 42 | -8 | 3.5587 | 0.0 | margem|pos17 |
| `TO:92410:0034:0133` | 41 | 6 | 21.5094 | 0.0 | margem|sem_digital_x_margem|pos17 |
| `TO:92410:0001:0252` | 41 | -8 | 10.9375 | 0.0 | margem|sem_digital_x_margem|pos17 |
| `TO:73091:0032:0038` | 40 | 8 | 12.4224 | 0.0 | margem|sem_digital_x_margem|pos17 |
| `TO:96156:0017:0075` | 40 | 11 | 3.5088 | 0.0 | margem|pos17 |
| `TO:73440:0029:0420` | 40 | 8 | 7.6389 | 0.0 | margem|pos17 |
| `TO:95591:0003:0163` | 39 | -2 | 8.1181 | 0.0 | margem|pos17 |
| `TO:96857:0021:0014` | 39 | 1 | 4.9327 | 0.0 | margem|pos17 |
| `TO:73440:0029:0701` | 39 | 10 | 3.3835 | 0.0 | margem|pos17 |
| `TO:92410:0001:0375` | 38 | -2 | 6.8966 | 0.0 | margem|pos17 |
| `TO:73385:0013:0110` | 37 | 5 | 6.6372 | 0.0 | margem|pos17 |
| `TO:95591:0003:0040` | 37 | -2 | 8.0321 | 0.0 | margem|pos17 |
| `TO:93858:0002:0260` | 37 | 2 | 27.1967 | 0.0 | margem|sem_digital_x_margem|pos17 |
| `TO:95257:0023:0094` | 36 | 8 | 6.7227 | 0.0 | margem|pos17 |
| `TO:73440:0029:0651` | 36 | 7 | 9.3525 | 0.0 | margem|pos17 |

## Seções com flag

4,384 seção(ões) (até 30):

- `TO:73008:0007:0135` · pos17 · Δmargem=-3 · Δabst=1
- `TO:73008:0007:0136` · pos17 · Δmargem=9 · Δabst=1
- `TO:73008:0007:0137` · pos17 · Δmargem=10 · Δabst=9
- `TO:73008:0007:0138` · margem|sem_digital_x_margem|pos17 · Δmargem=27 · Δabst=2
- `TO:73008:0007:0139` · pos17 · Δmargem=5 · Δabst=7
- `TO:73008:0007:0166` · pos17 · Δmargem=3 · Δabst=11
- `TO:73008:0007:0176` · pos17 · Δmargem=19 · Δabst=1
- `TO:73008:0007:0211` · pos17 · Δmargem=13 · Δabst=9
- `TO:73008:0007:0228` · margem|pos17 · Δmargem=26 · Δabst=12
- `TO:73008:0007:0243` · margem|pos17 · Δmargem=27 · Δabst=6
- `TO:73016:0027:0058` · pos17 · Δmargem=16 · Δabst=3
- `TO:73016:0027:0059` · pos17 · Δmargem=4 · Δabst=12
- `TO:73016:0027:0060` · pos17 · Δmargem=-2 · Δabst=5
- `TO:73016:0027:0061` · pos17 · Δmargem=18 · Δabst=6
- `TO:73016:0027:0062` · abstencao|pos17 · Δmargem=14 · Δabst=14
- `TO:73016:0027:0063` · pos17 · Δmargem=1 · Δabst=6
- `TO:73016:0027:0064` · pos17 · Δmargem=19 · Δabst=6
- `TO:73016:0027:0066` · pos17 · Δmargem=2 · Δabst=7
- `TO:73016:0027:0076` · pos17 · Δmargem=0 · Δabst=7
- `TO:73016:0027:0077` · pos17 · Δmargem=-5 · Δabst=-3
- `TO:73016:0027:0078` · pos17 · Δmargem=11 · Δabst=3
- `TO:73016:0027:0080` · pos17 · Δmargem=10 · Δabst=7
- `TO:73024:0027:0098` · pos17 · Δmargem=6 · Δabst=5
- `TO:73024:0027:0099` · abstencao|pos17 · Δmargem=6 · Δabst=14
- `TO:73024:0027:0100` · pos17 · Δmargem=-10 · Δabst=4
- `TO:73024:0027:0101` · pos17 · Δmargem=-5 · Δabst=9
- `TO:73024:0027:0102` · pos17 · Δmargem=6 · Δabst=0
- `TO:73024:0027:0103` · pos17 · Δmargem=-1 · Δabst=0
- `TO:73024:0027:0104` · pos17 · Δmargem=6 · Δabst=4
- `TO:73024:0027:0105` · pos17 · Δmargem=10 · Δabst=13
- … e mais 4354

## Hipóteses → observáveis (agregado; não conclusões)

| Hipótese | Observável |
|---|---|
| Transferência aparente dos eliminados | `votos_eliminados_1t` ≈ `ganho_finalistas` − `delta_comparecimento` (residual em `gap_transferencia`) |
| Abstenção seletiva | `|delta_abstencao|` alto com pouco Δ nos finalistas |
| Risco operacional | alto `% sem digital` × `|delta_margem|` |
| Cauda horária | alto `% ≥17h` × Δ comparecimento/margem |
| Contingência / troca de urna | status `so_1t` / `so_2t` |

## Limites

- Comparação é **agregada por seção** (`join_key`).
- Não dá para saber *quem* mudou de candidato entre turnos (sigilo do voto).
- “Migração” = mudança dos totais da seção (finalistas, eliminados, abstenção).
- RDV≡BU e BU≡CSV oficial comparam a **integridade entre arquivos públicos** disponibilizados.
