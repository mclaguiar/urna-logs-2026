# Curva horária — BA 2º turno

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

- Habilitações no dia: **9,423,056**
  - **1,009** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **669** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **340** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **9,419,163** (99.9587%)
- Pós-encerramento ≥17h: **3,893** (% entre oficial+pós: **0.0413**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **35,476** · urnas: **35,869**
- Pico (hora local): **8h** (1,797,670)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0383** · 18–19h **0.003** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **9,017,681** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **9,423,056**
- Votos computados no log (`O voto do eleitor foi computado`): **9,422,218**
- Votos de presidente no BU: **9,422,047**
  - nominais **9,094,019** · brancos **92,721** · nulos **235,307**

**+1,009** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**9,422,218**) e votos do BU (**9,422,047**) diferem em **+171**.
- **669** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **340** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **8,267,709** (87.74% do dia)
- Manual: **1,155,034** (12.26% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **313** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 1,797,670 | 19.0774 | oficial | 1,579,158 | 87.8447 | 218,435 | 12.151 | 0 | 0.0 | 77 | 0.0043 |
| 09h | 1,659,408 | 17.6101 | oficial | 1,458,083 | 87.8677 | 201,285 | 12.1299 | 0 | 0.0 | 40 | 0.0024 |
| 10h | 1,465,523 | 15.5525 | oficial | 1,287,722 | 87.8677 | 177,757 | 12.1293 | 0 | 0.0 | 44 | 0.003 |
| 11h | 1,117,784 | 11.8622 | oficial | 982,563 | 87.9028 | 135,188 | 12.0943 | 0 | 0.0 | 33 | 0.003 |
| 12h | 766,632 | 8.1357 | oficial | 673,002 | 87.7868 | 93,613 | 12.2109 | 0 | 0.0 | 17 | 0.0022 |
| 13h | 682,374 | 7.2415 | oficial | 597,247 | 87.5249 | 85,100 | 12.4712 | 0 | 0.0 | 27 | 0.004 |
| 14h | 714,797 | 7.5856 | oficial | 624,813 | 87.4113 | 89,959 | 12.5853 | 0 | 0.0 | 25 | 0.0035 |
| 15h | 707,363 | 7.5067 | oficial | 618,295 | 87.4084 | 89,041 | 12.5877 | 0 | 0.0 | 27 | 0.0038 |
| 16h | 507,612 | 5.3869 | oficial | 443,575 | 87.3847 | 64,014 | 12.6108 | 0 | 0.0 | 23 | 0.0045 |
| 17h | 3,606 | 0.0383 | pós-encerramento | 3,005 | 83.3333 | 601 | 16.6667 | 0 | 0.0 | 0 | 0.0 |
| 18h | 285 | 0.003 | pós-encerramento | 244 | 85.614 | 41 | 14.386 | 0 | 0.0 | 0 | 0.0 |
| 19h | 2 | 0.0 | pós-encerramento | 2 | 100.0 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 9,017,681 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
