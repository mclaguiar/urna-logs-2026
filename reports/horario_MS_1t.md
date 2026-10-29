# Curva horária — MS 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-4).
Critério: janela **8h–17h Brasília** (local +1h → BRT); ≥17h = pós-encerramento (fila).

Métricas deste relatório = **somente o dia oficial deste turno**.
Janelas no dia: **oficial** [8h,17h) · **pós-encerramento** ≥17h · **fora do previsto** &lt;8h.
Eventos de **outra data** no `.jez` = histórico (não entram nos totais nem no comparativo 1º×2º).
Dia oficial deste turno: **2026-10-04**.

## Resumo (só o dia do turno)

- Habilitações no dia: **1,541,987**
  - **767** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **705** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **62** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **1,525,134** (98.9071%)
- Pós-encerramento ≥17h: **16,853** (% entre oficial+pós: **1.0929**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **7,106** · urnas: **7,129**
- Pico (hora local): **10h** (199,965)
- Faixas ≥17h (ref. brasilia): 17–18h **1.0267** · 18–19h **0.0624** · 19h+ **0.0038**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **1,541,987**
- Votos computados no log (`O voto do eleitor foi computado`): **1,541,220**
- Votos de presidente no BU: **1,541,220**
  - nominais **1,490,354** · brancos **21,270** · nulos **29,596**

**+767** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**1,541,220** = **1,541,220**). O +767 está fora dessa conta.
- **705** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **62** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **1,358,122** (88.08% do dia)
- Manual: **183,821** (11.92% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **44** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 07h | 131,293 | 8.5145 | oficial | 115,083 | 87.6536 | 16,202 | 12.3403 | 0 | 0.0 | 8 | 0.0061 |
| 08h | 143,252 | 9.2901 | oficial | 124,824 | 87.136 | 18,425 | 12.8619 | 0 | 0.0 | 3 | 0.0021 |
| 09h | 179,086 | 11.614 | oficial | 156,275 | 87.2625 | 22,804 | 12.7335 | 0 | 0.0 | 7 | 0.0039 |
| 10h | 199,965 | 12.968 | oficial | 176,852 | 88.4415 | 23,110 | 11.557 | 0 | 0.0 | 3 | 0.0015 |
| 11h | 198,439 | 12.869 | oficial | 176,853 | 89.1221 | 21,580 | 10.8749 | 0 | 0.0 | 6 | 0.003 |
| 12h | 184,074 | 11.9375 | oficial | 163,550 | 88.8501 | 20,520 | 11.1477 | 0 | 0.0 | 4 | 0.0022 |
| 13h | 171,378 | 11.1141 | oficial | 151,455 | 88.3748 | 19,919 | 11.6228 | 0 | 0.0 | 4 | 0.0023 |
| 14h | 170,228 | 11.0395 | oficial | 149,374 | 87.7494 | 20,850 | 12.2483 | 0 | 0.0 | 4 | 0.0023 |
| 15h | 147,419 | 9.5603 | oficial | 129,641 | 87.9405 | 17,773 | 12.0561 | 0 | 0.0 | 5 | 0.0034 |
| 16h | 15,832 | 1.0267 | pós-encerramento | 13,422 | 84.7777 | 2,410 | 15.2223 | 0 | 0.0 | 0 | 0.0 |
| 17h | 962 | 0.0624 | pós-encerramento | 759 | 78.8981 | 203 | 21.1019 | 0 | 0.0 | 0 | 0.0 |
| 18h | 59 | 0.0038 | pós-encerramento | 34 | 57.6271 | 25 | 42.3729 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
