# Curva horária — MA 2º turno

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

- Habilitações no dia: **4,128,077**
  - **306** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **290** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **16** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **4,127,259** (99.9802%)
- Pós-encerramento ≥17h: **818** (% entre oficial+pós: **0.0198**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **18,093** · urnas: **18,327**
- Pico (hora local): **8h** (864,459)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0196** · 18–19h **0.0002** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **4,155,161** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **4,128,077**
- Votos computados no log (`O voto do eleitor foi computado`): **4,127,735**
- Votos de presidente no BU: **4,127,771**
  - nominais **4,038,202** · brancos **30,855** · nulos **58,714**

**+306** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**4,127,735**) e votos do BU (**4,127,771**) diferem em **-36**.
- **290** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **16** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **3,717,545** (90.06% do dia)
- Manual: **410,407** (9.94% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **125** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 864,459 | 20.941 | oficial | 780,060 | 90.2368 | 84,363 | 9.7591 | 0 | 0.0 | 36 | 0.0042 |
| 09h | 762,844 | 18.4794 | oficial | 688,477 | 90.2513 | 74,352 | 9.7467 | 0 | 0.0 | 15 | 0.002 |
| 10h | 604,269 | 14.638 | oficial | 544,468 | 90.1036 | 59,787 | 9.8941 | 0 | 0.0 | 14 | 0.0023 |
| 11h | 419,323 | 10.1578 | oficial | 377,254 | 89.9674 | 42,060 | 10.0305 | 0 | 0.0 | 9 | 0.0021 |
| 12h | 320,695 | 7.7686 | oficial | 288,503 | 89.9618 | 32,169 | 10.031 | 0 | 0.0 | 23 | 0.0072 |
| 13h | 315,322 | 7.6385 | oficial | 283,734 | 89.9823 | 31,581 | 10.0155 | 0 | 0.0 | 7 | 0.0022 |
| 14h | 323,418 | 7.8346 | oficial | 290,554 | 89.8385 | 32,857 | 10.1593 | 0 | 0.0 | 7 | 0.0022 |
| 15h | 316,128 | 7.658 | oficial | 284,155 | 89.8861 | 31,964 | 10.1111 | 0 | 0.0 | 9 | 0.0028 |
| 16h | 200,801 | 4.8643 | oficial | 179,668 | 89.4757 | 21,128 | 10.5219 | 0 | 0.0 | 5 | 0.0025 |
| 17h | 808 | 0.0196 | pós-encerramento | 670 | 82.9208 | 138 | 17.0792 | 0 | 0.0 | 0 | 0.0 |
| 18h | 10 | 0.0002 | pós-encerramento | 2 | 20.0 | 8 | 80.0 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 4,155,161 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
