# Curva horária — MT 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-4).
Critério pós-encerramento: ≥17h no **horário de Brasília** (local +1h → BRT).

## Resumo

- Habilitações: **2,053,208** (com hora: **2,053,208**)
- Seções: **8,287** · urnas: **8,305**
- Pico (hora local): **10h** (251,095)
- % ≥17h (ref. brasilia): **2.7912** · 17–18h: **2.5044** · 18–19h: **0.2615** · 19h+: **0.0253**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 07h | 175,540 | 8.5495 |  |
| 08h | 211,118 | 10.2823 |  |
| 09h | 233,846 | 11.3893 |  |
| 10h | 251,095 | 12.2294 |  |
| 11h | 248,821 | 12.1186 |  |
| 12h | 234,186 | 11.4059 |  |
| 13h | 223,912 | 10.9055 |  |
| 14h | 218,045 | 10.6197 |  |
| 15h | 199,335 | 9.7085 |  |
| 16h | 51,421 | 2.5044 | sim |
| 17h | 5,370 | 0.2615 | sim |
| 18h | 478 | 0.0233 | sim |
| 19h | 41 | 0.002 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
