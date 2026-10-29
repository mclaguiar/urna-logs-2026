# Curva horária — RR 2º turno

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

- Habilitações no dia: **308,630**
  - **33** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **31** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **2** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **308,499** (99.9576%)
- Pós-encerramento ≥17h: **131** (% entre oficial+pós: **0.0424**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **1,519** · urnas: **1,526**
- Pico (hora local): **9h** (51,889)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0424** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **328,794** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **308,630**
- Votos computados no log (`O voto do eleitor foi computado`): **308,597**
- Votos de presidente no BU: **308,597**
  - nominais **303,180** · brancos **2,176** · nulos **3,241**

**+33** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**308,597** = **308,597**). O +33 está fora dessa conta.
- **31** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **2** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **286,881** (92.95% do dia)
- Manual: **21,744** (7.05% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **5** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 07h | 33,726 | 10.9276 | oficial | 31,352 | 92.9609 | 2,374 | 7.0391 | 0 | 0.0 | 0 | 0.0 |
| 08h | 47,358 | 15.3446 | oficial | 43,903 | 92.7045 | 3,454 | 7.2934 | 0 | 0.0 | 1 | 0.0021 |
| 09h | 51,889 | 16.8127 | oficial | 48,316 | 93.1141 | 3,572 | 6.8839 | 0 | 0.0 | 1 | 0.0019 |
| 10h | 46,367 | 15.0235 | oficial | 43,222 | 93.2172 | 3,143 | 6.7785 | 0 | 0.0 | 2 | 0.0043 |
| 11h | 35,681 | 11.5611 | oficial | 33,212 | 93.0804 | 2,469 | 6.9196 | 0 | 0.0 | 0 | 0.0 |
| 12h | 25,164 | 8.1535 | oficial | 23,425 | 93.0893 | 1,738 | 6.9067 | 0 | 0.0 | 1 | 0.004 |
| 13h | 21,797 | 7.0625 | oficial | 20,244 | 92.8752 | 1,553 | 7.1248 | 0 | 0.0 | 0 | 0.0 |
| 14h | 24,450 | 7.9221 | oficial | 22,670 | 92.7198 | 1,780 | 7.2802 | 0 | 0.0 | 0 | 0.0 |
| 15h | 22,067 | 7.15 | oficial | 20,420 | 92.5364 | 1,647 | 7.4636 | 0 | 0.0 | 0 | 0.0 |
| 16h | 131 | 0.0424 | pós-encerramento | 117 | 89.313 | 14 | 10.687 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 328,794 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
