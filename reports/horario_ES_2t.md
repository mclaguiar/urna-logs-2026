# Curva horária — ES 2º turno

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

- Habilitações no dia: **2,409,653**
  - **439** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **107** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **332** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **2,409,428** (99.9907%)
- Pós-encerramento ≥17h: **225** (% entre oficial+pós: **0.0093**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **9,844** · urnas: **9,947**
- Pico (hora local): **8h** (408,931)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0093** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **2,345,081** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **2,409,653**
- Votos computados no log (`O voto do eleitor foi computado`): **2,409,518**
- Votos de presidente no BU: **2,409,214**
  - nominais **2,296,469** · brancos **33,080** · nulos **79,665**

**+439** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**2,409,518**) e votos do BU (**2,409,214**) diferem em **+304**.
- **107** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **332** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **1,750,030** (72.63% do dia)
- Manual: **659,548** (27.37% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **75** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 408,931 | 16.9705 | oficial | 296,413 | 72.4848 | 112,505 | 27.512 | 0 | 0.0 | 13 | 0.0032 |
| 09h | 378,442 | 15.7052 | oficial | 274,748 | 72.5998 | 103,684 | 27.3976 | 0 | 0.0 | 10 | 0.0026 |
| 10h | 363,095 | 15.0684 | oficial | 264,236 | 72.7732 | 98,852 | 27.2248 | 0 | 0.0 | 7 | 0.0019 |
| 11h | 299,094 | 12.4123 | oficial | 218,263 | 72.9747 | 80,821 | 27.0219 | 0 | 0.0 | 10 | 0.0033 |
| 12h | 238,327 | 9.8905 | oficial | 174,026 | 73.0198 | 64,294 | 26.9772 | 0 | 0.0 | 7 | 0.0029 |
| 13h | 213,924 | 8.8778 | oficial | 155,517 | 72.6973 | 58,397 | 27.298 | 0 | 0.0 | 10 | 0.0047 |
| 14h | 208,342 | 8.6461 | oficial | 150,414 | 72.1957 | 57,922 | 27.8014 | 0 | 0.0 | 6 | 0.0029 |
| 15h | 188,019 | 7.8027 | oficial | 135,543 | 72.0901 | 52,467 | 27.9052 | 0 | 0.0 | 9 | 0.0048 |
| 16h | 111,254 | 4.617 | oficial | 80,715 | 72.5502 | 30,536 | 27.4471 | 0 | 0.0 | 3 | 0.0027 |
| 17h | 225 | 0.0093 | pós-encerramento | 155 | 68.8889 | 70 | 31.1111 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 2,345,081 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
