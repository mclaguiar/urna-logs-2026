# Curva horária — PI 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério pós-encerramento: ≥17h no **horário de Brasília**.

## Resumo

- Habilitações: **2,242,127** (com hora: **2,242,127**)
- Seções: **10,225** · urnas: **10,267**
- Pico (hora local): **11h** (262,536)
- % ≥17h (ref. brasilia): **3.3652** · 17–18h: **2.657** · 18–19h: **0.587** · 19h+: **0.1212**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 08h | 215,413 | 9.6075 |  |
| 09h | 244,246 | 10.8935 |  |
| 10h | 259,338 | 11.5666 |  |
| 11h | 262,536 | 11.7092 |  |
| 12h | 253,138 | 11.2901 |  |
| 13h | 243,974 | 10.8814 |  |
| 14h | 237,075 | 10.5737 |  |
| 15h | 235,515 | 10.5041 |  |
| 16h | 215,439 | 9.6087 |  |
| 17h | 59,574 | 2.657 | sim |
| 18h | 13,162 | 0.587 | sim |
| 19h | 2,348 | 0.1047 | sim |
| 20h | 324 | 0.0145 | sim |
| 21h | 45 | 0.002 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
