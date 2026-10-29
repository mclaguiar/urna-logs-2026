# Curva horária — AC 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-5).
Critério: janela **8h–17h Brasília** (local +2h → BRT); ≥17h = pós-encerramento (fila).

Métricas deste relatório = **somente o dia oficial deste turno**.
Janelas no dia: **oficial** [8h,17h) · **pós-encerramento** ≥17h · **fora do previsto** &lt;8h.
Eventos de **outra data** no `.jez` = histórico (não entram nos totais nem no comparativo 1º×2º).
Dia oficial deste turno: **2026-10-04**.

## Resumo (só o dia do turno)

- Habilitações no dia: **488,718**
  - **388** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **361** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **27** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **480,751** (98.3698%)
- Pós-encerramento ≥17h: **7,967** (% entre oficial+pós: **1.6302**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **2,270** · urnas: **2,276**
- Pico (hora local): **10h** (61,100)
- Faixas ≥17h (ref. brasilia): 17–18h **1.4264** · 18–19h **0.1819** · 19h+ **0.0219**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **488,718**
- Votos computados no log (`O voto do eleitor foi computado`): **488,330**
- Votos de presidente no BU: **488,330**
  - nominais **469,089** · brancos **5,579** · nulos **13,662**

**+388** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**488,330** = **488,330**). O +388 está fora dessa conta.
- **361** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **27** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **446,418** (91.34% do dia)
- Manual: **42,288** (8.65% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **12** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 06h | 47,246 | 9.6673 | oficial | 43,051 | 91.1209 | 4,194 | 8.8769 | 0 | 0.0 | 1 | 0.0021 |
| 07h | 51,003 | 10.4361 | oficial | 46,417 | 91.0084 | 4,585 | 8.9897 | 0 | 0.0 | 1 | 0.002 |
| 08h | 54,495 | 11.1506 | oficial | 49,618 | 91.0506 | 4,877 | 8.9494 | 0 | 0.0 | 0 | 0.0 |
| 09h | 58,254 | 11.9198 | oficial | 53,098 | 91.1491 | 5,151 | 8.8423 | 0 | 0.0 | 5 | 0.0086 |
| 10h | 61,100 | 12.5021 | oficial | 55,953 | 91.5761 | 5,145 | 8.4206 | 0 | 0.0 | 2 | 0.0033 |
| 11h | 59,912 | 12.259 | oficial | 54,938 | 91.6978 | 4,974 | 8.3022 | 0 | 0.0 | 0 | 0.0 |
| 12h | 55,599 | 11.3765 | oficial | 51,026 | 91.775 | 4,573 | 8.225 | 0 | 0.0 | 0 | 0.0 |
| 13h | 51,566 | 10.5513 | oficial | 47,088 | 91.316 | 4,478 | 8.684 | 0 | 0.0 | 0 | 0.0 |
| 14h | 41,576 | 8.5072 | oficial | 37,996 | 91.3893 | 3,577 | 8.6035 | 0 | 0.0 | 3 | 0.0072 |
| 15h | 6,971 | 1.4264 | pós-encerramento | 6,328 | 90.7761 | 643 | 9.2239 | 0 | 0.0 | 0 | 0.0 |
| 16h | 889 | 0.1819 | pós-encerramento | 806 | 90.6637 | 83 | 9.3363 | 0 | 0.0 | 0 | 0.0 |
| 17h | 107 | 0.0219 | pós-encerramento | 99 | 92.5234 | 8 | 7.4766 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
