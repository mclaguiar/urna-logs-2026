# Curva horária — PR 1º turno

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

- Habilitações no dia: **6,844,534**
  - **3,077** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **2,468** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **609** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **6,802,196** (99.3814%)
- Pós-encerramento ≥17h: **42,338** (% entre oficial+pós: **0.6186**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **27,142** · urnas: **27,334**
- Pico (hora local): **12h** (876,713)
- Faixas ≥17h (ref. brasilia): 17–18h **0.5769** · 18–19h **0.0386** · 19h+ **0.0031**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **6,844,534**
- Votos computados no log (`O voto do eleitor foi computado`): **6,841,643**
- Votos de presidente no BU: **6,841,457**
  - nominais **6,585,511** · brancos **122,499** · nulos **133,447**

**+3,077** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**6,841,643**) e votos do BU (**6,841,457**) diferem em **+186**.
- **2,468** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **609** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **6,286,049** (91.84% do dia)
- Manual: **558,254** (8.16% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **231** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 601,135 | 8.7827 | oficial | 539,883 | 89.8106 | 61,212 | 10.1827 | 0 | 0.0 | 40 | 0.0067 |
| 09h | 692,776 | 10.1216 | oficial | 623,671 | 90.0249 | 69,089 | 9.9728 | 0 | 0.0 | 16 | 0.0023 |
| 10h | 814,418 | 11.8988 | oficial | 739,170 | 90.7605 | 75,230 | 9.2373 | 0 | 0.0 | 18 | 0.0022 |
| 11h | 875,992 | 12.7984 | oficial | 805,542 | 91.9577 | 70,417 | 8.0385 | 0 | 0.0 | 33 | 0.0038 |
| 12h | 876,713 | 12.809 | oficial | 812,665 | 92.6945 | 64,018 | 7.302 | 0 | 0.0 | 30 | 0.0034 |
| 13h | 836,233 | 12.2175 | oficial | 774,597 | 92.6293 | 61,616 | 7.3683 | 0 | 0.0 | 20 | 0.0024 |
| 14h | 810,543 | 11.8422 | oficial | 749,674 | 92.4903 | 60,842 | 7.5063 | 0 | 0.0 | 27 | 0.0033 |
| 15h | 745,005 | 10.8847 | oficial | 690,718 | 92.7132 | 54,266 | 7.284 | 0 | 0.0 | 21 | 0.0028 |
| 16h | 549,381 | 8.0266 | oficial | 511,025 | 93.0183 | 38,330 | 6.9769 | 0 | 0.0 | 26 | 0.0047 |
| 17h | 39,483 | 0.5769 | pós-encerramento | 36,457 | 92.3359 | 3,026 | 7.6641 | 0 | 0.0 | 0 | 0.0 |
| 18h | 2,642 | 0.0386 | pós-encerramento | 2,443 | 92.4678 | 199 | 7.5322 | 0 | 0.0 | 0 | 0.0 |
| 19h | 199 | 0.0029 | pós-encerramento | 190 | 95.4774 | 9 | 4.5226 | 0 | 0.0 | 0 | 0.0 |
| 20h | 14 | 0.0002 | pós-encerramento | 14 | 100.0 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
