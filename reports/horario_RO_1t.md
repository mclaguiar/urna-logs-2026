# Curva horária — RO 1º turno

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

- Habilitações no dia: **991,781**
  - **701** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **673** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **28** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **987,987** (99.6175%)
- Pós-encerramento ≥17h: **3,794** (% entre oficial+pós: **0.3825**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **4,698** · urnas: **4,711**
- Pico (hora local): **10h** (135,482)
- Faixas ≥17h (ref. brasilia): 17–18h **0.3756** · 18–19h **0.007** · 19h+ **0.0**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **991,781**
- Votos computados no log (`O voto do eleitor foi computado`): **991,080**
- Votos de presidente no BU: **991,080**
  - nominais **968,125** · brancos **9,846** · nulos **13,109**

**+701** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**991,080** = **991,080**). O +701 está fora dessa conta.
- **673** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **28** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **913,593** (92.12% do dia)
- Manual: **78,159** (7.88% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **29** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 07h | 98,966 | 9.9786 | oficial | 89,302 | 90.235 | 9,660 | 9.7609 | 0 | 0.0 | 4 | 0.004 |
| 08h | 114,250 | 11.5197 | oficial | 103,612 | 90.6888 | 10,635 | 9.3085 | 0 | 0.0 | 3 | 0.0026 |
| 09h | 126,847 | 12.7898 | oficial | 116,341 | 91.7176 | 10,503 | 8.2801 | 0 | 0.0 | 3 | 0.0024 |
| 10h | 135,482 | 13.6605 | oficial | 125,411 | 92.5665 | 10,064 | 7.4283 | 0 | 0.0 | 7 | 0.0052 |
| 11h | 128,773 | 12.984 | oficial | 120,094 | 93.2602 | 8,675 | 6.7367 | 0 | 0.0 | 4 | 0.0031 |
| 12h | 109,612 | 11.052 | oficial | 102,160 | 93.2015 | 7,451 | 6.7976 | 0 | 0.0 | 1 | 0.0009 |
| 13h | 97,867 | 9.8678 | oficial | 90,600 | 92.5746 | 7,264 | 7.4223 | 0 | 0.0 | 3 | 0.0031 |
| 14h | 95,758 | 9.6552 | oficial | 88,244 | 92.1531 | 7,512 | 7.8448 | 0 | 0.0 | 2 | 0.0021 |
| 15h | 80,432 | 8.1099 | oficial | 74,335 | 92.4197 | 6,095 | 7.5778 | 0 | 0.0 | 2 | 0.0025 |
| 16h | 3,725 | 0.3756 | pós-encerramento | 3,430 | 92.0805 | 295 | 7.9195 | 0 | 0.0 | 0 | 0.0 |
| 17h | 69 | 0.007 | pós-encerramento | 64 | 92.7536 | 5 | 7.2464 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
