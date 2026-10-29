# Curva horária — SC 1º turno

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

- Habilitações no dia: **4,649,499**
  - **1,340** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **1,182** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **158** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **4,611,259** (99.1775%)
- Pós-encerramento ≥17h: **38,240** (% entre oficial+pós: **0.8225**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **17,326** · urnas: **17,416**
- Pico (hora local): **11h** (574,741)
- Faixas ≥17h (ref. brasilia): 17–18h **0.7864** · 18–19h **0.0337** · 19h+ **0.0024**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **4,649,499**
- Votos computados no log (`O voto do eleitor foi computado`): **4,648,159**
- Votos de presidente no BU: **4,648,159**
  - nominais **4,501,081** · brancos **69,007** · nulos **78,071**

**+1,340** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**4,648,159** = **4,648,159**). O +1,340 está fora dessa conta.
- **1,182** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **158** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **4,058,921** (87.3% do dia)
- Manual: **590,425** (12.7% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **153** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 461,496 | 9.9257 | oficial | 392,775 | 85.1091 | 68,698 | 14.8859 | 0 | 0.0 | 23 | 0.005 |
| 09h | 513,613 | 11.0466 | oficial | 441,015 | 85.8652 | 72,585 | 14.1322 | 0 | 0.0 | 13 | 0.0025 |
| 10h | 557,735 | 11.9956 | oficial | 485,685 | 87.0817 | 72,033 | 12.9153 | 0 | 0.0 | 17 | 0.003 |
| 11h | 574,741 | 12.3614 | oficial | 506,455 | 88.1188 | 68,262 | 11.877 | 0 | 0.0 | 24 | 0.0042 |
| 12h | 556,423 | 11.9674 | oficial | 490,659 | 88.1809 | 65,749 | 11.8164 | 0 | 0.0 | 15 | 0.0027 |
| 13h | 548,879 | 11.8051 | oficial | 482,331 | 87.8757 | 66,529 | 12.1209 | 0 | 0.0 | 19 | 0.0035 |
| 14h | 536,461 | 11.538 | oficial | 470,251 | 87.658 | 66,195 | 12.3392 | 0 | 0.0 | 15 | 0.0028 |
| 15h | 491,235 | 10.5653 | oficial | 431,054 | 87.749 | 60,165 | 12.2477 | 0 | 0.0 | 16 | 0.0033 |
| 16h | 370,676 | 7.9724 | oficial | 325,435 | 87.795 | 45,231 | 12.2023 | 0 | 0.0 | 10 | 0.0027 |
| 17h | 36,562 | 0.7864 | pós-encerramento | 31,815 | 87.0166 | 4,746 | 12.9807 | 0 | 0.0 | 1 | 0.0027 |
| 18h | 1,566 | 0.0337 | pós-encerramento | 1,345 | 85.8876 | 221 | 14.1124 | 0 | 0.0 | 0 | 0.0 |
| 19h | 108 | 0.0023 | pós-encerramento | 98 | 90.7407 | 10 | 9.2593 | 0 | 0.0 | 0 | 0.0 |
| 20h | 4 | 0.0001 | pós-encerramento | 3 | 75.0 | 1 | 25.0 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
