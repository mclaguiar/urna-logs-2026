# Curva horária — RS 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério pós-encerramento: ≥17h no **horário de Brasília**.

## Resumo

- Habilitações: **6,704,686** (com hora: **6,704,686**)
- Seções: **27,547** · urnas: **27,677**
- Pico (hora local): **11h** (871,594)
- % ≥17h (ref. brasilia): **0.4656** · 17–18h: **0.4437** · 18–19h: **0.0204** · 19h+: **0.0015**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 08h | 669,940 | 9.9921 |  |
| 09h | 769,635 | 11.4791 |  |
| 10h | 853,444 | 12.7291 |  |
| 11h | 871,594 | 12.9998 |  |
| 12h | 810,676 | 12.0912 |  |
| 13h | 767,401 | 11.4457 |  |
| 14h | 754,811 | 11.258 |  |
| 15h | 682,588 | 10.1808 |  |
| 16h | 493,380 | 7.3587 |  |
| 17h | 29,748 | 0.4437 | sim |
| 18h | 1,369 | 0.0204 | sim |
| 19h | 88 | 0.0013 | sim |
| 20h | 12 | 0.0002 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
