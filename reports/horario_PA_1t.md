# Curva horária — PA 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério pós-encerramento: ≥17h no **horário de Brasília**.

## Resumo

- Habilitações: **5,069,004** (com hora: **5,069,004**)
- Seções: **20,827** · urnas: **20,892**
- Pico (hora local): **11h** (573,435)
- % ≥17h (ref. brasilia): **5.5965** · 17–18h: **4.311** · 18–19h: **1.0574** · 19h+: **0.2282**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 08h | 449,992 | 8.8773 |  |
| 09h | 517,219 | 10.2036 |  |
| 10h | 554,340 | 10.9359 |  |
| 11h | 573,435 | 11.3126 |  |
| 12h | 554,357 | 10.9362 |  |
| 13h | 541,643 | 10.6854 |  |
| 14h | 540,446 | 10.6618 |  |
| 15h | 535,862 | 10.5713 |  |
| 16h | 518,021 | 10.2194 |  |
| 17h | 218,524 | 4.311 | sim |
| 18h | 53,599 | 1.0574 | sim |
| 19h | 10,037 | 0.198 | sim |
| 20h | 1,373 | 0.0271 | sim |
| 21h | 136 | 0.0027 | sim |
| 22h | 20 | 0.0004 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
