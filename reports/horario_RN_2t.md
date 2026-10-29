# Curva horária — RN 2º turno

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

- Habilitações no dia: **2,233,014**
  - **191** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **149** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **42** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **2,232,667** (99.9845%)
- Pós-encerramento ≥17h: **347** (% entre oficial+pós: **0.0155**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **8,115** · urnas: **8,186**
- Pico (hora local): **8h** (397,295)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0154** · 18–19h **0.0001** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **2,163,415** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **2,233,014**
- Votos computados no log (`O voto do eleitor foi computado`): **2,232,823**
- Votos de presidente no BU: **2,232,823**
  - nominais **2,151,005** · brancos **19,939** · nulos **61,879**

**+191** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**2,232,823** = **2,232,823**). O +191 está fora dessa conta.
- **149** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **42** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **1,968,208** (88.14% do dia)
- Manual: **264,713** (11.85% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **93** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 397,295 | 17.7919 | oficial | 347,573 | 87.4849 | 49,704 | 12.5106 | 0 | 0.0 | 18 | 0.0045 |
| 09h | 381,623 | 17.09 | oficial | 336,302 | 88.1241 | 45,307 | 11.8722 | 0 | 0.0 | 14 | 0.0037 |
| 10h | 340,311 | 15.24 | oficial | 301,133 | 88.4876 | 39,159 | 11.5068 | 0 | 0.0 | 19 | 0.0056 |
| 11h | 260,167 | 11.6509 | oficial | 230,456 | 88.58 | 29,700 | 11.4157 | 0 | 0.0 | 11 | 0.0042 |
| 12h | 196,450 | 8.7975 | oficial | 173,941 | 88.5421 | 22,500 | 11.4533 | 0 | 0.0 | 9 | 0.0046 |
| 13h | 168,917 | 7.5645 | oficial | 148,588 | 87.9651 | 20,324 | 12.0319 | 0 | 0.0 | 5 | 0.003 |
| 14h | 171,755 | 7.6916 | oficial | 151,113 | 87.9817 | 20,640 | 12.0171 | 0 | 0.0 | 2 | 0.0012 |
| 15h | 188,436 | 8.4386 | oficial | 165,991 | 88.0888 | 22,436 | 11.9064 | 0 | 0.0 | 9 | 0.0048 |
| 16h | 127,713 | 5.7193 | oficial | 112,838 | 88.3528 | 14,869 | 11.6425 | 0 | 0.0 | 6 | 0.0047 |
| 17h | 345 | 0.0154 | pós-encerramento | 271 | 78.5507 | 74 | 21.4493 | 0 | 0.0 | 0 | 0.0 |
| 18h | 2 | 0.0001 | pós-encerramento | 2 | 100.0 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 2,163,415 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
