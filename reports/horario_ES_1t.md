# Curva horária — ES 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério pós-encerramento: ≥17h no **horário de Brasília**.

## Resumo

- Habilitações: **2,353,067** (com hora: **2,353,067**)
- Seções: **9,844** · urnas: **9,878**
- Pico (hora local): **11h** (292,468)
- % ≥17h (ref. brasilia): **1.2855** · 17–18h: **1.2081** · 18–19h: **0.0743** · 19h+: **0.0031**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 08h | 234,285 | 9.9566 |  |
| 09h | 266,241 | 11.3146 |  |
| 10h | 284,991 | 12.1115 |  |
| 11h | 292,468 | 12.4292 |  |
| 12h | 281,006 | 11.9421 |  |
| 13h | 265,641 | 11.2891 |  |
| 14h | 257,895 | 10.96 |  |
| 15h | 242,652 | 10.3122 |  |
| 16h | 197,639 | 8.3992 |  |
| 17h | 28,427 | 1.2081 | sim |
| 18h | 1,748 | 0.0743 | sim |
| 19h | 74 | 0.0031 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
