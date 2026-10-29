# Comparativo 1º × 2º turno — AC

Status: **pronto**

Comparativo 1º×2º preenchido (finalistas 13×22; saldo agregado por seção — não é migração eleitor a eleitor).

## Disponibilidade

- 1º turno (audit): sim · 2,270 seções
- 2º turno (audit): sim · 2,270 seções
- Finalistas (nominais no 2º): **13** e **22**
- Margem = votos(13) − votos(22)

## Métricas

- Seções em ambos: **2,270**
- Só no 1º: **0** · só no 2º: **0**
- Δ comparecimento (soma seções ambos): **-34676**
- Δ abstenção (pp, aptos ambos): **5.6467**
- % sem digital 1º→2º: **8.6513** → **8.3718** (Δ **-0.2795**)

## Pós-17h (UF)

- % ≥17h no 1º: **1.6302**
- % ≥17h no 2º: **0.028**
- Δ (2º − 1º): **-1.6022**

## Flags de anomalia (percentis na UF)

- `|Δ abstenção|` ≥ p95: **119**
- `|Δ margem|` ≥ p95: **127**
- alto % sem digital 1º × `|Δ margem|`: **58**
- cauda pós-17h atípica: **2270**
- só em um turno: **0**

## Seções que mais movem a margem (13−22)

| join_key | Δ margem | Δ abst | % sem dig 1º | %≥17h 2º | flags |
|---|---:|---:|---:|---:|---|
| `AC:01031:0003:0095` | 130 | -10 | 8.1818 | 0.0 | margem|pos17 |
| `AC:01554:0003:0160` | -113 | -5 | 21.1765 | 0.0 | margem|sem_digital_x_margem|pos17 |
| `AC:01040:0004:0223` | 86 | 105 | 17.2414 | 0.0 | abstencao|margem|sem_digital_x_margem|pos17 |
| `AC:01040:0004:0160` | 79 | 87 | 8.8235 | 0.0 | abstencao|margem|pos17 |
| `AC:01040:0004:0324` | 74 | 88 | 7.2816 | 0.0 | abstencao|margem|pos17 |
| `AC:01473:0005:0063` | 73 | 90 | 13.0597 | 0.0 | abstencao|margem|sem_digital_x_margem|pos17 |
| `AC:01104:0005:0056` | 62 | 89 | 23.5043 | 0.0 | abstencao|margem|sem_digital_x_margem|pos17 |
| `AC:01139:0007:0067` | 62 | 25 | 26.5306 | 0.0 | margem|sem_digital_x_margem|pos17 |
| `AC:01139:0007:0089` | 55 | 21 | 11.245 | 0.0 | margem|sem_digital_x_margem|pos17 |
| `AC:01058:0006:0023` | 50 | 16 | 10.5072 | 0.3846 | margem|pos17 |
| `AC:01082:0004:0241` | 50 | 49 | 12.3348 | 0.0 | abstencao|margem|sem_digital_x_margem|pos17 |
| `AC:01090:0004:0283` | 48 | 71 | 17.1429 | 0.0 | abstencao|margem|sem_digital_x_margem|pos17 |
| `AC:01392:0009:0463` | 48 | 25 | 16.5975 | 0.0 | margem|sem_digital_x_margem|pos17 |
| `AC:01473:0005:0092` | 47 | 71 | 14.9733 | 0.0 | abstencao|margem|sem_digital_x_margem|pos17 |
| `AC:01473:0005:0144` | 47 | 72 | 10.0806 | 0.0 | abstencao|margem|pos17 |

## Seções com flag

2,270 seção(ões) (até 30):

- `AC:01007:0009:0001` · pos17 · Δmargem=-5 · Δabst=9
- `AC:01007:0009:0002` · pos17 · Δmargem=-2 · Δabst=8
- `AC:01007:0009:0003` · pos17 · Δmargem=13 · Δabst=1
- `AC:01007:0009:0004` · pos17 · Δmargem=12 · Δabst=10
- `AC:01007:0009:0005` · pos17 · Δmargem=15 · Δabst=17
- `AC:01007:0009:0006` · pos17 · Δmargem=11 · Δabst=19
- `AC:01007:0009:0007` · pos17 · Δmargem=11 · Δabst=9
- `AC:01007:0009:0008` · pos17 · Δmargem=13 · Δabst=14
- `AC:01007:0009:0009` · pos17 · Δmargem=16 · Δabst=23
- `AC:01007:0009:0010` · pos17 · Δmargem=18 · Δabst=27
- `AC:01007:0009:0120` · pos17 · Δmargem=15 · Δabst=16
- `AC:01007:0009:0136` · pos17 · Δmargem=6 · Δabst=16
- `AC:01007:0009:0137` · pos17 · Δmargem=9 · Δabst=19
- `AC:01007:0009:0163` · pos17 · Δmargem=9 · Δabst=8
- `AC:01007:0009:0186` · pos17 · Δmargem=22 · Δabst=28
- `AC:01007:0009:0192` · pos17 · Δmargem=12 · Δabst=20
- `AC:01007:0009:0200` · pos17 · Δmargem=-4 · Δabst=9
- `AC:01007:0009:0201` · pos17 · Δmargem=23 · Δabst=10
- `AC:01007:0009:0202` · pos17 · Δmargem=-4 · Δabst=14
- `AC:01007:0009:0208` · pos17 · Δmargem=16 · Δabst=11
- `AC:01007:0009:0212` · pos17 · Δmargem=10 · Δabst=9
- `AC:01007:0009:0237` · pos17 · Δmargem=-1 · Δabst=10
- `AC:01007:0009:0242` · pos17 · Δmargem=-1 · Δabst=19
- `AC:01007:0009:0252` · pos17 · Δmargem=7 · Δabst=16
- `AC:01007:0009:0304` · pos17 · Δmargem=27 · Δabst=22
- `AC:01007:0009:0305` · pos17 · Δmargem=17 · Δabst=22
- `AC:01007:0009:0310` · pos17 · Δmargem=5 · Δabst=29
- `AC:01007:0009:0411` · pos17 · Δmargem=4 · Δabst=24
- `AC:01007:0009:0412` · margem|pos17 · Δmargem=33 · Δabst=19
- `AC:01007:0009:0413` · pos17 · Δmargem=20 · Δabst=11
- … e mais 2240

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
