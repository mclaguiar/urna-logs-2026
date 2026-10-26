# Curva horária — RR 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-4).
Critério pós-encerramento: ≥17h no **horário de Brasília** (local +1h → BRT).

## Resumo

- Habilitações: **333,054** (com hora: **333,054**)
- Seções: **1,519** · urnas: **1,522**
- Pico (hora local): **10h** (44,781)
- % ≥17h (ref. brasilia): **0.9467** · 17–18h: **0.8068** · 18–19h: **0.1033** · 19h+: **0.0366**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 07h | 30,665 | 9.2072 |  |
| 08h | 36,824 | 11.0565 |  |
| 09h | 42,157 | 12.6577 |  |
| 10h | 44,781 | 13.4456 |  |
| 11h | 42,862 | 12.8694 |  |
| 12h | 36,255 | 10.8856 |  |
| 13h | 32,132 | 9.6477 |  |
| 14h | 33,004 | 9.9095 |  |
| 15h | 31,221 | 9.3742 |  |
| 16h | 2,687 | 0.8068 | sim |
| 17h | 344 | 0.1033 | sim |
| 18h | 118 | 0.0354 | sim |
| 19h | 4 | 0.0012 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
