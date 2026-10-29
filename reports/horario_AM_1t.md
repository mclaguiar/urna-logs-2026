# Curva horária — AM 1º turno

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

- Habilitações no dia: **2,235,742**
  - **1,193** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **1,093** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **100** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **2,076,875** (92.8942%)
- Pós-encerramento ≥17h: **147,443** (% entre oficial+pós: **6.6287**)
- Fora do previsto (&lt;8h no dia): **11,424** (0.511%)
- Seções: **8,157** · urnas: **8,186**
- Pico (hora local): **11h** (248,314)
- Faixas ≥17h (ref. brasilia): 17–18h **5.0948** · 18–19h **1.2305** · 19h+ **0.3034**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **2,235,742**
- Votos computados no log (`O voto do eleitor foi computado`): **2,234,549**
- Votos de presidente no BU: **2,234,549**
  - nominais **2,170,845** · brancos **24,402** · nulos **39,302**

**+1,193** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**2,234,549** = **2,234,549**). O +1,193 está fora dessa conta.
- **1,093** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **100** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **2,015,200** (90.14% do dia)
- Manual: **220,434** (9.86% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **108** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 06h | 11,424 | 0.511 | fora (<8h) | 10,346 | 90.5637 | 1,078 | 9.4363 | 0 | 0.0 | 0 | 0.0 |
| 07h | 183,352 | 8.2009 | oficial | 164,322 | 89.6211 | 19,019 | 10.3729 | 0 | 0.0 | 11 | 0.006 |
| 08h | 210,695 | 9.4239 | oficial | 188,188 | 89.3177 | 22,501 | 10.6794 | 0 | 0.0 | 6 | 0.0028 |
| 09h | 227,021 | 10.1542 | oficial | 203,592 | 89.6798 | 23,418 | 10.3153 | 0 | 0.0 | 11 | 0.0048 |
| 10h | 241,786 | 10.8146 | oficial | 218,053 | 90.1843 | 23,725 | 9.8124 | 0 | 0.0 | 8 | 0.0033 |
| 11h | 248,314 | 11.1066 | oficial | 224,357 | 90.3521 | 23,940 | 9.641 | 0 | 0.0 | 17 | 0.0068 |
| 12h | 246,244 | 11.014 | oficial | 222,761 | 90.4635 | 23,472 | 9.532 | 0 | 0.0 | 11 | 0.0045 |
| 13h | 244,374 | 10.9303 | oficial | 221,041 | 90.4519 | 23,319 | 9.5423 | 0 | 0.0 | 14 | 0.0057 |
| 14h | 243,015 | 10.8695 | oficial | 219,435 | 90.2969 | 23,568 | 9.6982 | 0 | 0.0 | 12 | 0.0049 |
| 15h | 232,074 | 10.3802 | oficial | 209,392 | 90.2264 | 22,675 | 9.7706 | 0 | 0.0 | 7 | 0.003 |
| 16h | 113,325 | 5.0688 | pós-encerramento | 102,728 | 90.649 | 10,587 | 9.3422 | 0 | 0.0 | 10 | 0.0088 |
| 17h | 27,370 | 1.2242 | pós-encerramento | 24,793 | 90.5846 | 2,576 | 9.4118 | 0 | 0.0 | 1 | 0.0037 |
| 18h | 5,212 | 0.2331 | pós-encerramento | 4,786 | 91.8266 | 426 | 8.1734 | 0 | 0.0 | 0 | 0.0 |
| 19h | 1,170 | 0.0523 | pós-encerramento | 1,071 | 91.5385 | 99 | 8.4615 | 0 | 0.0 | 0 | 0.0 |
| 20h | 346 | 0.0155 | pós-encerramento | 316 | 91.3295 | 30 | 8.6705 | 0 | 0.0 | 0 | 0.0 |
| 21h | 20 | 0.0009 | pós-encerramento | 19 | 95.0 | 1 | 5.0 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
