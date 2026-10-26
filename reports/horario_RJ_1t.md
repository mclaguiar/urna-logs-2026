# Curva horária — RJ 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério pós-encerramento: ≥17h no **horário de Brasília**.

## Resumo

- Habilitações: **9,863,105** (com hora: **9,863,105**)
- Seções: **37,675** · urnas: **37,874**
- Pico (hora local): **11h** (1,180,044)
- % ≥17h (ref. brasilia): **2.3019** · 17–18h: **2.0513** · 18–19h: **0.2329** · 19h+: **0.0176**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 08h | 982,588 | 9.9623 |  |
| 09h | 1,085,903 | 11.0097 |  |
| 10h | 1,138,783 | 11.5459 |  |
| 11h | 1,180,044 | 11.9642 |  |
| 12h | 1,179,864 | 11.9624 |  |
| 13h | 1,128,291 | 11.4395 |  |
| 14h | 1,061,457 | 10.7619 |  |
| 15h | 1,003,476 | 10.174 |  |
| 16h | 875,660 | 8.8781 |  |
| 17h | 202,326 | 2.0513 | sim |
| 18h | 22,974 | 0.2329 | sim |
| 19h | 1,687 | 0.0171 | sim |
| 20h | 52 | 0.0005 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
