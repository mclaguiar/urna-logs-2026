# Curva horária — SP 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério pós-encerramento: ≥17h no **horário de Brasília**.

## Resumo

- Habilitações: **26,439,279** (com hora: **26,439,279**)
- Seções: **103,656** · urnas: **104,073**
- Pico (hora local): **11h** (3,437,597)
- % ≥17h (ref. brasilia): **0.3664** · 17–18h: **0.3584** · 18–19h: **0.0074** · 19h+: **0.0006**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 08h | 2,902,498 | 10.978 |  |
| 09h | 3,140,855 | 11.8795 |  |
| 10h | 3,313,353 | 12.5319 |  |
| 11h | 3,437,597 | 13.0019 |  |
| 12h | 3,372,614 | 12.7561 |  |
| 13h | 3,070,517 | 11.6135 |  |
| 14h | 2,760,502 | 10.4409 |  |
| 15h | 2,380,176 | 9.0024 |  |
| 16h | 1,964,306 | 7.4295 |  |
| 17h | 94,748 | 0.3584 | sim |
| 18h | 1,960 | 0.0074 | sim |
| 19h | 105 | 0.0004 | sim |
| 20h | 33 | 0.0001 | sim |
| 21h | 15 | 0.0001 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
