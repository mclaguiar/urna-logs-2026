# Curva horária — TO 2º turno

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

- Habilitações no dia: **954,857**
  - **94** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **80** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **14** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **954,676** (99.981%)
- Pós-encerramento ≥17h: **181** (% entre oficial+pós: **0.019**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **4,384** · urnas: **4,389**
- Pico (hora local): **8h** (185,663)
- Faixas ≥17h (ref. brasilia): 17–18h **0.019** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **960,372** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **954,857**
- Votos computados no log (`O voto do eleitor foi computado`): **954,763**
- Votos de presidente no BU: **954,763**
  - nominais **910,878** · brancos **8,059** · nulos **35,826**

**+94** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**954,763** = **954,763**). O +94 está fora dessa conta.
- **80** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
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

- Com digital: **881,045** (92.27% do dia)
- Manual: **73,791** (7.73% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **21** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 185,663 | 19.4441 | oficial | 170,969 | 92.0857 | 14,690 | 7.9122 | 0 | 0.0 | 4 | 0.0022 |
| 09h | 164,661 | 17.2446 | oficial | 152,169 | 92.4135 | 12,485 | 7.5822 | 0 | 0.0 | 7 | 0.0043 |
| 10h | 131,489 | 13.7705 | oficial | 121,983 | 92.7705 | 9,505 | 7.2287 | 0 | 0.0 | 1 | 0.0008 |
| 11h | 97,439 | 10.2046 | oficial | 90,305 | 92.6785 | 7,132 | 7.3195 | 0 | 0.0 | 2 | 0.0021 |
| 12h | 77,100 | 8.0745 | oficial | 71,198 | 92.345 | 5,901 | 7.6537 | 0 | 0.0 | 1 | 0.0013 |
| 13h | 76,407 | 8.0019 | oficial | 70,381 | 92.1133 | 6,026 | 7.8867 | 0 | 0.0 | 0 | 0.0 |
| 14h | 81,083 | 8.4916 | oficial | 74,532 | 91.9206 | 6,547 | 8.0744 | 0 | 0.0 | 4 | 0.0049 |
| 15h | 81,848 | 8.5718 | oficial | 75,217 | 91.8984 | 6,631 | 8.1016 | 0 | 0.0 | 0 | 0.0 |
| 16h | 58,986 | 6.1775 | oficial | 54,131 | 91.7692 | 4,853 | 8.2274 | 0 | 0.0 | 2 | 0.0034 |
| 17h | 181 | 0.019 | pós-encerramento | 160 | 88.3978 | 21 | 11.6022 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 960,372 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
