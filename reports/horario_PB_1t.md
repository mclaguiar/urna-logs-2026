# Curva horária — PB 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério pós-encerramento: ≥17h no **horário de Brasília**.

## Resumo

- Habilitações: **2,685,567** (com hora: **2,685,567**)
- Seções: **10,712** · urnas: **10,766**
- Pico (hora local): **11h** (304,359)
- % ≥17h (ref. brasilia): **3.9493** · 17–18h: **3.3701** · 18–19h: **0.526** · 19h+: **0.0532**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 08h | 246,782 | 9.1892 |  |
| 09h | 272,043 | 10.1298 |  |
| 10h | 291,872 | 10.8682 |  |
| 11h | 304,359 | 11.3331 |  |
| 12h | 303,076 | 11.2854 |  |
| 13h | 295,103 | 10.9885 |  |
| 14h | 292,597 | 10.8952 |  |
| 15h | 296,021 | 11.0227 |  |
| 16h | 277,653 | 10.3387 |  |
| 17h | 90,507 | 3.3701 | sim |
| 18h | 14,125 | 0.526 | sim |
| 19h | 1,327 | 0.0494 | sim |
| 20h | 101 | 0.0038 | sim |
| 21h | 1 | 0.0 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
