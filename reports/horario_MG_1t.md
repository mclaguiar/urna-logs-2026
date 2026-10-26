# Curva horária — MG 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério pós-encerramento: ≥17h no **horário de Brasília**.

## Resumo

- Habilitações: **12,640,883** (com hora: **12,640,883**)
- Seções: **52,062** · urnas: **52,217**
- Pico (hora local): **11h** (1,555,744)
- % ≥17h (ref. brasilia): **1.9665** · 17–18h: **1.7087** · 18–19h: **0.2308** · 19h+: **0.0269**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 08h | 1,268,878 | 10.0379 |  |
| 09h | 1,427,657 | 11.294 |  |
| 10h | 1,509,271 | 11.9396 |  |
| 11h | 1,555,744 | 12.3072 |  |
| 12h | 1,517,924 | 12.0081 |  |
| 13h | 1,412,723 | 11.1758 |  |
| 14h | 1,336,974 | 10.5766 |  |
| 15h | 1,263,405 | 9.9946 |  |
| 16h | 1,099,722 | 8.6997 |  |
| 17h | 216,001 | 1.7087 | sim |
| 18h | 29,181 | 0.2308 | sim |
| 19h | 2,900 | 0.0229 | sim |
| 20h | 374 | 0.003 | sim |
| 21h | 82 | 0.0006 | sim |
| 22h | 27 | 0.0002 | sim |
| 23h | 20 | 0.0002 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
