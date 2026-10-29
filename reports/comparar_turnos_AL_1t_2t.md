# Comparativo 1º × 2º turno — AL

Status: **pronto**

Comparativo 1º×2º preenchido (finalistas 13×22; saldo agregado por seção — não é migração eleitor a eleitor).

## Disponibilidade

- 1º turno (audit): sim · 7,101 seções
- 2º turno (audit): sim · 7,101 seções
- Finalistas (nominais no 2º): **13** e **22**
- Margem = votos(13) − votos(22)

## Métricas

- Seções em ambos: **7,101**
- Só no 1º: **0** · só no 2º: **0**
- Δ comparecimento (soma seções ambos): **13204**
- Δ abstenção (pp, aptos ambos): **-0.5421**
- % sem digital 1º→2º: **10.1744** → **10.5463** (Δ **0.3719**)

## Pós-17h (UF)

- % ≥17h no 1º: **9.0679**
- % ≥17h no 2º: **0.0292**
- Δ (2º − 1º): **-9.0387**

## Flags de anomalia (percentis na UF)

- `|Δ abstenção|` ≥ p95: **389**
- `|Δ margem|` ≥ p95: **369**
- alto % sem digital 1º × `|Δ margem|`: **106**
- cauda pós-17h atípica: **7101**
- só em um turno: **0**

## Seções que mais movem a margem (13−22)

| join_key | Δ margem | Δ abst | % sem dig 1º | %≥17h 2º | flags |
|---|---:|---:|---:|---:|---|
| `AL:27170:0029:0056` | -68 | 15 | 9.3656 | 0.0 | margem|pos17 |
| `AL:27812:0044:0145` | 67 | -42 | 5.9055 | 0.3378 | abstencao|margem|pos17 |
| `AL:27057:0022:0159` | 67 | -26 | 5.6291 | 0.0 | abstencao|margem|pos17 |
| `AL:27170:0029:0053` | -66 | 3 | 3.5032 | 0.0 | margem|pos17 |
| `AL:27057:0022:0152` | 66 | -20 | 9.7403 | 0.0 | margem|pos17 |
| `AL:27170:0029:0023` | -66 | 7 | 15.2778 | 0.0 | margem|sem_digital_x_margem|pos17 |
| `AL:27170:0029:0047` | -65 | 12 | 6.3091 | 0.0 | margem|pos17 |
| `AL:28339:0013:0097` | 65 | -9 | 6.1818 | 0.0 | margem|pos17 |
| `AL:27855:0054:0127` | 65 | -23 | 5.8355 | 0.0 | abstencao|margem|pos17 |
| `AL:27855:0003:0087` | 64 | -19 | 16.6667 | 0.0 | margem|sem_digital_x_margem|pos17 |
| `AL:27855:0003:0061` | 63 | 1 | 12.3779 | 0.3268 | margem|pos17 |
| `AL:28894:0031:0139` | 62 | -19 | 26.7361 | 0.0 | margem|sem_digital_x_margem|pos17 |
| `AL:27855:0033:0288` | 60 | -15 | 10.7955 | 0.0 | margem|pos17 |
| `AL:27855:0033:0094` | 59 | -17 | 5.2632 | 0.0 | margem|pos17 |
| `AL:27510:0049:0079` | 59 | -22 | 9.2527 | 0.0 | margem|pos17 |

## Seções com flag

7,101 seção(ões) (até 30):

- `AL:27006:0017:0011` · pos17 · Δmargem=17 · Δabst=4
- `AL:27006:0017:0012` · pos17 · Δmargem=12 · Δabst=9
- `AL:27006:0017:0013` · pos17 · Δmargem=19 · Δabst=9
- `AL:27006:0017:0014` · pos17 · Δmargem=26 · Δabst=0
- `AL:27006:0017:0015` · pos17 · Δmargem=24 · Δabst=-1
- `AL:27006:0017:0016` · pos17 · Δmargem=17 · Δabst=14
- `AL:27006:0017:0017` · pos17 · Δmargem=40 · Δabst=14
- `AL:27006:0017:0018` · pos17 · Δmargem=11 · Δabst=10
- `AL:27006:0017:0072` · pos17 · Δmargem=11 · Δabst=2
- `AL:27006:0017:0073` · pos17 · Δmargem=23 · Δabst=4
- `AL:27006:0017:0074` · pos17 · Δmargem=21 · Δabst=3
- `AL:27006:0017:0078` · pos17 · Δmargem=25 · Δabst=5
- `AL:27006:0017:0092` · pos17 · Δmargem=37 · Δabst=4
- `AL:27006:0017:0093` · pos17 · Δmargem=12 · Δabst=9
- `AL:27006:0017:0094` · pos17 · Δmargem=27 · Δabst=12
- `AL:27006:0017:0095` · pos17 · Δmargem=30 · Δabst=4
- `AL:27006:0017:0119` · pos17 · Δmargem=25 · Δabst=0
- `AL:27006:0017:0120` · pos17 · Δmargem=36 · Δabst=9
- `AL:27006:0017:0132` · pos17 · Δmargem=31 · Δabst=6
- `AL:27006:0017:0145` · pos17 · Δmargem=9 · Δabst=19
- `AL:27006:0017:0157` · pos17 · Δmargem=25 · Δabst=11
- `AL:27006:0017:0160` · pos17 · Δmargem=14 · Δabst=7
- `AL:27006:0017:0163` · pos17 · Δmargem=26 · Δabst=13
- `AL:27006:0017:0165` · pos17 · Δmargem=23 · Δabst=15
- `AL:27006:0017:0166` · pos17 · Δmargem=1 · Δabst=9
- `AL:27006:0017:0170` · pos17 · Δmargem=31 · Δabst=17
- `AL:27006:0017:0171` · abstencao|pos17 · Δmargem=18 · Δabst=23
- `AL:27006:0017:0174` · pos17 · Δmargem=23 · Δabst=19
- `AL:27006:0017:0178` · margem|sem_digital_x_margem|pos17 · Δmargem=43 · Δabst=15
- `AL:27006:0017:0181` · pos17 · Δmargem=26 · Δabst=19
- … e mais 7071

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
