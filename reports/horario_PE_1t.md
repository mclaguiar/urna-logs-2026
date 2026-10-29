# Curva horária — PE 1º turno

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

- Habilitações no dia: **5,913,637**
  - **2,575** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **2,344** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **231** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **5,479,939** (92.6661%)
- Pós-encerramento ≥17h: **433,698** (% entre oficial+pós: **7.3339**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **21,418** · urnas: **21,516**
- Pico (hora local): **12h** (644,935)
- Faixas ≥17h (ref. brasilia): 17–18h **5.5007** · 18–19h **1.5581** · 19h+ **0.2751**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **5,913,637**
- Votos computados no log (`O voto do eleitor foi computado`): **5,911,062**
- Votos de presidente no BU: **5,911,062**
  - nominais **5,601,155** · brancos **109,491** · nulos **200,416**

**+2,575** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**5,911,062** = **5,911,062**). O +2,575 está fora dessa conta.
- **2,344** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **231** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **5,090,073** (86.07% do dia)
- Manual: **823,391** (13.92% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **173** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 522,952 | 8.8432 | oficial | 449,470 | 85.9486 | 73,458 | 14.0468 | 0 | 0.0 | 24 | 0.0046 |
| 09h | 571,459 | 9.6634 | oficial | 490,174 | 85.7759 | 81,272 | 14.2218 | 0 | 0.0 | 13 | 0.0023 |
| 10h | 606,851 | 10.2619 | oficial | 522,344 | 86.0745 | 84,491 | 13.9229 | 0 | 0.0 | 16 | 0.0026 |
| 11h | 637,169 | 10.7746 | oficial | 550,249 | 86.3584 | 86,910 | 13.64 | 0 | 0.0 | 10 | 0.0016 |
| 12h | 644,935 | 10.9059 | oficial | 557,586 | 86.4562 | 87,332 | 13.5412 | 0 | 0.0 | 17 | 0.0026 |
| 13h | 630,953 | 10.6695 | oficial | 545,024 | 86.3811 | 85,906 | 13.6153 | 0 | 0.0 | 23 | 0.0036 |
| 14h | 621,120 | 10.5032 | oficial | 534,387 | 86.036 | 86,717 | 13.9614 | 0 | 0.0 | 16 | 0.0026 |
| 15h | 628,339 | 10.6253 | oficial | 538,986 | 85.7795 | 89,338 | 14.2181 | 0 | 0.0 | 15 | 0.0024 |
| 16h | 616,161 | 10.4193 | oficial | 529,366 | 85.9136 | 86,775 | 14.0832 | 0 | 0.0 | 20 | 0.0032 |
| 17h | 325,289 | 5.5007 | pós-encerramento | 279,279 | 85.8557 | 45,997 | 14.1403 | 0 | 0.0 | 13 | 0.004 |
| 18h | 92,139 | 1.5581 | pós-encerramento | 79,340 | 86.109 | 12,793 | 13.8845 | 0 | 0.0 | 6 | 0.0065 |
| 19h | 14,642 | 0.2476 | pós-encerramento | 12,470 | 85.166 | 2,172 | 14.834 | 0 | 0.0 | 0 | 0.0 |
| 20h | 1,465 | 0.0248 | pós-encerramento | 1,252 | 85.4608 | 213 | 14.5392 | 0 | 0.0 | 0 | 0.0 |
| 21h | 162 | 0.0027 | pós-encerramento | 146 | 90.1235 | 16 | 9.8765 | 0 | 0.0 | 0 | 0.0 |
| 22h | 1 | 0.0 | pós-encerramento | 0 | 0.0 | 1 | 100.0 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
