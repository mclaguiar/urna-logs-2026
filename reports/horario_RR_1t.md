# Curva horária — RR 1º turno

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

- Habilitações no dia: **333,054**
  - **282** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **264** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **18** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **329,901** (99.0533%)
- Pós-encerramento ≥17h: **3,153** (% entre oficial+pós: **0.9467**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **1,519** · urnas: **1,522**
- Pico (hora local): **10h** (44,781)
- Faixas ≥17h (ref. brasilia): 17–18h **0.8068** · 18–19h **0.1033** · 19h+ **0.0366**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **333,054**
- Votos computados no log (`O voto do eleitor foi computado`): **332,772**
- Votos de presidente no BU: **332,772**
  - nominais **325,559** · brancos **2,618** · nulos **4,595**

**+282** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**332,772** = **332,772**). O +282 está fora dessa conta.
- **264** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **18** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **310,026** (93.09% do dia)
- Manual: **23,023** (6.91% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **5** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 07h | 30,665 | 9.2072 | oficial | 28,514 | 92.9855 | 2,150 | 7.0113 | 0 | 0.0 | 1 | 0.0033 |
| 08h | 36,824 | 11.0565 | oficial | 34,078 | 92.5429 | 2,745 | 7.4544 | 0 | 0.0 | 1 | 0.0027 |
| 09h | 42,157 | 12.6577 | oficial | 39,066 | 92.6679 | 3,090 | 7.3297 | 0 | 0.0 | 1 | 0.0024 |
| 10h | 44,781 | 13.4456 | oficial | 41,726 | 93.1779 | 3,055 | 6.8221 | 0 | 0.0 | 0 | 0.0 |
| 11h | 42,862 | 12.8694 | oficial | 40,029 | 93.3904 | 2,833 | 6.6096 | 0 | 0.0 | 0 | 0.0 |
| 12h | 36,255 | 10.8856 | oficial | 33,947 | 93.634 | 2,308 | 6.366 | 0 | 0.0 | 0 | 0.0 |
| 13h | 32,132 | 9.6477 | oficial | 29,954 | 93.2217 | 2,178 | 6.7783 | 0 | 0.0 | 0 | 0.0 |
| 14h | 33,004 | 9.9095 | oficial | 30,722 | 93.0857 | 2,281 | 6.9113 | 0 | 0.0 | 1 | 0.003 |
| 15h | 31,221 | 9.3742 | oficial | 29,035 | 92.9983 | 2,185 | 6.9985 | 0 | 0.0 | 1 | 0.0032 |
| 16h | 2,687 | 0.8068 | pós-encerramento | 2,511 | 93.4499 | 176 | 6.5501 | 0 | 0.0 | 0 | 0.0 |
| 17h | 344 | 0.1033 | pós-encerramento | 326 | 94.7674 | 18 | 5.2326 | 0 | 0.0 | 0 | 0.0 |
| 18h | 118 | 0.0354 | pós-encerramento | 114 | 96.6102 | 4 | 3.3898 | 0 | 0.0 | 0 | 0.0 |
| 19h | 4 | 0.0012 | pós-encerramento | 4 | 100.0 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
