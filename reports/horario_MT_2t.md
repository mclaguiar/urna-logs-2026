# Curva horária — MT 2º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-4).
Critério: janela **8h–17h Brasília** (local +1h → BRT); ≥17h = pós-encerramento (fila).

Métricas deste relatório = **somente o dia oficial deste turno**.
Janelas no dia: **oficial** [8h,17h) · **pós-encerramento** ≥17h · **fora do previsto** &lt;8h.
Eventos de **outra data** no `.jez` = histórico (não entram nos totais nem no comparativo 1º×2º).
Dia oficial deste turno: **2026-10-25**.

## Resumo (só o dia do turno)

- Habilitações no dia: **2,085,473**
  - **139** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **125** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **14** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **2,084,657** (99.9609%)
- Pós-encerramento ≥17h: **816** (% entre oficial+pós: **0.0391**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **8,287** · urnas: **8,359**
- Pico (hora local): **8h** (359,559)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0391** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **2,047,721** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **2,085,473**
- Votos computados no log (`O voto do eleitor foi computado`): **2,085,334**
- Votos de presidente no BU: **2,085,334**
  - nominais **2,045,266** · brancos **15,431** · nulos **24,637**

**+139** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**2,085,334** = **2,085,334**). O +139 está fora dessa conta.
- **125** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **14** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **1,867,265** (89.54% do dia)
- Manual: **218,134** (10.46% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **74** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 07h | 352,358 | 16.8958 | oficial | 312,787 | 88.7697 | 39,551 | 11.2247 | 0 | 0.0 | 20 | 0.0057 |
| 08h | 359,559 | 17.2411 | oficial | 321,130 | 89.3122 | 38,418 | 10.6848 | 0 | 0.0 | 11 | 0.0031 |
| 09h | 341,151 | 16.3584 | oficial | 306,453 | 89.8291 | 34,687 | 10.1676 | 0 | 0.0 | 11 | 0.0032 |
| 10h | 271,486 | 13.018 | oficial | 244,780 | 90.163 | 26,697 | 9.8337 | 0 | 0.0 | 9 | 0.0033 |
| 11h | 196,990 | 9.4458 | oficial | 177,668 | 90.1914 | 19,319 | 9.8071 | 0 | 0.0 | 3 | 0.0015 |
| 12h | 152,162 | 7.2963 | oficial | 136,646 | 89.803 | 15,511 | 10.1937 | 0 | 0.0 | 5 | 0.0033 |
| 13h | 146,041 | 7.0028 | oficial | 130,810 | 89.5707 | 15,225 | 10.4252 | 0 | 0.0 | 6 | 0.0041 |
| 14h | 151,074 | 7.2441 | oficial | 134,829 | 89.247 | 16,241 | 10.7504 | 0 | 0.0 | 4 | 0.0026 |
| 15h | 113,836 | 5.4585 | oficial | 101,476 | 89.1423 | 12,355 | 10.8533 | 0 | 0.0 | 5 | 0.0044 |
| 16h | 815 | 0.0391 | pós-encerramento | 685 | 84.0491 | 130 | 15.9509 | 0 | 0.0 | 0 | 0.0 |
| 17h | 1 | 0.0 | pós-encerramento | 1 | 100.0 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 2,047,721 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
