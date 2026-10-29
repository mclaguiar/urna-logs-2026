# Curva horária — RJ 1º turno

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

- Habilitações no dia: **9,863,105**
  - **3,303** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **2,641** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **662** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **9,636,066** (97.6981%)
- Pós-encerramento ≥17h: **227,039** (% entre oficial+pós: **2.3019**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **37,675** · urnas: **37,874**
- Pico (hora local): **11h** (1,180,044)
- Faixas ≥17h (ref. brasilia): 17–18h **2.0513** · 18–19h **0.2329** · 19h+ **0.0176**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **9,863,105**
- Votos computados no log (`O voto do eleitor foi computado`): **9,859,980**
- Votos de presidente no BU: **9,859,802**
  - nominais **9,370,087** · brancos **201,979** · nulos **287,736**

**+3,303** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**9,859,980**) e votos do BU (**9,859,802**) diferem em **+178**.
- **2,641** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **662** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **8,469,597** (85.87% do dia)
- Manual: **1,393,147** (14.12% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **361** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 982,588 | 9.9623 | oficial | 822,945 | 83.7528 | 159,579 | 16.2407 | 0 | 0.0 | 64 | 0.0065 |
| 09h | 1,085,903 | 11.0097 | oficial | 915,430 | 84.3013 | 170,440 | 15.6957 | 0 | 0.0 | 33 | 0.003 |
| 10h | 1,138,783 | 11.5459 | oficial | 968,077 | 85.0098 | 170,668 | 14.9869 | 0 | 0.0 | 38 | 0.0033 |
| 11h | 1,180,044 | 11.9642 | oficial | 1,014,021 | 85.9308 | 165,976 | 14.0652 | 0 | 0.0 | 47 | 0.004 |
| 12h | 1,179,864 | 11.9624 | oficial | 1,022,370 | 86.6515 | 157,456 | 13.3453 | 0 | 0.0 | 38 | 0.0032 |
| 13h | 1,128,291 | 11.4395 | oficial | 980,886 | 86.9356 | 147,370 | 13.0613 | 0 | 0.0 | 35 | 0.0031 |
| 14h | 1,061,457 | 10.7619 | oficial | 920,483 | 86.7188 | 140,937 | 13.2777 | 0 | 0.0 | 37 | 0.0035 |
| 15h | 1,003,476 | 10.174 | oficial | 868,820 | 86.581 | 134,630 | 13.4164 | 0 | 0.0 | 26 | 0.0026 |
| 16h | 875,660 | 8.8781 | oficial | 759,406 | 86.7238 | 116,224 | 13.2727 | 0 | 0.0 | 30 | 0.0034 |
| 17h | 202,326 | 2.0513 | pós-encerramento | 175,709 | 86.8445 | 26,605 | 13.1496 | 0 | 0.0 | 12 | 0.0059 |
| 18h | 22,974 | 0.2329 | pós-encerramento | 19,943 | 86.8068 | 3,030 | 13.1888 | 0 | 0.0 | 1 | 0.0044 |
| 19h | 1,687 | 0.0171 | pós-encerramento | 1,460 | 86.5442 | 227 | 13.4558 | 0 | 0.0 | 0 | 0.0 |
| 20h | 52 | 0.0005 | pós-encerramento | 47 | 90.3846 | 5 | 9.6154 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
