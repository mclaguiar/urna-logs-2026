# Curva horária — PR 2º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério: janela **8h–17h Brasília**; ≥17h = pós-encerramento (fila).

Métricas deste relatório = **somente o dia oficial deste turno**.
Janelas no dia: **oficial** [8h,17h) · **pós-encerramento** ≥17h · **fora do previsto** &lt;8h.
Eventos de **outra data** no `.jez` = histórico (não entram nos totais nem no comparativo 1º×2º).
Dia oficial deste turno: **2026-10-25**.

## Resumo (só o dia do turno)

- Habilitações no dia: **7,059,855**
  - **516** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **447** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **69** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **7,059,065** (99.9888%)
- Pós-encerramento ≥17h: **790** (% entre oficial+pós: **0.0112**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **27,142** · urnas: **27,527**
- Pico (hora local): **8h** (1,142,359)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0112** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **6,830,043** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **7,059,855**
- Votos computados no log (`O voto do eleitor foi computado`): **7,059,339**
- Votos de presidente no BU: **7,059,339**
  - nominais **6,857,948** · brancos **82,572** · nulos **118,819**

**+516** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**7,059,339** = **7,059,339**). O +516 está fora dessa conta.
- **447** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **69** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **6,517,119** (92.31% do dia)
- Manual: **542,488** (7.68% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **248** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 1,142,359 | 16.1811 | oficial | 1,039,507 | 90.9965 | 102,802 | 8.9991 | 0 | 0.0 | 50 | 0.0044 |
| 09h | 1,110,632 | 15.7317 | oficial | 1,016,881 | 91.5588 | 93,714 | 8.4379 | 0 | 0.0 | 37 | 0.0033 |
| 10h | 1,109,350 | 15.7135 | oficial | 1,025,234 | 92.4175 | 84,078 | 7.579 | 0 | 0.0 | 38 | 0.0034 |
| 11h | 940,439 | 13.3209 | oficial | 876,621 | 93.214 | 63,788 | 6.7828 | 0 | 0.0 | 30 | 0.0032 |
| 12h | 678,791 | 9.6148 | oficial | 632,886 | 93.2372 | 45,885 | 6.7598 | 0 | 0.0 | 20 | 0.0029 |
| 13h | 613,792 | 8.6941 | oficial | 568,230 | 92.577 | 45,542 | 7.4198 | 0 | 0.0 | 20 | 0.0033 |
| 14h | 620,756 | 8.7928 | oficial | 573,793 | 92.4345 | 46,939 | 7.5616 | 0 | 0.0 | 24 | 0.0039 |
| 15h | 516,618 | 7.3177 | oficial | 479,177 | 92.7527 | 37,419 | 7.2431 | 0 | 0.0 | 22 | 0.0043 |
| 16h | 326,328 | 4.6223 | oficial | 304,087 | 93.1845 | 22,234 | 6.8134 | 0 | 0.0 | 7 | 0.0021 |
| 17h | 790 | 0.0112 | pós-encerramento | 703 | 88.9873 | 87 | 11.0127 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 6,830,043 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
