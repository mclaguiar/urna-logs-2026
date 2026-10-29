# Curva horária — MG 2º turno

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

- Habilitações no dia: **13,045,066**
  - **863** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **674** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **189** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **13,043,089** (99.9848%)
- Pós-encerramento ≥17h: **1,977** (% entre oficial+pós: **0.0152**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **52,062** · urnas: **52,384**
- Pico (hora local): **8h** (2,290,125)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0152** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **12,604,710** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **13,045,066**
- Votos computados no log (`O voto do eleitor foi computado`): **13,044,249**
- Votos de presidente no BU: **13,044,203**
  - nominais **12,592,885** · brancos **164,141** · nulos **287,177**

**+863** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**13,044,249**) e votos do BU (**13,044,203**) diferem em **+46**.
- **674** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **189** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **10,654,536** (81.67% do dia)
- Manual: **2,390,176** (18.32% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **354** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 2,290,125 | 17.5555 | oficial | 1,868,368 | 81.5837 | 421,688 | 18.4133 | 0 | 0.0 | 69 | 0.003 |
| 09h | 2,006,413 | 15.3806 | oficial | 1,639,749 | 81.7254 | 366,624 | 18.2726 | 0 | 0.0 | 40 | 0.002 |
| 10h | 1,917,776 | 14.7012 | oficial | 1,579,451 | 82.3585 | 338,266 | 17.6385 | 0 | 0.0 | 59 | 0.0031 |
| 11h | 1,648,961 | 12.6405 | oficial | 1,366,329 | 82.86 | 282,593 | 17.1376 | 0 | 0.0 | 39 | 0.0024 |
| 12h | 1,316,472 | 10.0917 | oficial | 1,083,980 | 82.3398 | 232,444 | 17.6566 | 0 | 0.0 | 48 | 0.0036 |
| 13h | 1,131,169 | 8.6712 | oficial | 918,447 | 81.1945 | 212,702 | 18.8037 | 0 | 0.0 | 20 | 0.0018 |
| 14h | 1,135,661 | 8.7057 | oficial | 914,225 | 80.5016 | 221,392 | 19.4945 | 0 | 0.0 | 44 | 0.0039 |
| 15h | 968,789 | 7.4265 | oficial | 777,763 | 80.282 | 191,001 | 19.7154 | 0 | 0.0 | 25 | 0.0026 |
| 16h | 627,723 | 4.812 | oficial | 504,708 | 80.403 | 123,005 | 19.5954 | 0 | 0.0 | 10 | 0.0016 |
| 17h | 1,977 | 0.0152 | pós-encerramento | 1,516 | 76.6818 | 461 | 23.3182 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 12,604,710 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
