# Curva horária — AL 2º turno

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

- Habilitações no dia: **1,951,827**
  - **195** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **186** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **9** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **1,951,257** (99.9708%)
- Pós-encerramento ≥17h: **570** (% entre oficial+pós: **0.0292**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **7,101** · urnas: **7,211**
- Pico (hora local): **8h** (378,842)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0292** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **1,933,317** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **1,951,827**
- Votos computados no log (`O voto do eleitor foi computado`): **1,951,632**
- Votos de presidente no BU: **1,951,632**
  - nominais **1,896,761** · brancos **16,983** · nulos **37,888**

**+195** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**1,951,632** = **1,951,632**). O +195 está fora dessa conta.
- **186** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **9** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **1,745,904** (89.45% do dia)
- Manual: **205,855** (10.55% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **68** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 378,842 | 19.4096 | oficial | 336,975 | 88.9487 | 41,851 | 11.0471 | 0 | 0.0 | 16 | 0.0042 |
| 09h | 344,945 | 17.6729 | oficial | 307,439 | 89.127 | 37,489 | 10.8681 | 0 | 0.0 | 17 | 0.0049 |
| 10h | 292,737 | 14.9981 | oficial | 262,183 | 89.5626 | 30,544 | 10.4339 | 0 | 0.0 | 10 | 0.0034 |
| 11h | 215,805 | 11.0566 | oficial | 193,772 | 89.7903 | 22,026 | 10.2064 | 0 | 0.0 | 7 | 0.0032 |
| 12h | 153,258 | 7.852 | oficial | 137,989 | 90.0371 | 15,267 | 9.9616 | 0 | 0.0 | 2 | 0.0013 |
| 13h | 139,206 | 7.1321 | oficial | 125,212 | 89.9473 | 13,989 | 10.0491 | 0 | 0.0 | 5 | 0.0036 |
| 14h | 152,476 | 7.812 | oficial | 136,714 | 89.6626 | 15,756 | 10.3334 | 0 | 0.0 | 6 | 0.0039 |
| 15h | 160,500 | 8.2231 | oficial | 143,579 | 89.4573 | 16,918 | 10.5408 | 0 | 0.0 | 3 | 0.0019 |
| 16h | 113,488 | 5.8144 | oficial | 101,551 | 89.4817 | 11,935 | 10.5165 | 0 | 0.0 | 2 | 0.0018 |
| 17h | 570 | 0.0292 | pós-encerramento | 490 | 85.9649 | 80 | 14.0351 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 1,933,317 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
