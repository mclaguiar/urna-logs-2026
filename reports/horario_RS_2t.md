# Curva horária — RS 2º turno

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

- Habilitações no dia: **6,889,987**
  - **349** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **280** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **69** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **6,889,278** (99.9897%)
- Pós-encerramento ≥17h: **709** (% entre oficial+pós: **0.0103**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **27,547** · urnas: **27,894**
- Pico (hora local): **10h** (1,086,871)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0103** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **6,697,924** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **6,889,987**
- Votos computados no log (`O voto do eleitor foi computado`): **6,889,636**
- Votos de presidente no BU: **6,889,638**
  - nominais **6,698,930** · brancos **89,463** · nulos **101,245**

**+349** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**6,889,636**) e votos do BU (**6,889,638**) diferem em **-2**.
- **280** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **69** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **5,747,916** (83.42% do dia)
- Manual: **1,141,850** (16.57% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **221** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 1,030,011 | 14.9494 | oficial | 861,753 | 83.6644 | 168,207 | 16.3306 | 0 | 0.0 | 51 | 0.005 |
| 09h | 1,035,176 | 15.0244 | oficial | 864,235 | 83.4868 | 170,904 | 16.5097 | 0 | 0.0 | 37 | 0.0036 |
| 10h | 1,086,871 | 15.7746 | oficial | 912,471 | 83.9539 | 174,355 | 16.0419 | 0 | 0.0 | 45 | 0.0041 |
| 11h | 874,117 | 12.6868 | oficial | 731,538 | 83.6888 | 142,566 | 16.3097 | 0 | 0.0 | 13 | 0.0015 |
| 12h | 636,998 | 9.2453 | oficial | 529,422 | 83.112 | 107,554 | 16.8845 | 0 | 0.0 | 22 | 0.0035 |
| 13h | 636,029 | 9.2312 | oficial | 529,313 | 83.2215 | 106,701 | 16.7761 | 0 | 0.0 | 15 | 0.0024 |
| 14h | 665,449 | 9.6582 | oficial | 552,212 | 82.9834 | 113,224 | 17.0147 | 0 | 0.0 | 13 | 0.002 |
| 15h | 559,225 | 8.1165 | oficial | 463,215 | 82.8316 | 95,995 | 17.1657 | 0 | 0.0 | 15 | 0.0027 |
| 16h | 365,402 | 5.3034 | oficial | 303,233 | 82.9861 | 62,159 | 17.0111 | 0 | 0.0 | 10 | 0.0027 |
| 17h | 709 | 0.0103 | pós-encerramento | 524 | 73.9069 | 185 | 26.0931 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 6,697,924 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
