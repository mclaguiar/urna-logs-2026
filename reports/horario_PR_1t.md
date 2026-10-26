# Curva horária — PR 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério pós-encerramento: ≥17h no **horário de Brasília**.

## Resumo

- Habilitações: **6,844,534** (com hora: **6,844,534**)
- Seções: **27,142** · urnas: **27,334**
- Pico (hora local): **12h** (876,713)
- % ≥17h (ref. brasilia): **0.6186** · 17–18h: **0.5769** · 18–19h: **0.0386** · 19h+: **0.0031**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 08h | 601,135 | 8.7827 |  |
| 09h | 692,776 | 10.1216 |  |
| 10h | 814,418 | 11.8988 |  |
| 11h | 875,992 | 12.7984 |  |
| 12h | 876,713 | 12.809 |  |
| 13h | 836,233 | 12.2175 |  |
| 14h | 810,543 | 11.8422 |  |
| 15h | 745,005 | 10.8847 |  |
| 16h | 549,381 | 8.0266 |  |
| 17h | 39,483 | 0.5769 | sim |
| 18h | 2,642 | 0.0386 | sim |
| 19h | 199 | 0.0029 | sim |
| 20h | 14 | 0.0002 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
