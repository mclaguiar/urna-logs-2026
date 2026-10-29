# Curva horária — ES 1º turno

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

- Habilitações no dia: **2,353,067**
  - **785** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **696** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **89** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **2,322,818** (98.7145%)
- Pós-encerramento ≥17h: **30,249** (% entre oficial+pós: **1.2855**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **9,844** · urnas: **9,878**
- Pico (hora local): **11h** (292,468)
- Faixas ≥17h (ref. brasilia): 17–18h **1.2081** · 18–19h **0.0743** · 19h+ **0.0031**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **2,353,067**
- Votos computados no log (`O voto do eleitor foi computado`): **2,352,281**
- Votos de presidente no BU: **2,352,282**
  - nominais **2,251,199** · brancos **43,211** · nulos **57,872**

**+785** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**2,352,281**) e votos do BU (**2,352,282**) diferem em **-1**.
- **696** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **89** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **1,709,559** (72.65% do dia)
- Manual: **643,456** (27.35% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **52** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 234,285 | 9.9566 | oficial | 168,337 | 71.8514 | 65,942 | 28.1461 | 0 | 0.0 | 6 | 0.0026 |
| 09h | 266,241 | 11.3146 | oficial | 192,690 | 72.3743 | 73,545 | 27.6235 | 0 | 0.0 | 6 | 0.0023 |
| 10h | 284,991 | 12.1115 | oficial | 208,485 | 73.1549 | 76,502 | 26.8437 | 0 | 0.0 | 4 | 0.0014 |
| 11h | 292,468 | 12.4292 | oficial | 215,343 | 73.6296 | 77,120 | 26.3687 | 0 | 0.0 | 5 | 0.0017 |
| 12h | 281,006 | 11.9421 | oficial | 206,834 | 73.6048 | 74,168 | 26.3937 | 0 | 0.0 | 4 | 0.0014 |
| 13h | 265,641 | 11.2891 | oficial | 194,521 | 73.227 | 71,113 | 26.7703 | 0 | 0.0 | 7 | 0.0026 |
| 14h | 257,895 | 10.96 | oficial | 187,686 | 72.7761 | 70,201 | 27.2208 | 0 | 0.0 | 8 | 0.0031 |
| 15h | 242,652 | 10.3122 | oficial | 175,204 | 72.2038 | 67,444 | 27.7945 | 0 | 0.0 | 4 | 0.0016 |
| 16h | 197,639 | 8.3992 | oficial | 140,704 | 71.1924 | 56,928 | 28.804 | 0 | 0.0 | 7 | 0.0035 |
| 17h | 28,427 | 1.2081 | pós-encerramento | 18,627 | 65.5257 | 9,799 | 34.4707 | 0 | 0.0 | 1 | 0.0035 |
| 18h | 1,748 | 0.0743 | pós-encerramento | 1,092 | 62.4714 | 656 | 37.5286 | 0 | 0.0 | 0 | 0.0 |
| 19h | 74 | 0.0031 | pós-encerramento | 36 | 48.6486 | 38 | 51.3514 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
