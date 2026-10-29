# Curva horária — AL 1º turno

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

- Habilitações no dia: **1,939,312**
  - **884** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **785** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **99** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **1,763,458** (90.9321%)
- Pós-encerramento ≥17h: **175,854** (% entre oficial+pós: **9.0679**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **7,101** · urnas: **7,151**
- Pico (hora local): **12h** (206,518)
- Faixas ≥17h (ref. brasilia): 17–18h **6.2129** · 18–19h **2.3268** · 19h+ **0.5281**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **1,939,312**
- Votos computados no log (`O voto do eleitor foi computado`): **1,938,428**
- Votos de presidente no BU: **1,938,428**
  - nominais **1,818,929** · brancos **33,712** · nulos **85,787**

**+884** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**1,938,428** = **1,938,428**). O +884 está fora dessa conta.
- **785** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **99** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **1,741,852** (89.82% do dia)
- Manual: **197,391** (10.18% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **69** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 162,870 | 8.3983 | oficial | 144,265 | 88.5768 | 18,592 | 11.4152 | 0 | 0.0 | 13 | 0.008 |
| 09h | 183,379 | 9.4559 | oficial | 162,785 | 88.7697 | 20,587 | 11.2265 | 0 | 0.0 | 7 | 0.0038 |
| 10h | 194,933 | 10.0517 | oficial | 174,010 | 89.2666 | 20,916 | 10.7298 | 0 | 0.0 | 7 | 0.0036 |
| 11h | 204,785 | 10.5597 | oficial | 183,826 | 89.7654 | 20,953 | 10.2317 | 0 | 0.0 | 6 | 0.0029 |
| 12h | 206,518 | 10.649 | oficial | 186,176 | 90.15 | 20,336 | 9.8471 | 0 | 0.0 | 6 | 0.0029 |
| 13h | 203,208 | 10.4784 | oficial | 183,108 | 90.1087 | 20,096 | 9.8894 | 0 | 0.0 | 4 | 0.002 |
| 14h | 202,606 | 10.4473 | oficial | 182,500 | 90.0763 | 20,094 | 9.9178 | 0 | 0.0 | 12 | 0.0059 |
| 15h | 204,903 | 10.5658 | oficial | 184,275 | 89.9328 | 20,623 | 10.0648 | 0 | 0.0 | 5 | 0.0024 |
| 16h | 200,256 | 10.3261 | oficial | 180,820 | 90.2944 | 19,432 | 9.7036 | 0 | 0.0 | 4 | 0.002 |
| 17h | 120,488 | 6.2129 | pós-encerramento | 109,575 | 90.9427 | 10,909 | 9.054 | 0 | 0.0 | 4 | 0.0033 |
| 18h | 45,124 | 2.3268 | pós-encerramento | 41,243 | 91.3993 | 3,881 | 8.6007 | 0 | 0.0 | 0 | 0.0 |
| 19h | 8,917 | 0.4598 | pós-encerramento | 8,099 | 90.8265 | 817 | 9.1623 | 0 | 0.0 | 1 | 0.0112 |
| 20h | 1,207 | 0.0622 | pós-encerramento | 1,080 | 89.478 | 127 | 10.522 | 0 | 0.0 | 0 | 0.0 |
| 21h | 110 | 0.0057 | pós-encerramento | 87 | 79.0909 | 23 | 20.9091 | 0 | 0.0 | 0 | 0.0 |
| 22h | 8 | 0.0004 | pós-encerramento | 3 | 37.5 | 5 | 62.5 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
