# Curva horária — ZZ 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério: janela 8h–17h no **horário local** (exterior); ≥17h = pós-encerramento.

Métricas deste relatório = **somente o dia oficial deste turno**.
Janelas no dia: **oficial** [8h,17h) · **pós-encerramento** ≥17h · **fora do previsto** &lt;8h.
Eventos de **outra data** no `.jez` = histórico (não entram nos totais nem no comparativo 1º×2º).
Dia oficial deste turno: **2026-10-04**.

## Resumo (só o dia do turno)

- Habilitações no dia: **341,086**
  - O BU registra **680** votos de presidente a mais do que as habilitações do log.
- Oficial [8h,17h): **338,916** (99.3638%)
- Pós-encerramento ≥17h: **2,170** (% entre oficial+pós: **0.6362**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **1,310** · urnas: **1,282**
- Pico (hora local): **11h** (45,356)
- Faixas ≥17h (ref. local): 17–18h **0.6075** · 18–19h **0.0287** · 19h+ **0.0**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **341,086**
- Votos computados no log (`O voto do eleitor foi computado`): **340,977**
- Votos de presidente no BU: **341,766**
  - nominais **331,005** · brancos **5,816** · nulos **4,945**

**-680**: o BU tem **680** votos de presidente a mais do que as habilitações do log.

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

- Com digital: **0** (0.0% do dia)
- Manual: **341,086** (100.0% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **0** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 35,851 | 10.5108 | oficial | 0 | 0.0 | 35,851 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 09h | 39,956 | 11.7143 | oficial | 0 | 0.0 | 39,956 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 10h | 42,534 | 12.4702 | oficial | 0 | 0.0 | 42,534 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 11h | 45,356 | 13.2975 | oficial | 0 | 0.0 | 45,356 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 12h | 43,190 | 12.6625 | oficial | 0 | 0.0 | 43,190 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 13h | 40,194 | 11.7841 | oficial | 0 | 0.0 | 40,194 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 14h | 38,016 | 11.1456 | oficial | 0 | 0.0 | 38,016 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 15h | 32,290 | 9.4668 | oficial | 0 | 0.0 | 32,290 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 16h | 21,529 | 6.3119 | oficial | 0 | 0.0 | 21,529 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 17h | 2,072 | 0.6075 | pós-encerramento | 0 | 0.0 | 2,072 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 18h | 98 | 0.0287 | pós-encerramento | 0 | 0.0 | 98 | 100.0 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
