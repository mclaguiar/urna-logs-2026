# Curva horária — MT 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-4).
Critério: janela **8h–17h Brasília** (local +1h → BRT); ≥17h = pós-encerramento (fila).

Métricas deste relatório = **somente o dia oficial deste turno**.
Janelas no dia: **oficial** [8h,17h) · **pós-encerramento** ≥17h · **fora do previsto** &lt;8h.
Eventos de **outra data** no `.jez` = histórico (não entram nos totais nem no comparativo 1º×2º).
Dia oficial deste turno: **2026-10-04**.

## Resumo (só o dia do turno)

- Habilitações no dia: **2,053,208**
  - **1,075** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **993** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **82** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **1,995,898** (97.2088%)
- Pós-encerramento ≥17h: **57,310** (% entre oficial+pós: **2.7912**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **8,287** · urnas: **8,305**
- Pico (hora local): **10h** (251,095)
- Faixas ≥17h (ref. brasilia): 17–18h **2.5044** · 18–19h **0.2615** · 19h+ **0.0253**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **2,053,208**
- Votos computados no log (`O voto do eleitor foi computado`): **2,052,133**
- Votos de presidente no BU: **2,052,133**
  - nominais **1,993,383** · brancos **20,756** · nulos **37,994**

**+1,075** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**2,052,133** = **2,052,133**). O +1,075 está fora dessa conta.
- **993** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **82** — o voto também não foi registrado, e o log não traz essa frase.

## Como foi a habilitação

No **boletim (BU)** há três caminhos:

- **Com digital:** a urna reconheceu a digital do eleitor.
- **Biografia:** tinha digital cadastrada, o reconhecimento não fechou, e a liberação foi pelo ano de nascimento mais a digital do mesário.
- **Sem biometria:** não tinha digital cadastrada, e a liberação foi a mesma (ano de nascimento mais a digital do mesário).

Sem digital no BU = biografia + sem biometria.

Neste relatório a fonte é o **log**, nas linhas anteriores a `Eleitor foi habilitado`:

- **Com digital:** `Tipo de habilitação do eleitor [biométrica]`.
- **Manual:** ano de nascimento conferido, pedido de habilitação manual ou digital do mesário. Em 2026 o log usa essas mesmas frases para biografia e para sem biometria, então os dois caminhos caem aqui.
- **Sem biometria:** só entra se o log escrever `O eleitor não possui biometria` ou `Eleitor sem dados biométricos`. Quando essa frase não aparece, a coluna fica em zero e esses eleitores estão dentro de Manual.
- **Não classificada:** a janela anterior não trouxe nenhum desses sinais.

### Totais do dia

- Com digital: **1,837,787** (89.51% do dia)
- Manual: **215,352** (10.49% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **69** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 07h | 175,540 | 8.5495 | oficial | 153,397 | 87.3858 | 22,132 | 12.608 | 0 | 0.0 | 11 | 0.0063 |
| 08h | 211,118 | 10.2823 | oficial | 185,627 | 87.9257 | 25,487 | 12.0724 | 0 | 0.0 | 4 | 0.0019 |
| 09h | 233,846 | 11.3893 | oficial | 208,201 | 89.0334 | 25,642 | 10.9653 | 0 | 0.0 | 3 | 0.0013 |
| 10h | 251,095 | 12.2294 | oficial | 226,543 | 90.222 | 24,543 | 9.7744 | 0 | 0.0 | 9 | 0.0036 |
| 11h | 248,821 | 12.1186 | oficial | 225,794 | 90.7456 | 23,021 | 9.252 | 0 | 0.0 | 6 | 0.0024 |
| 12h | 234,186 | 11.4059 | oficial | 211,711 | 90.4029 | 22,469 | 9.5945 | 0 | 0.0 | 6 | 0.0026 |
| 13h | 223,912 | 10.9055 | oficial | 201,505 | 89.9929 | 22,397 | 10.0026 | 0 | 0.0 | 10 | 0.0045 |
| 14h | 218,045 | 10.6197 | oficial | 195,441 | 89.6333 | 22,596 | 10.363 | 0 | 0.0 | 8 | 0.0037 |
| 15h | 199,335 | 9.7085 | oficial | 178,352 | 89.4735 | 20,976 | 10.523 | 0 | 0.0 | 7 | 0.0035 |
| 16h | 51,421 | 2.5044 | pós-encerramento | 46,019 | 89.4946 | 5,397 | 10.4957 | 0 | 0.0 | 5 | 0.0097 |
| 17h | 5,370 | 0.2615 | pós-encerramento | 4,766 | 88.7523 | 604 | 11.2477 | 0 | 0.0 | 0 | 0.0 |
| 18h | 478 | 0.0233 | pós-encerramento | 402 | 84.1004 | 76 | 15.8996 | 0 | 0.0 | 0 | 0.0 |
| 19h | 41 | 0.002 | pós-encerramento | 29 | 70.7317 | 12 | 29.2683 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
