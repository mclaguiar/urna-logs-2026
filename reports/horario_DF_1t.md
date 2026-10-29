# Curva horária — DF 1º turno

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

- Habilitações no dia: **1,832,541**
  - **1,145** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **1,094** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **51** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **1,813,053** (98.9366%)
- Pós-encerramento ≥17h: **19,488** (% entre oficial+pós: **1.0634**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **6,969** · urnas: **6,989**
- Pico (hora local): **11h** (232,143)
- Faixas ≥17h (ref. brasilia): 17–18h **1.0165** · 18–19h **0.0469** · 19h+ **0.0**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **1,832,541**
- Votos computados no log (`O voto do eleitor foi computado`): **1,831,396**
- Votos de presidente no BU: **1,831,396**
  - nominais **1,772,865** · brancos **25,362** · nulos **33,169**

**+1,145** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**1,831,396** = **1,831,396**). O +1,145 está fora dessa conta.
- **1,094** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **51** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **1,686,227** (92.02% do dia)
- Manual: **146,241** (7.98% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **73** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 184,013 | 10.0414 | oficial | 168,907 | 91.7908 | 15,093 | 8.2021 | 0 | 0.0 | 13 | 0.0071 |
| 09h | 205,726 | 11.2263 | oficial | 188,368 | 91.5626 | 17,348 | 8.4326 | 0 | 0.0 | 10 | 0.0049 |
| 10h | 221,044 | 12.0622 | oficial | 202,709 | 91.7053 | 18,327 | 8.2911 | 0 | 0.0 | 8 | 0.0036 |
| 11h | 232,143 | 12.6678 | oficial | 213,831 | 92.1118 | 18,307 | 7.8861 | 0 | 0.0 | 5 | 0.0022 |
| 12h | 231,420 | 12.6284 | oficial | 213,818 | 92.3939 | 17,595 | 7.6031 | 0 | 0.0 | 7 | 0.003 |
| 13h | 213,654 | 11.6589 | oficial | 197,513 | 92.4453 | 16,138 | 7.5533 | 0 | 0.0 | 3 | 0.0014 |
| 14h | 196,978 | 10.7489 | oficial | 181,628 | 92.2073 | 15,336 | 7.7856 | 0 | 0.0 | 14 | 0.0071 |
| 15h | 184,733 | 10.0807 | oficial | 169,928 | 91.9857 | 14,797 | 8.0099 | 0 | 0.0 | 8 | 0.0043 |
| 16h | 143,342 | 7.822 | oficial | 131,641 | 91.837 | 11,697 | 8.1602 | 0 | 0.0 | 4 | 0.0028 |
| 17h | 18,628 | 1.0165 | pós-encerramento | 17,079 | 91.6846 | 1,548 | 8.3101 | 0 | 0.0 | 1 | 0.0054 |
| 18h | 860 | 0.0469 | pós-encerramento | 805 | 93.6047 | 55 | 6.3953 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
