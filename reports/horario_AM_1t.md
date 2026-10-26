# Curva horária — AM 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-4).
Critério pós-encerramento: ≥17h no **horário de Brasília** (local +1h → BRT).

## Resumo

- Habilitações: **2,235,742** (com hora: **2,235,742**)
- Seções: **8,157** · urnas: **8,186**
- Pico (hora local): **11h** (248,314)
- % ≥17h (ref. brasilia): **6.5948** · 17–18h: **5.0688** · 18–19h: **1.2242** · 19h+: **0.3018**

## Contagem por hora (local)

| Hora local | Habilitações | % | ≥17h BRT* |
|---:|---:|---:|:---:|
| 06h | 11,424 | 0.511 |  |
| 07h | 183,352 | 8.2009 |  |
| 08h | 210,695 | 9.4239 |  |
| 09h | 227,021 | 10.1542 |  |
| 10h | 241,786 | 10.8146 |  |
| 11h | 248,314 | 11.1066 |  |
| 12h | 246,244 | 11.014 |  |
| 13h | 244,374 | 10.9303 |  |
| 14h | 243,015 | 10.8695 |  |
| 15h | 232,074 | 10.3802 |  |
| 16h | 113,325 | 5.0688 | sim |
| 17h | 27,370 | 1.2242 | sim |
| 18h | 5,212 | 0.2331 | sim |
| 19h | 1,170 | 0.0523 | sim |
| 20h | 346 | 0.0155 | sim |
| 21h | 20 | 0.0009 | sim |

\* Exterior (ZZ): coluna marca ≥17h **local**. Demais UFs: ≥17h Brasília.

## Nota

Não se espera distribuição normal: multimodal (manhã/tarde) + cauda pós-encerramento.
