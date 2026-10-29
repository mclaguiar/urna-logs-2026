# Curva horária — GO 2º turno

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

- Habilitações no dia: **4,047,597**
  - **317** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **275** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **42** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **4,046,945** (99.9839%)
- Pós-encerramento ≥17h: **652** (% entre oficial+pós: **0.0161**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **15,686** · urnas: **15,840**
- Pico (hora local): **8h** (754,347)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0161** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **3,965,818** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **4,047,597**
- Votos computados no log (`O voto do eleitor foi computado`): **4,047,280**
- Votos de presidente no BU: **4,047,280**
  - nominais **3,930,889** · brancos **43,214** · nulos **73,177**

**+317** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**4,047,280** = **4,047,280**). O +317 está fora dessa conta.
- **275** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **42** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **3,598,476** (88.9% do dia)
- Manual: **448,984** (11.09% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **137** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 754,347 | 18.6369 | oficial | 669,727 | 88.7824 | 84,594 | 11.2142 | 0 | 0.0 | 26 | 0.0034 |
| 09h | 660,099 | 16.3084 | oficial | 588,244 | 89.1145 | 71,832 | 10.882 | 0 | 0.0 | 23 | 0.0035 |
| 10h | 613,481 | 15.1567 | oficial | 548,593 | 89.423 | 64,870 | 10.5741 | 0 | 0.0 | 18 | 0.0029 |
| 11h | 496,103 | 12.2567 | oficial | 444,044 | 89.5064 | 52,047 | 10.4912 | 0 | 0.0 | 12 | 0.0024 |
| 12h | 369,685 | 9.1334 | oficial | 329,065 | 89.0123 | 40,606 | 10.9839 | 0 | 0.0 | 14 | 0.0038 |
| 13h | 325,118 | 8.0324 | oficial | 287,307 | 88.3701 | 37,801 | 11.6269 | 0 | 0.0 | 10 | 0.0031 |
| 14h | 321,370 | 7.9398 | oficial | 283,394 | 88.1831 | 37,966 | 11.8138 | 0 | 0.0 | 10 | 0.0031 |
| 15h | 298,445 | 7.3734 | oficial | 263,698 | 88.3573 | 34,729 | 11.6366 | 0 | 0.0 | 18 | 0.006 |
| 16h | 208,297 | 5.1462 | oficial | 183,861 | 88.2687 | 24,430 | 11.7284 | 0 | 0.0 | 6 | 0.0029 |
| 17h | 652 | 0.0161 | pós-encerramento | 543 | 83.2822 | 109 | 16.7178 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 3,965,818 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
