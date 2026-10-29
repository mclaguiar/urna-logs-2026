# Curva horária — PI 1º turno

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

- Habilitações no dia: **2,242,127**
  - **1,244** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **1,090** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **154** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **2,166,674** (96.6348%)
- Pós-encerramento ≥17h: **75,453** (% entre oficial+pós: **3.3652**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **10,225** · urnas: **10,267**
- Pico (hora local): **11h** (262,536)
- Faixas ≥17h (ref. brasilia): 17–18h **2.657** · 18–19h **0.587** · 19h+ **0.1212**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **2,242,127**
- Votos computados no log (`O voto do eleitor foi computado`): **2,240,883**
- Votos de presidente no BU: **2,240,883**
  - nominais **2,146,446** · brancos **28,329** · nulos **66,108**

**+1,244** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**2,240,883** = **2,240,883**). O +1,244 está fora dessa conta.
- **1,090** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **154** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **2,002,310** (89.3% do dia)
- Manual: **239,734** (10.69% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **83** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 215,413 | 9.6075 | oficial | 187,094 | 86.8536 | 28,308 | 13.1413 | 0 | 0.0 | 11 | 0.0051 |
| 09h | 244,246 | 10.8935 | oficial | 214,329 | 87.7513 | 29,910 | 12.2459 | 0 | 0.0 | 7 | 0.0029 |
| 10h | 259,338 | 11.5666 | oficial | 230,453 | 88.862 | 28,874 | 11.1337 | 0 | 0.0 | 11 | 0.0042 |
| 11h | 262,536 | 11.7092 | oficial | 235,832 | 89.8284 | 26,696 | 10.1685 | 0 | 0.0 | 8 | 0.003 |
| 12h | 253,138 | 11.2901 | oficial | 228,083 | 90.1022 | 25,047 | 9.8946 | 0 | 0.0 | 8 | 0.0032 |
| 13h | 243,974 | 10.8814 | oficial | 219,508 | 89.9719 | 24,454 | 10.0232 | 0 | 0.0 | 12 | 0.0049 |
| 14h | 237,075 | 10.5737 | oficial | 212,996 | 89.8433 | 24,069 | 10.1525 | 0 | 0.0 | 10 | 0.0042 |
| 15h | 235,515 | 10.5041 | oficial | 211,246 | 89.6953 | 24,265 | 10.303 | 0 | 0.0 | 4 | 0.0017 |
| 16h | 215,439 | 9.6087 | oficial | 194,260 | 90.1694 | 21,170 | 9.8264 | 0 | 0.0 | 9 | 0.0042 |
| 17h | 59,574 | 2.657 | pós-encerramento | 54,150 | 90.8954 | 5,422 | 9.1013 | 0 | 0.0 | 2 | 0.0034 |
| 18h | 13,162 | 0.587 | pós-encerramento | 11,964 | 90.898 | 1,197 | 9.0944 | 0 | 0.0 | 1 | 0.0076 |
| 19h | 2,348 | 0.1047 | pós-encerramento | 2,082 | 88.6712 | 266 | 11.3288 | 0 | 0.0 | 0 | 0.0 |
| 20h | 324 | 0.0145 | pós-encerramento | 279 | 86.1111 | 45 | 13.8889 | 0 | 0.0 | 0 | 0.0 |
| 21h | 45 | 0.002 | pós-encerramento | 34 | 75.5556 | 11 | 24.4444 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
