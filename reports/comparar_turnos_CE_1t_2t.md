# Comparativo 1º × 2º turno — CE

Status: **pronto**

Comparativo 1º×2º preenchido (finalistas 13×22; saldo agregado por seção — não é migração eleitor a eleitor).

## Disponibilidade

- 1º turno (audit): sim · 23,765 seções
- 2º turno (audit): sim · 23,765 seções
- Finalistas (nominais no 2º): **13** e **22**
- Margem = votos(13) − votos(22)

## Métricas

- Seções em ambos: **23,765**
- Só no 1º: **0** · só no 2º: **0**
- Δ comparecimento (soma seções ambos): **114372**
- Δ abstenção (pp, aptos ambos): **-1.635**
- % sem digital 1º→2º: **10.9036** → **11.1664** (Δ **0.2628**)

## Pós-17h (UF)

- % ≥17h no 1º: **5.9899**
- % ≥17h no 2º: **0.0159**
- Δ (2º − 1º): **-5.974**

## Flags de anomalia (percentis na UF)

- `|Δ abstenção|` ≥ p95: **1236**
- `|Δ margem|` ≥ p95: **1267**
- alto % sem digital 1º × `|Δ margem|`: **256**
- cauda pós-17h atípica: **23765**
- só em um turno: **0**

## Seções que mais movem a margem (13−22)

| join_key | Δ margem | Δ abst | % sem dig 1º | %≥17h 2º | flags |
|---|---:|---:|---:|---:|---|
| `CE:15490:0036:0054` | 78 | 3 | 13.8298 | 0.0 | margem|sem_digital_x_margem|pos17 |
| `CE:15490:0036:0070` | 71 | -11 | 8.9888 | 0.0 | margem|pos17 |
| `CE:13730:0120:0320` | 68 | 15 | 12.5506 | 0.0 | margem|pos17 |
| `CE:13730:0120:0226` | 67 | -15 | 7.4468 | 0.0 | margem|pos17 |
| `CE:15695:0081:0114` | 66 | -12 | 9.434 | 0.0 | margem|pos17 |
| `CE:13897:0118:0510` | 65 | -4 | 5.4545 | 0.0 | margem|pos17 |
| `CE:13951:0025:0228` | 65 | -28 | 32.5203 | 0.0 | abstencao|margem|sem_digital_x_margem|pos17 |
| `CE:13897:0002:0810` | 64 | -17 | 3.9275 | 0.0 | margem|pos17 |
| `CE:13897:0095:0257` | 64 | -12 | 13.881 | 0.0 | margem|sem_digital_x_margem|pos17 |
| `CE:14478:0028:0448` | 62 | -19 | 6.0837 | 0.0 | abstencao|margem|pos17 |
| `CE:13897:0114:0285` | 62 | -2 | 15.2941 | 0.2915 | margem|sem_digital_x_margem|pos17 |
| `CE:98574:0065:0197` | 62 | 0 | 19.2 | 0.4 | margem|sem_digital_x_margem|pos17 |
| `CE:13897:0095:0317` | 61 | -11 | 4.1667 | 0.0 | margem|pos17 |
| `CE:13730:0120:0315` | 59 | -6 | 12.749 | 0.0 | margem|pos17 |
| `CE:13730:0120:0409` | 59 | -3 | 4.8611 | 0.0 | margem|pos17 |

## Seções com flag

23,765 seção(ões) (até 30):

- `CE:13005:0030:0082` · pos17 · Δmargem=33 · Δabst=8
- `CE:13005:0030:0087` · pos17 · Δmargem=18 · Δabst=-10
- `CE:13005:0030:0088` · pos17 · Δmargem=32 · Δabst=-12
- `CE:13005:0030:0092` · abstencao|margem|pos17 · Δmargem=38 · Δabst=-22
- `CE:13005:0030:0093` · pos17 · Δmargem=15 · Δabst=-10
- `CE:13005:0030:0094` · pos17 · Δmargem=22 · Δabst=-6
- `CE:13005:0030:0095` · abstencao|pos17 · Δmargem=36 · Δabst=-21
- `CE:13005:0030:0096` · pos17 · Δmargem=5 · Δabst=-14
- `CE:13005:0030:0097` · pos17 · Δmargem=34 · Δabst=-14
- `CE:13005:0030:0109` · abstencao|pos17 · Δmargem=9 · Δabst=-19
- `CE:13005:0030:0110` · pos17 · Δmargem=25 · Δabst=-14
- `CE:13005:0030:0111` · pos17 · Δmargem=21 · Δabst=-4
- `CE:13005:0030:0115` · pos17 · Δmargem=26 · Δabst=-8
- `CE:13005:0030:0116` · pos17 · Δmargem=21 · Δabst=-12
- `CE:13005:0030:0167` · pos17 · Δmargem=14 · Δabst=-1
- `CE:13005:0030:0168` · pos17 · Δmargem=3 · Δabst=-3
- `CE:13005:0030:0182` · pos17 · Δmargem=1 · Δabst=-2
- `CE:13005:0030:0205` · pos17 · Δmargem=19 · Δabst=-2
- `CE:13005:0030:0206` · pos17 · Δmargem=24 · Δabst=-15
- `CE:13005:0030:0211` · pos17 · Δmargem=12 · Δabst=-13
- `CE:13005:0030:0223` · pos17 · Δmargem=26 · Δabst=-9
- `CE:13005:0030:0227` · pos17 · Δmargem=19 · Δabst=-15
- `CE:13005:0030:0228` · pos17 · Δmargem=35 · Δabst=-11
- `CE:13005:0030:0229` · pos17 · Δmargem=27 · Δabst=-13
- `CE:13005:0030:0243` · margem|pos17 · Δmargem=38 · Δabst=-12
- `CE:13005:0030:0246` · pos17 · Δmargem=21 · Δabst=-16
- `CE:13005:0030:0256` · pos17 · Δmargem=22 · Δabst=-4
- `CE:13005:0030:0257` · pos17 · Δmargem=12 · Δabst=-5
- `CE:13005:0030:0268` · abstencao|pos17 · Δmargem=35 · Δabst=-18
- `CE:13005:0030:0285` · pos17 · Δmargem=30 · Δabst=-12
- … e mais 23735

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
