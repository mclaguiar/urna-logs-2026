# Curva horária — PA 1º turno

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

- Habilitações no dia: **5,069,004**
  - **2,500** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **2,072** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **428** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **4,785,315** (94.4035%)
- Pós-encerramento ≥17h: **283,689** (% entre oficial+pós: **5.5965**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **20,827** · urnas: **20,892**
- Pico (hora local): **11h** (573,435)
- Faixas ≥17h (ref. brasilia): 17–18h **4.311** · 18–19h **1.0574** · 19h+ **0.2282**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **5,069,004**
- Votos computados no log (`O voto do eleitor foi computado`): **5,066,642**
- Votos de presidente no BU: **5,066,504**
  - nominais **4,863,355** · brancos **54,203** · nulos **148,946**

**+2,500** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**5,066,642**) e votos do BU (**5,066,504**) diferem em **+138**.
- **2,072** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **428** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **4,589,770** (90.55% do dia)
- Manual: **479,092** (9.45% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **142** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 449,992 | 8.8773 | oficial | 403,817 | 89.7387 | 46,151 | 10.256 | 0 | 0.0 | 24 | 0.0053 |
| 09h | 517,219 | 10.2036 | oficial | 465,646 | 90.0288 | 51,565 | 9.9697 | 0 | 0.0 | 8 | 0.0015 |
| 10h | 554,340 | 10.9359 | oficial | 502,102 | 90.5765 | 52,231 | 9.4222 | 0 | 0.0 | 7 | 0.0013 |
| 11h | 573,435 | 11.3126 | oficial | 521,324 | 90.9125 | 52,093 | 9.0844 | 0 | 0.0 | 18 | 0.0031 |
| 12h | 554,357 | 10.9362 | oficial | 504,114 | 90.9367 | 50,233 | 9.0615 | 0 | 0.0 | 10 | 0.0018 |
| 13h | 541,643 | 10.6854 | oficial | 491,883 | 90.8131 | 49,745 | 9.1841 | 0 | 0.0 | 15 | 0.0028 |
| 14h | 540,446 | 10.6618 | oficial | 489,844 | 90.637 | 50,592 | 9.3612 | 0 | 0.0 | 10 | 0.0019 |
| 15h | 535,862 | 10.5713 | oficial | 485,182 | 90.5423 | 50,661 | 9.4541 | 0 | 0.0 | 19 | 0.0035 |
| 16h | 518,021 | 10.2194 | oficial | 468,954 | 90.528 | 49,048 | 9.4683 | 0 | 0.0 | 19 | 0.0037 |
| 17h | 218,524 | 4.311 | pós-encerramento | 198,006 | 90.6106 | 20,511 | 9.3862 | 0 | 0.0 | 7 | 0.0032 |
| 18h | 53,599 | 1.0574 | pós-encerramento | 48,426 | 90.3487 | 5,168 | 9.642 | 0 | 0.0 | 5 | 0.0093 |
| 19h | 10,037 | 0.198 | pós-encerramento | 9,100 | 90.6645 | 937 | 9.3355 | 0 | 0.0 | 0 | 0.0 |
| 20h | 1,373 | 0.0271 | pós-encerramento | 1,238 | 90.1675 | 135 | 9.8325 | 0 | 0.0 | 0 | 0.0 |
| 21h | 136 | 0.0027 | pós-encerramento | 116 | 85.2941 | 20 | 14.7059 | 0 | 0.0 | 0 | 0.0 |
| 22h | 20 | 0.0004 | pós-encerramento | 18 | 90.0 | 2 | 10.0 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
