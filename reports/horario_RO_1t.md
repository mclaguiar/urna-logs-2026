# Curva horária — RO 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-4).
Critério pós-encerramento: ≥17h no **horário de Brasília** (local +1h → BRT).

## Resumo

- Habilitações: **991,781** (com hora: **991,781**)
- Seções: **4,698** · urnas: **4,711**
- Pico (hora local): **10h** (135,482)
- % ≥17h (ref. brasilia): **0.3825** · 17–18h: **0.3756** · 18–19h: **0.007** · 19h+: **0.0**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 07h | 98,966 | 9.9786 |  |
| 08h | 114,250 | 11.5197 |  |
| 09h | 126,847 | 12.7898 |  |
| 10h | 135,482 | 13.6605 |  |
| 11h | 128,773 | 12.984 |  |
| 12h | 109,612 | 11.052 |  |
| 13h | 97,867 | 9.8678 |  |
| 14h | 95,758 | 9.6552 |  |
| 15h | 80,432 | 8.1099 |  |
| 16h | 3,725 | 0.3756 | sim |
| 17h | 69 | 0.007 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
