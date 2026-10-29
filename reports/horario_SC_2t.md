# Curva horária — SC 2º turno

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

- Habilitações no dia: **4,762,557**
  - **254** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **222** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **32** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **4,762,157** (99.9916%)
- Pós-encerramento ≥17h: **400** (% entre oficial+pós: **0.0084**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **17,326** · urnas: **17,559**
- Pico (hora local): **8h** (807,296)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0084** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **4,636,836** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **4,762,557**
- Votos computados no log (`O voto do eleitor foi computado`): **4,762,303**
- Votos de presidente no BU: **4,762,303**
  - nominais **4,638,385** · brancos **48,674** · nulos **75,244**

**+254** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**4,762,303** = **4,762,303**). O +254 está fora dessa conta.
- **222** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **32** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **4,152,065** (87.18% do dia)
- Manual: **610,324** (12.82% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **168** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 807,296 | 16.9509 | oficial | 695,602 | 86.1644 | 111,657 | 13.831 | 0 | 0.0 | 37 | 0.0046 |
| 09h | 757,182 | 15.8986 | oficial | 658,204 | 86.9281 | 98,951 | 13.0683 | 0 | 0.0 | 27 | 0.0036 |
| 10h | 731,781 | 15.3653 | oficial | 642,065 | 87.74 | 89,688 | 12.2561 | 0 | 0.0 | 28 | 0.0038 |
| 11h | 573,462 | 12.0411 | oficial | 506,632 | 88.3462 | 66,813 | 11.6508 | 0 | 0.0 | 17 | 0.003 |
| 12h | 420,797 | 8.8355 | oficial | 370,153 | 87.9647 | 50,635 | 12.0331 | 0 | 0.0 | 9 | 0.0021 |
| 13h | 448,021 | 9.4072 | oficial | 389,072 | 86.8424 | 58,936 | 13.1547 | 0 | 0.0 | 13 | 0.0029 |
| 14h | 447,231 | 9.3906 | oficial | 387,809 | 86.7134 | 59,409 | 13.2837 | 0 | 0.0 | 13 | 0.0029 |
| 15h | 359,539 | 7.5493 | oficial | 312,557 | 86.9327 | 46,963 | 13.062 | 0 | 0.0 | 19 | 0.0053 |
| 16h | 216,848 | 4.5532 | oficial | 189,660 | 87.4622 | 27,183 | 12.5355 | 0 | 0.0 | 5 | 0.0023 |
| 17h | 400 | 0.0084 | pós-encerramento | 311 | 77.75 | 89 | 22.25 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 4,636,836 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
