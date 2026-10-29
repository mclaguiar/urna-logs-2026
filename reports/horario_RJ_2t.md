# Curva horária — RJ 2º turno

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

- Habilitações no dia: **10,078,145**
  - **696** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **594** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **102** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **10,074,262** (99.9615%)
- Pós-encerramento ≥17h: **3,883** (% entre oficial+pós: **0.0385**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **37,675** · urnas: **38,161**
- Pico (hora local): **10h** (1,480,624)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0298** · 18–19h **0.0087** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **9,855,192** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **10,078,145**
- Votos computados no log (`O voto do eleitor foi computado`): **10,077,449**
- Votos de presidente no BU: **10,077,449**
  - nominais **9,734,426** · brancos **111,682** · nulos **231,341**

**+696** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**10,077,449** = **10,077,449**). O +696 está fora dessa conta.
- **594** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **102** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **8,599,393** (85.33% do dia)
- Manual: **1,478,371** (14.67% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **381** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 1,457,274 | 14.4597 | oficial | 1,224,941 | 84.057 | 232,252 | 15.9374 | 0 | 0.0 | 81 | 0.0056 |
| 09h | 1,348,857 | 13.384 | oficial | 1,134,476 | 84.1065 | 214,338 | 15.8903 | 0 | 0.0 | 43 | 0.0032 |
| 10h | 1,480,624 | 14.6914 | oficial | 1,253,644 | 84.67 | 226,926 | 15.3264 | 0 | 0.0 | 54 | 0.0036 |
| 11h | 1,449,928 | 14.3869 | oficial | 1,240,557 | 85.5599 | 209,323 | 14.4368 | 0 | 0.0 | 48 | 0.0033 |
| 12h | 1,226,121 | 12.1661 | oficial | 1,056,407 | 86.1585 | 169,671 | 13.838 | 0 | 0.0 | 43 | 0.0035 |
| 13h | 1,009,699 | 10.0187 | oficial | 872,304 | 86.3925 | 137,360 | 13.6041 | 0 | 0.0 | 35 | 0.0035 |
| 14h | 887,412 | 8.8053 | oficial | 764,606 | 86.1613 | 122,771 | 13.8347 | 0 | 0.0 | 35 | 0.0039 |
| 15h | 748,990 | 7.4318 | oficial | 645,915 | 86.2381 | 103,053 | 13.7589 | 0 | 0.0 | 22 | 0.0029 |
| 16h | 465,357 | 4.6175 | oficial | 403,232 | 86.65 | 62,105 | 13.3457 | 0 | 0.0 | 20 | 0.0043 |
| 17h | 3,008 | 0.0298 | pós-encerramento | 2,541 | 84.4747 | 467 | 15.5253 | 0 | 0.0 | 0 | 0.0 |
| 18h | 872 | 0.0087 | pós-encerramento | 768 | 88.0734 | 104 | 11.9266 | 0 | 0.0 | 0 | 0.0 |
| 19h | 3 | 0.0 | pós-encerramento | 2 | 66.6667 | 1 | 33.3333 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-09-24 | 1 |
| 2026-10-04 | 9,855,191 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
