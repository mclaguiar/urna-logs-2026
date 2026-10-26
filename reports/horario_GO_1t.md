# Curva horária — GO 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério pós-encerramento: ≥17h no **horário de Brasília**.

## Resumo

- Habilitações: **3,973,196** (com hora: **3,973,196**)
- Seções: **15,686** · urnas: **15,740**
- Pico (hora local): **11h** (492,869)
- % ≥17h (ref. brasilia): **1.7716** · 17–18h: **1.6041** · 18–19h: **0.1582** · 19h+: **0.0093**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 08h | 388,155 | 9.7693 |  |
| 09h | 440,372 | 11.0836 |  |
| 10h | 472,926 | 11.9029 |  |
| 11h | 492,869 | 12.4048 |  |
| 12h | 477,997 | 12.0305 |  |
| 13h | 439,374 | 11.0585 |  |
| 14h | 422,611 | 10.6366 |  |
| 15h | 410,552 | 10.333 |  |
| 16h | 357,952 | 9.0092 |  |
| 17h | 63,734 | 1.6041 | sim |
| 18h | 6,285 | 0.1582 | sim |
| 19h | 342 | 0.0086 | sim |
| 20h | 27 | 0.0007 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
