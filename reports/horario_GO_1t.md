# Curva horária — GO 1º turno

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

- Habilitações no dia: **3,973,196**
  - **1,609** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **1,462** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **147** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **3,902,808** (98.2284%)
- Pós-encerramento ≥17h: **70,388** (% entre oficial+pós: **1.7716**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **15,686** · urnas: **15,740**
- Pico (hora local): **11h** (492,869)
- Faixas ≥17h (ref. brasilia): 17–18h **1.6041** · 18–19h **0.1582** · 19h+ **0.0093**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **3,973,196**
- Votos computados no log (`O voto do eleitor foi computado`): **3,971,587**
- Votos de presidente no BU: **3,971,587**
  - nominais **3,827,930** · brancos **45,643** · nulos **98,014**

**+1,609** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**3,971,587** = **3,971,587**). O +1,609 está fora dessa conta.
- **1,462** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **147** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **3,526,830** (88.77% do dia)
- Manual: **446,267** (11.23% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **99** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 388,155 | 9.7693 | oficial | 340,472 | 87.7155 | 47,668 | 12.2807 | 0 | 0.0 | 15 | 0.0039 |
| 09h | 440,372 | 11.0836 | oficial | 388,790 | 88.2867 | 51,574 | 11.7115 | 0 | 0.0 | 8 | 0.0018 |
| 10h | 472,926 | 11.9029 | oficial | 420,372 | 88.8875 | 52,543 | 11.1102 | 0 | 0.0 | 11 | 0.0023 |
| 11h | 492,869 | 12.4048 | oficial | 440,720 | 89.4193 | 52,143 | 10.5795 | 0 | 0.0 | 6 | 0.0012 |
| 12h | 477,997 | 12.0305 | oficial | 427,777 | 89.4937 | 50,207 | 10.5036 | 0 | 0.0 | 13 | 0.0027 |
| 13h | 439,374 | 11.0585 | oficial | 390,797 | 88.944 | 48,564 | 11.053 | 0 | 0.0 | 13 | 0.003 |
| 14h | 422,611 | 10.6366 | oficial | 374,505 | 88.617 | 48,096 | 11.3807 | 0 | 0.0 | 10 | 0.0024 |
| 15h | 410,552 | 10.333 | oficial | 363,321 | 88.4957 | 47,223 | 11.5023 | 0 | 0.0 | 8 | 0.0019 |
| 16h | 357,952 | 9.0092 | oficial | 317,350 | 88.6571 | 40,589 | 11.3392 | 0 | 0.0 | 13 | 0.0036 |
| 17h | 63,734 | 1.6041 | pós-encerramento | 56,876 | 89.2397 | 6,857 | 10.7588 | 0 | 0.0 | 1 | 0.0016 |
| 18h | 6,285 | 0.1582 | pós-encerramento | 5,532 | 88.0191 | 752 | 11.965 | 0 | 0.0 | 1 | 0.0159 |
| 19h | 342 | 0.0086 | pós-encerramento | 296 | 86.5497 | 46 | 13.4503 | 0 | 0.0 | 0 | 0.0 |
| 20h | 27 | 0.0007 | pós-encerramento | 22 | 81.4815 | 5 | 18.5185 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
