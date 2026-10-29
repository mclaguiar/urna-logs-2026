# Curva horária — CE 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério: janela **8h–17h Brasília**; ≥17h = pós-encerramento (fila).

Métricas deste relatório = **somente o dia oficial deste turno**.
Janelas no dia: **oficial** [8h,17h) · **pós-encerramento** ≥17h · **fora do previsto** &lt;8h.
Eventos de **outra data** no `.jez` = histórico (não entram nos totais nem no comparativo 1º×2º).
Dia oficial deste turno: **2026-10-04**.

## Resumo (só o dia do turno)

- Habilitações no dia: **5,913,837**
  - **3,366** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **3,047** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **319** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **5,559,606** (94.0101%)
- Pós-encerramento ≥17h: **354,231** (% entre oficial+pós: **5.9899**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **23,765** · urnas: **23,866**
- Pico (hora local): **11h** (658,718)
- Faixas ≥17h (ref. brasilia): 17–18h **4.6666** · 18–19h **1.1164** · 19h+ **0.2069**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **5,913,837**
- Votos computados no log (`O voto do eleitor foi computado`): **5,910,471**
- Votos de presidente no BU: **5,910,471**
  - nominais **5,617,991** · brancos **103,295** · nulos **189,185**

**+3,366** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**5,910,471** = **5,910,471**). O +3,366 está fora dessa conta.
- **3,047** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **319** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **5,268,586** (89.09% do dia)
- Manual: **645,067** (10.91% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **184** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 524,609 | 8.8709 | oficial | 459,345 | 87.5595 | 65,236 | 12.4352 | 0 | 0.0 | 28 | 0.0053 |
| 09h | 589,166 | 9.9625 | oficial | 519,098 | 88.1073 | 70,053 | 11.8902 | 0 | 0.0 | 15 | 0.0025 |
| 10h | 632,718 | 10.6989 | oficial | 562,211 | 88.8565 | 70,490 | 11.1408 | 0 | 0.0 | 17 | 0.0027 |
| 11h | 658,718 | 11.1386 | oficial | 589,816 | 89.54 | 68,882 | 10.457 | 0 | 0.0 | 20 | 0.003 |
| 12h | 651,026 | 11.0085 | oficial | 583,502 | 89.6281 | 67,499 | 10.3681 | 0 | 0.0 | 25 | 0.0038 |
| 13h | 634,154 | 10.7232 | oficial | 567,868 | 89.5473 | 66,270 | 10.4501 | 0 | 0.0 | 16 | 0.0025 |
| 14h | 623,316 | 10.54 | oficial | 556,255 | 89.2413 | 67,045 | 10.7562 | 0 | 0.0 | 16 | 0.0026 |
| 15h | 628,650 | 10.6302 | oficial | 560,123 | 89.0993 | 68,509 | 10.8978 | 0 | 0.0 | 18 | 0.0029 |
| 16h | 617,249 | 10.4374 | oficial | 552,161 | 89.4551 | 65,068 | 10.5416 | 0 | 0.0 | 20 | 0.0032 |
| 17h | 275,978 | 4.6666 | pós-encerramento | 248,408 | 90.0101 | 27,564 | 9.9878 | 0 | 0.0 | 6 | 0.0022 |
| 18h | 66,020 | 1.1164 | pós-encerramento | 59,042 | 89.4305 | 6,976 | 10.5665 | 0 | 0.0 | 2 | 0.003 |
| 19h | 10,437 | 0.1765 | pós-encerramento | 9,181 | 87.9659 | 1,255 | 12.0245 | 0 | 0.0 | 1 | 0.0096 |
| 20h | 1,515 | 0.0256 | pós-encerramento | 1,332 | 87.9208 | 183 | 12.0792 | 0 | 0.0 | 0 | 0.0 |
| 21h | 280 | 0.0047 | pós-encerramento | 243 | 86.7857 | 37 | 13.2143 | 0 | 0.0 | 0 | 0.0 |
| 22h | 1 | 0.0 | pós-encerramento | 1 | 100.0 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
