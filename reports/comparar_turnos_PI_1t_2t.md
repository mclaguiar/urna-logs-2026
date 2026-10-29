# Comparativo 1º × 2º turno — PI

Status: **pronto**

Comparativo 1º×2º preenchido (finalistas 13×22; saldo agregado por seção — não é migração eleitor a eleitor).

## Disponibilidade

- 1º turno (audit): sim · 10,225 seções
- 2º turno (audit): sim · 10,225 seções
- Finalistas (nominais no 2º): **13** e **22**
- Margem = votos(13) − votos(22)

## Métricas

- Seções em ambos: **10,225**
- Só no 1º: **0** · só no 2º: **0**
- Δ comparecimento (soma seções ambos): **-1053**
- Δ abstenção (pp, aptos ambos): **0.037**
- % sem digital 1º→2º: **10.6885** → **10.9993** (Δ **0.3108**)

## Pós-17h (UF)

- % ≥17h no 1º: **3.3652**
- % ≥17h no 2º: **0.0133**
- Δ (2º − 1º): **-3.3519**

## Flags de anomalia (percentis na UF)

- `|Δ abstenção|` ≥ p95: **548**
- `|Δ margem|` ≥ p95: **525**
- alto % sem digital 1º × `|Δ margem|`: **114**
- cauda pós-17h atípica: **10225**
- só em um turno: **0**

## Seções que mais movem a margem (13−22)

| join_key | Δ margem | Δ abst | % sem dig 1º | %≥17h 2º | flags |
|---|---:|---:|---:|---:|---|
| `PI:11878:0028:0099` | -134 | 14 | 11.1498 | 0.0 | margem|pos17 |
| `PI:12190:0002:0532` | 57 | -10 | 8.6275 | 0.0 | margem|pos17 |
| `PI:12190:0002:0418` | 55 | -10 | 8.3851 | 0.0 | margem|pos17 |
| `PI:11878:0028:0094` | -52 | 6 | 13.5246 | 0.0 | margem|pos17 |
| `PI:12190:0002:0429` | 51 | -10 | 3.9877 | 0.0 | margem|pos17 |
| `PI:12190:0002:0550` | 51 | -7 | 41.4035 | 0.0 | margem|sem_digital_x_margem|pos17 |
| `PI:10049:0044:0057` | 49 | -6 | 13.1356 | 0.0 | margem|pos17 |
| `PI:12190:0098:0228` | 49 | -1 | 3.7975 | 0.0 | margem|pos17 |
| `PI:12190:0098:0318` | 49 | 2 | 8.8028 | 0.0 | margem|pos17 |
| `PI:12190:0098:0065` | 48 | -24 | 4.127 | 0.0 | abstencao|margem|pos17 |
| `PI:12190:0098:0067` | 48 | -26 | 3.6184 | 0.0 | abstencao|margem|pos17 |
| `PI:10537:0053:0114` | 47 | -16 | 7.9812 | 0.0 | abstencao|margem|pos17 |
| `PI:10936:0064:0036` | 47 | -19 | 8.1967 | 0.0 | abstencao|margem|pos17 |
| `PI:12190:0098:0308` | 47 | -11 | 11.6667 | 0.0 | margem|pos17 |
| `PI:12190:0001:0487` | 46 | -15 | 3.7288 | 0.0 | abstencao|margem|pos17 |

## Seções com flag

10,225 seção(ões) (até 30):

- `PI:10006:0011:0081` · margem|pos17 · Δmargem=35 · Δabst=-11
- `PI:10006:0011:0083` · pos17 · Δmargem=12 · Δabst=-5
- `PI:10006:0011:0084` · pos17 · Δmargem=9 · Δabst=-8
- `PI:10006:0011:0085` · pos17 · Δmargem=9 · Δabst=-4
- `PI:10006:0011:0086` · pos17 · Δmargem=12 · Δabst=0
- `PI:10006:0011:0087` · pos17 · Δmargem=18 · Δabst=-8
- `PI:10006:0011:0088` · pos17 · Δmargem=13 · Δabst=-2
- `PI:10006:0011:0119` · abstencao|pos17 · Δmargem=16 · Δabst=-15
- `PI:10006:0011:0120` · abstencao|pos17 · Δmargem=21 · Δabst=-19
- `PI:10006:0011:0121` · pos17 · Δmargem=0 · Δabst=-1
- `PI:10006:0011:0123` · pos17 · Δmargem=9 · Δabst=10
- `PI:10006:0011:0125` · pos17 · Δmargem=9 · Δabst=-13
- `PI:10006:0011:0126` · pos17 · Δmargem=-2 · Δabst=6
- `PI:10006:0011:0130` · pos17 · Δmargem=14 · Δabst=-2
- `PI:10006:0011:0133` · abstencao|margem|pos17 · Δmargem=31 · Δabst=-22
- `PI:10006:0011:0134` · pos17 · Δmargem=5 · Δabst=2
- `PI:10006:0011:0149` · pos17 · Δmargem=13 · Δabst=4
- `PI:10006:0011:0152` · pos17 · Δmargem=-5 · Δabst=1
- `PI:10006:0011:0165` · pos17 · Δmargem=6 · Δabst=4
- `PI:10006:0011:0166` · pos17 · Δmargem=15 · Δabst=6
- `PI:10006:0011:0176` · pos17 · Δmargem=23 · Δabst=-3
- `PI:10006:0011:0177` · pos17 · Δmargem=24 · Δabst=13
- `PI:10006:0011:0213` · pos17 · Δmargem=8 · Δabst=1
- `PI:10006:0011:0215` · pos17 · Δmargem=14 · Δabst=-8
- `PI:10006:0011:0217` · pos17 · Δmargem=17 · Δabst=3
- `PI:10006:0011:0219` · pos17 · Δmargem=10 · Δabst=-1
- `PI:10006:0011:0222` · pos17 · Δmargem=17 · Δabst=0
- `PI:10006:0011:0223` · pos17 · Δmargem=2 · Δabst=3
- `PI:10006:0011:0245` · pos17 · Δmargem=24 · Δabst=-5
- `PI:10006:0011:0250` · pos17 · Δmargem=18 · Δabst=3
- … e mais 10195

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
