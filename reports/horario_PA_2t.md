# Curva horária — PA 2º turno

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

- Habilitações no dia: **4,989,944**
  - **371** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **319** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **52** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **4,988,768** (99.9764%)
- Pós-encerramento ≥17h: **1,176** (% entre oficial+pós: **0.0236**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **20,827** · urnas: **21,018**
- Pico (hora local): **8h** (1,001,592)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0235** · 18–19h **0.0001** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **5,060,330** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **4,989,944**
- Votos computados no log (`O voto do eleitor foi computado`): **4,989,573**
- Votos de presidente no BU: **4,989,573**
  - nominais **4,890,389** · brancos **36,501** · nulos **62,683**

**+371** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**4,989,573** = **4,989,573**). O +371 está fora dessa conta.
- **319** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **52** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **4,513,130** (90.44% do dia)
- Manual: **476,621** (9.55% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **193** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 1,001,592 | 20.0722 | oficial | 907,789 | 90.6346 | 93,755 | 9.3606 | 0 | 0.0 | 48 | 0.0048 |
| 09h | 883,341 | 17.7024 | oficial | 800,575 | 90.6303 | 82,741 | 9.3668 | 0 | 0.0 | 25 | 0.0028 |
| 10h | 753,931 | 15.109 | oficial | 683,099 | 90.605 | 70,797 | 9.3904 | 0 | 0.0 | 35 | 0.0046 |
| 11h | 546,300 | 10.948 | oficial | 494,449 | 90.5087 | 51,829 | 9.4873 | 0 | 0.0 | 22 | 0.004 |
| 12h | 396,422 | 7.9444 | oficial | 358,300 | 90.3835 | 38,108 | 9.613 | 0 | 0.0 | 14 | 0.0035 |
| 13h | 376,296 | 7.5411 | oficial | 339,488 | 90.2183 | 36,793 | 9.7777 | 0 | 0.0 | 15 | 0.004 |
| 14h | 384,188 | 7.6992 | oficial | 346,361 | 90.154 | 37,816 | 9.8431 | 0 | 0.0 | 11 | 0.0029 |
| 15h | 372,815 | 7.4713 | oficial | 335,690 | 90.042 | 37,111 | 9.9543 | 0 | 0.0 | 14 | 0.0038 |
| 16h | 273,883 | 5.4887 | oficial | 246,388 | 89.961 | 27,486 | 10.0357 | 0 | 0.0 | 9 | 0.0033 |
| 17h | 1,172 | 0.0235 | pós-encerramento | 988 | 84.3003 | 184 | 15.6997 | 0 | 0.0 | 0 | 0.0 |
| 18h | 4 | 0.0001 | pós-encerramento | 3 | 75.0 | 1 | 25.0 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 5,060,330 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
