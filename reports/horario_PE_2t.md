# Curva horária — PE 2º turno

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

- Habilitações no dia: **6,127,096**
  - **629** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **552** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **77** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **6,125,515** (99.9742%)
- Pós-encerramento ≥17h: **1,581** (% entre oficial+pós: **0.0258**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **21,418** · urnas: **21,607**
- Pico (hora local): **8h** (1,155,170)
- Faixas ≥17h (ref. brasilia): 17–18h **0.024** · 18–19h **0.0018** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **5,892,279** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **6,127,096**
- Votos computados no log (`O voto do eleitor foi computado`): **6,126,467**
- Votos de presidente no BU: **6,126,467**
  - nominais **5,950,067** · brancos **56,758** · nulos **119,642**

**+629** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**6,126,467** = **6,126,467**). O +629 está fora dessa conta.
- **552** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **77** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **5,249,012** (85.67% do dia)
- Manual: **877,873** (14.33% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **211** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 1,155,170 | 18.8535 | oficial | 997,288 | 86.3326 | 157,838 | 13.6636 | 0 | 0.0 | 44 | 0.0038 |
| 09h | 1,039,077 | 16.9587 | oficial | 893,243 | 85.965 | 145,799 | 14.0316 | 0 | 0.0 | 35 | 0.0034 |
| 10h | 933,300 | 15.2323 | oficial | 801,255 | 85.8518 | 132,011 | 14.1445 | 0 | 0.0 | 34 | 0.0036 |
| 11h | 728,361 | 11.8875 | oficial | 624,091 | 85.6843 | 104,247 | 14.3125 | 0 | 0.0 | 23 | 0.0032 |
| 12h | 534,015 | 8.7156 | oficial | 457,803 | 85.7285 | 76,193 | 14.268 | 0 | 0.0 | 19 | 0.0036 |
| 13h | 454,549 | 7.4187 | oficial | 387,878 | 85.3325 | 66,663 | 14.6657 | 0 | 0.0 | 8 | 0.0018 |
| 14h | 468,083 | 7.6396 | oficial | 397,872 | 85.0003 | 70,191 | 14.9954 | 0 | 0.0 | 20 | 0.0043 |
| 15h | 482,313 | 7.8718 | oficial | 408,926 | 84.7844 | 73,367 | 15.2115 | 0 | 0.0 | 20 | 0.0041 |
| 16h | 330,647 | 5.3965 | oficial | 279,380 | 84.4949 | 51,259 | 15.5026 | 0 | 0.0 | 8 | 0.0024 |
| 17h | 1,468 | 0.024 | pós-encerramento | 1,183 | 80.5858 | 285 | 19.4142 | 0 | 0.0 | 0 | 0.0 |
| 18h | 111 | 0.0018 | pós-encerramento | 91 | 81.982 | 20 | 18.018 | 0 | 0.0 | 0 | 0.0 |
| 19h | 2 | 0.0 | pós-encerramento | 2 | 100.0 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 5,892,279 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
