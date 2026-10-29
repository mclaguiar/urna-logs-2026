# Curva horária — MS 2º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-4).
Critério: janela **8h–17h Brasília** (local +1h → BRT); ≥17h = pós-encerramento (fila).

Métricas deste relatório = **somente o dia oficial deste turno**.
Janelas no dia: **oficial** [8h,17h) · **pós-encerramento** ≥17h · **fora do previsto** &lt;8h.
Eventos de **outra data** no `.jez` = histórico (não entram nos totais nem no comparativo 1º×2º).
Dia oficial deste turno: **2026-10-25**.

## Resumo (só o dia do turno)

- Habilitações no dia: **1,594,581**
  - **121** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **104** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **17** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **1,594,208** (99.9766%)
- Pós-encerramento ≥17h: **373** (% entre oficial+pós: **0.0234**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **7,106** · urnas: **7,155**
- Pico (hora local): **9h** (264,804)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0234** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **1,530,728** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **1,594,581**
- Votos computados no log (`O voto do eleitor foi computado`): **1,594,460**
- Votos de presidente no BU: **1,594,460**
  - nominais **1,556,865** · brancos **14,958** · nulos **22,637**

**+121** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**1,594,460** = **1,594,460**). O +121 está fora dessa conta.
- **104** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **17** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **1,411,119** (88.49% do dia)
- Manual: **183,413** (11.5% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **49** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 07h | 217,141 | 13.6174 | oficial | 190,672 | 87.8102 | 26,463 | 12.187 | 0 | 0.0 | 6 | 0.0028 |
| 08h | 248,485 | 15.5831 | oficial | 217,823 | 87.6604 | 30,655 | 12.3368 | 0 | 0.0 | 7 | 0.0028 |
| 09h | 264,804 | 16.6065 | oficial | 233,953 | 88.3495 | 30,840 | 11.6463 | 0 | 0.0 | 11 | 0.0042 |
| 10h | 231,355 | 14.5088 | oficial | 206,320 | 89.179 | 25,030 | 10.8189 | 0 | 0.0 | 5 | 0.0022 |
| 11h | 186,844 | 11.7174 | oficial | 167,773 | 89.7931 | 19,063 | 10.2026 | 0 | 0.0 | 8 | 0.0043 |
| 12h | 138,411 | 8.6801 | oficial | 123,652 | 89.3368 | 14,756 | 10.661 | 0 | 0.0 | 3 | 0.0022 |
| 13h | 116,210 | 7.2878 | oficial | 102,517 | 88.217 | 13,691 | 11.7813 | 0 | 0.0 | 2 | 0.0017 |
| 14h | 110,110 | 6.9053 | oficial | 96,795 | 87.9075 | 13,311 | 12.0888 | 0 | 0.0 | 4 | 0.0036 |
| 15h | 80,848 | 5.0702 | oficial | 71,294 | 88.1828 | 9,551 | 11.8135 | 0 | 0.0 | 3 | 0.0037 |
| 16h | 373 | 0.0234 | pós-encerramento | 320 | 85.7909 | 53 | 14.2091 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 1,530,728 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
