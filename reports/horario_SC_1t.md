# Curva horária — SC 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério pós-encerramento: ≥17h no **horário de Brasília**.

## Resumo

- Habilitações: **4,649,499** (com hora: **4,649,499**)
- Seções: **17,326** · urnas: **17,416**
- Pico (hora local): **11h** (574,741)
- % ≥17h (ref. brasilia): **0.8225** · 17–18h: **0.7864** · 18–19h: **0.0337** · 19h+: **0.0024**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 08h | 461,496 | 9.9257 |  |
| 09h | 513,613 | 11.0466 |  |
| 10h | 557,735 | 11.9956 |  |
| 11h | 574,741 | 12.3614 |  |
| 12h | 556,423 | 11.9674 |  |
| 13h | 548,879 | 11.8051 |  |
| 14h | 536,461 | 11.538 |  |
| 15h | 491,235 | 10.5653 |  |
| 16h | 370,676 | 7.9724 |  |
| 17h | 36,562 | 0.7864 | sim |
| 18h | 1,566 | 0.0337 | sim |
| 19h | 108 | 0.0023 | sim |
| 20h | 4 | 0.0001 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
