# Curva horária — MG 1º turno

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

- Habilitações no dia: **12,640,883**
  - **3,609** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **3,449** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **160** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **12,392,298** (98.0335%)
- Pós-encerramento ≥17h: **248,585** (% entre oficial+pós: **1.9665**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **52,062** · urnas: **52,217**
- Pico (hora local): **11h** (1,555,744)
- Faixas ≥17h (ref. brasilia): 17–18h **1.7087** · 18–19h **0.2308** · 19h+ **0.0269**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **12,640,883**
- Votos computados no log (`O voto do eleitor foi computado`): **12,636,937**
- Votos de presidente no BU: **12,637,274**
  - nominais **11,976,796** · brancos **268,302** · nulos **392,176**

**+3,609** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**12,636,937**) e votos do BU (**12,637,274**) diferem em **-337**.
- **3,449** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **160** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **10,378,646** (82.1% do dia)
- Manual: **2,261,871** (17.89% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **366** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 1,268,878 | 10.0379 | oficial | 1,025,580 | 80.8257 | 243,224 | 19.1684 | 0 | 0.0 | 74 | 0.0058 |
| 09h | 1,427,657 | 11.294 | oficial | 1,162,323 | 81.4147 | 265,301 | 18.583 | 0 | 0.0 | 33 | 0.0023 |
| 10h | 1,509,271 | 11.9396 | oficial | 1,240,514 | 82.1929 | 268,725 | 17.805 | 0 | 0.0 | 32 | 0.0021 |
| 11h | 1,555,744 | 12.3072 | oficial | 1,291,185 | 82.9947 | 264,524 | 17.0031 | 0 | 0.0 | 35 | 0.0022 |
| 12h | 1,517,924 | 12.0081 | oficial | 1,265,839 | 83.3928 | 252,045 | 16.6046 | 0 | 0.0 | 40 | 0.0026 |
| 13h | 1,412,723 | 11.1758 | oficial | 1,170,518 | 82.8555 | 242,153 | 17.1409 | 0 | 0.0 | 52 | 0.0037 |
| 14h | 1,336,974 | 10.5766 | oficial | 1,099,633 | 82.2479 | 237,297 | 17.7488 | 0 | 0.0 | 44 | 0.0033 |
| 15h | 1,263,405 | 9.9946 | oficial | 1,031,204 | 81.621 | 232,172 | 18.3767 | 0 | 0.0 | 29 | 0.0023 |
| 16h | 1,099,722 | 8.6997 | oficial | 891,937 | 81.1057 | 207,766 | 18.8926 | 0 | 0.0 | 19 | 0.0017 |
| 17h | 216,001 | 1.7087 | pós-encerramento | 174,088 | 80.5959 | 41,906 | 19.4008 | 0 | 0.0 | 7 | 0.0032 |
| 18h | 29,181 | 0.2308 | pós-encerramento | 23,170 | 79.401 | 6,010 | 20.5956 | 0 | 0.0 | 1 | 0.0034 |
| 19h | 2,900 | 0.0229 | pós-encerramento | 2,276 | 78.4828 | 624 | 21.5172 | 0 | 0.0 | 0 | 0.0 |
| 20h | 374 | 0.003 | pós-encerramento | 284 | 75.9358 | 90 | 24.0642 | 0 | 0.0 | 0 | 0.0 |
| 21h | 82 | 0.0006 | pós-encerramento | 59 | 71.9512 | 23 | 28.0488 | 0 | 0.0 | 0 | 0.0 |
| 22h | 27 | 0.0002 | pós-encerramento | 22 | 81.4815 | 5 | 18.5185 | 0 | 0.0 | 0 | 0.0 |
| 23h | 20 | 0.0002 | pós-encerramento | 14 | 70.0 | 6 | 30.0 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
