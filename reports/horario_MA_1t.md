# Curva horária — MA 1º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério: janela **8h–17h Brasília**; ≥17h = pós-encerramento (fila).

Métricas deste relatório = **somente o dia oficial deste turno**.
Janelas no dia: **oficial** [8h,17h) · **pós-encerramento** ≥17h · **fora do previsto** &lt;8h.
Eventos de **outra data** no `.jez` = histórico (não entram nos totais nem no comparativo 1º×2º).
Dia oficial deste turno: **2026-10-04**.

## Resumo (só o dia do turno)

- Habilitações no dia: **4,162,525**
  - **2,182** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **1,977** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **205** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **3,922,212** (94.2267%)
- Pós-encerramento ≥17h: **240,313** (% entre oficial+pós: **5.7733**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **18,093** · urnas: **18,178**
- Pico (hora local): **11h** (461,412)
- Faixas ≥17h (ref. brasilia): 17–18h **4.3093** · 18–19h **1.2211** · 19h+ **0.2429**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **4,162,525**
- Votos computados no log (`O voto do eleitor foi computado`): **4,160,343**
- Votos de presidente no BU: **4,160,343**
  - nominais **4,010,784** · brancos **46,315** · nulos **103,244**

**+2,182** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**4,160,343** = **4,160,343**). O +2,182 está fora dessa conta.
- **1,977** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **205** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **3,759,621** (90.32% do dia)
- Manual: **402,776** (9.68% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **128** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 374,464 | 8.9961 | oficial | 335,524 | 89.6011 | 38,916 | 10.3925 | 0 | 0.0 | 24 | 0.0064 |
| 09h | 427,422 | 10.2683 | oficial | 383,540 | 89.7333 | 43,875 | 10.265 | 0 | 0.0 | 7 | 0.0016 |
| 10h | 456,631 | 10.97 | oficial | 412,035 | 90.2337 | 44,584 | 9.7637 | 0 | 0.0 | 12 | 0.0026 |
| 11h | 461,412 | 11.0849 | oficial | 417,777 | 90.5432 | 43,624 | 9.4545 | 0 | 0.0 | 11 | 0.0024 |
| 12h | 446,517 | 10.7271 | oficial | 404,660 | 90.6259 | 41,843 | 9.371 | 0 | 0.0 | 14 | 0.0031 |
| 13h | 446,732 | 10.7322 | oficial | 404,468 | 90.5393 | 42,249 | 9.4573 | 0 | 0.0 | 15 | 0.0034 |
| 14h | 446,811 | 10.7341 | oficial | 403,828 | 90.38 | 42,970 | 9.617 | 0 | 0.0 | 13 | 0.0029 |
| 15h | 446,179 | 10.719 | oficial | 403,763 | 90.4935 | 42,404 | 9.5038 | 0 | 0.0 | 12 | 0.0027 |
| 16h | 416,044 | 9.995 | oficial | 376,334 | 90.4553 | 39,699 | 9.542 | 0 | 0.0 | 11 | 0.0026 |
| 17h | 179,375 | 4.3093 | pós-encerramento | 162,572 | 90.6325 | 16,795 | 9.3631 | 0 | 0.0 | 8 | 0.0045 |
| 18h | 50,829 | 1.2211 | pós-encerramento | 45,990 | 90.4798 | 4,838 | 9.5182 | 0 | 0.0 | 1 | 0.002 |
| 19h | 8,687 | 0.2087 | pós-encerramento | 7,860 | 90.48 | 827 | 9.52 | 0 | 0.0 | 0 | 0.0 |
| 20h | 1,219 | 0.0293 | pós-encerramento | 1,090 | 89.4176 | 129 | 10.5824 | 0 | 0.0 | 0 | 0.0 |
| 21h | 179 | 0.0043 | pós-encerramento | 158 | 88.2682 | 21 | 11.7318 | 0 | 0.0 | 0 | 0.0 |
| 22h | 24 | 0.0006 | pós-encerramento | 22 | 91.6667 | 2 | 8.3333 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
