# Curva horária — MS 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-4).
Critério pós-encerramento: ≥17h no **horário de Brasília** (local +1h → BRT).

## Resumo

- Habilitações: **1,541,987** (com hora: **1,541,987**)
- Seções: **7,106** · urnas: **7,129**
- Pico (hora local): **10h** (199,965)
- % ≥17h (ref. brasilia): **1.0929** · 17–18h: **1.0267** · 18–19h: **0.0624** · 19h+: **0.0038**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 07h | 131,293 | 8.5145 |  |
| 08h | 143,252 | 9.2901 |  |
| 09h | 179,086 | 11.614 |  |
| 10h | 199,965 | 12.968 |  |
| 11h | 198,439 | 12.869 |  |
| 12h | 184,074 | 11.9375 |  |
| 13h | 171,378 | 11.1141 |  |
| 14h | 170,228 | 11.0395 |  |
| 15h | 147,419 | 9.5603 |  |
| 16h | 15,832 | 1.0267 | sim |
| 17h | 962 | 0.0624 | sim |
| 18h | 59 | 0.0038 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
