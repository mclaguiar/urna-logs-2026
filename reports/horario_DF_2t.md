# Curva horária — DF 2º turno

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

- Habilitações no dia: **1,868,504**
  - **224** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **191** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **33** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **1,867,642** (99.9539%)
- Pós-encerramento ≥17h: **862** (% entre oficial+pós: **0.0461**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **6,969** · urnas: **7,015**
- Pico (hora local): **8h** (301,787)
- Faixas ≥17h (ref. brasilia): 17–18h **0.046** · 18–19h **0.0001** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **1,826,519** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **1,868,504**
- Votos computados no log (`O voto do eleitor foi computado`): **1,868,280**
- Votos de presidente no BU: **1,868,280**
  - nominais **1,804,766** · brancos **22,386** · nulos **41,128**

**+224** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**1,868,280** = **1,868,280**). O +224 está fora dessa conta.
- **191** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **33** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **1,725,093** (92.32% do dia)
- Manual: **143,353** (7.67% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **58** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 301,787 | 16.1513 | oficial | 279,583 | 92.6425 | 22,191 | 7.3532 | 0 | 0.0 | 13 | 0.0043 |
| 09h | 287,043 | 15.3622 | oficial | 264,670 | 92.2057 | 22,367 | 7.7922 | 0 | 0.0 | 6 | 0.0021 |
| 10h | 288,661 | 15.4488 | oficial | 266,335 | 92.2657 | 22,316 | 7.7309 | 0 | 0.0 | 10 | 0.0035 |
| 11h | 250,591 | 13.4113 | oficial | 231,729 | 92.473 | 18,851 | 7.5226 | 0 | 0.0 | 11 | 0.0044 |
| 12h | 196,695 | 10.5269 | oficial | 182,057 | 92.558 | 14,633 | 7.4394 | 0 | 0.0 | 5 | 0.0025 |
| 13h | 159,645 | 8.544 | oficial | 147,220 | 92.2171 | 12,422 | 7.781 | 0 | 0.0 | 3 | 0.0019 |
| 14h | 151,272 | 8.0959 | oficial | 139,351 | 92.1195 | 11,917 | 7.8779 | 0 | 0.0 | 4 | 0.0026 |
| 15h | 139,949 | 7.4899 | oficial | 128,734 | 91.9864 | 11,212 | 8.0115 | 0 | 0.0 | 3 | 0.0021 |
| 16h | 91,999 | 4.9237 | oficial | 84,651 | 92.013 | 7,345 | 7.9838 | 0 | 0.0 | 3 | 0.0033 |
| 17h | 860 | 0.046 | pós-encerramento | 761 | 88.4884 | 99 | 11.5116 | 0 | 0.0 | 0 | 0.0 |
| 18h | 2 | 0.0001 | pós-encerramento | 2 | 100.0 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 1,826,519 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
