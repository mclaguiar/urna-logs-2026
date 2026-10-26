# Curva horária — TO 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério pós-encerramento: ≥17h no **horário de Brasília**.

## Resumo

- Habilitações: **965,768** (com hora: **965,768**)
- Seções: **4,384** · urnas: **4,388**
- Pico (hora local): **11h** (118,730)
- % ≥17h (ref. brasilia): **1.5536** · 17–18h: **1.4393** · 18–19h: **0.1087** · 19h+: **0.0056**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 08h | 92,963 | 9.6258 |  |
| 09h | 107,644 | 11.1459 |  |
| 10h | 116,492 | 12.0621 |  |
| 11h | 118,730 | 12.2938 |  |
| 12h | 111,341 | 11.5288 |  |
| 13h | 105,353 | 10.9087 |  |
| 14h | 103,295 | 10.6956 |  |
| 15h | 102,419 | 10.6049 |  |
| 16h | 92,527 | 9.5807 |  |
| 17h | 13,900 | 1.4393 | sim |
| 18h | 1,050 | 0.1087 | sim |
| 19h | 54 | 0.0056 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
