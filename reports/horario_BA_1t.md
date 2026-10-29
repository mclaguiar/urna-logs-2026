# Curva horária — BA 1º turno

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

- Habilitações no dia: **9,057,210**
  - **3,609** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **3,113** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **496** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **8,398,318** (92.7252%)
- Pós-encerramento ≥17h: **658,892** (% entre oficial+pós: **7.2748**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **35,476** · urnas: **35,675**
- Pico (hora local): **11h** (995,027)
- Faixas ≥17h (ref. brasilia): 17–18h **5.1669** · 18–19h **1.6492** · 19h+ **0.4587**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **9,057,210**
- Votos computados no log (`O voto do eleitor foi computado`): **9,053,565**
- Votos de presidente no BU: **9,053,601**
  - nominais **8,560,542** · brancos **154,936** · nulos **338,123**

**+3,609** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**9,053,565**) e votos do BU (**9,053,601**) diferem em **-36**.
- **3,113** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **496** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **7,968,996** (87.99% do dia)
- Manual: **1,087,893** (12.01% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **321** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 784,280 | 8.6592 | oficial | 683,885 | 87.1991 | 100,331 | 12.7928 | 0 | 0.0 | 64 | 0.0082 |
| 09h | 897,773 | 9.9122 | oficial | 785,243 | 87.4657 | 112,506 | 12.5317 | 0 | 0.0 | 24 | 0.0027 |
| 10h | 951,727 | 10.5079 | oficial | 835,642 | 87.8027 | 116,064 | 12.1951 | 0 | 0.0 | 21 | 0.0022 |
| 11h | 995,027 | 10.986 | oficial | 878,215 | 88.2604 | 116,783 | 11.7367 | 0 | 0.0 | 29 | 0.0029 |
| 12h | 990,201 | 10.9327 | oficial | 876,585 | 88.526 | 113,583 | 11.4707 | 0 | 0.0 | 33 | 0.0033 |
| 13h | 958,402 | 10.5816 | oficial | 846,170 | 88.2897 | 112,203 | 11.7073 | 0 | 0.0 | 29 | 0.003 |
| 14h | 949,475 | 10.4831 | oficial | 836,179 | 88.0675 | 113,256 | 11.9283 | 0 | 0.0 | 40 | 0.0042 |
| 15h | 952,913 | 10.521 | oficial | 838,204 | 87.9623 | 114,674 | 12.034 | 0 | 0.0 | 35 | 0.0037 |
| 16h | 918,520 | 10.1413 | oficial | 809,369 | 88.1166 | 109,127 | 11.8807 | 0 | 0.0 | 24 | 0.0026 |
| 17h | 467,976 | 5.1669 | pós-encerramento | 412,678 | 88.1836 | 55,286 | 11.8139 | 0 | 0.0 | 12 | 0.0026 |
| 18h | 149,371 | 1.6492 | pós-encerramento | 130,923 | 87.6495 | 18,441 | 12.3458 | 0 | 0.0 | 7 | 0.0047 |
| 19h | 34,011 | 0.3755 | pós-encerramento | 29,488 | 86.7014 | 4,520 | 13.2898 | 0 | 0.0 | 3 | 0.0088 |
| 20h | 6,509 | 0.0719 | pós-encerramento | 5,559 | 85.4048 | 950 | 14.5952 | 0 | 0.0 | 0 | 0.0 |
| 21h | 935 | 0.0103 | pós-encerramento | 783 | 83.7433 | 152 | 16.2567 | 0 | 0.0 | 0 | 0.0 |
| 22h | 90 | 0.001 | pós-encerramento | 73 | 81.1111 | 17 | 18.8889 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
