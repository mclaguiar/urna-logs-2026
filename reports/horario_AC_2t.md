# Curva horária — AC 2º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-5).
Critério: janela **8h–17h Brasília** (local +2h → BRT); ≥17h = pós-encerramento (fila).

Métricas deste relatório = **somente o dia oficial deste turno**.
Janelas no dia: **oficial** [8h,17h) · **pós-encerramento** ≥17h · **fora do previsto** &lt;8h.
Eventos de **outra data** no `.jez` = histórico (não entram nos totais nem no comparativo 1º×2º).
Dia oficial deste turno: **2026-10-25**.

## Resumo (só o dia do turno)

- Habilitações no dia: **453,714**
  - **60** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **53** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **7** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **453,587** (99.972%)
- Pós-encerramento ≥17h: **127** (% entre oficial+pós: **0.028**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **2,270** · urnas: **2,279**
- Pico (hora local): **6h** (68,717)
- Faixas ≥17h (ref. brasilia): 17–18h **0.028** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **484,471** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **453,714**
- Votos computados no log (`O voto do eleitor foi computado`): **453,654**
- Votos de presidente no BU: **453,654**
  - nominais **432,228** · brancos **5,016** · nulos **16,410**

**+60** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**453,654** = **453,654**). O +60 está fora dessa conta.
- **53** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **7** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **415,709** (91.62% do dia)
- Manual: **37,990** (8.37% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **15** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 06h | 68,717 | 15.1454 | oficial | 63,132 | 91.8725 | 5,585 | 8.1275 | 0 | 0.0 | 0 | 0.0 |
| 07h | 61,974 | 13.6593 | oficial | 56,459 | 91.1011 | 5,514 | 8.8973 | 0 | 0.0 | 1 | 0.0016 |
| 08h | 66,426 | 14.6405 | oficial | 60,755 | 91.4627 | 5,669 | 8.5343 | 0 | 0.0 | 2 | 0.003 |
| 09h | 65,101 | 14.3485 | oficial | 59,683 | 91.6775 | 5,416 | 8.3194 | 0 | 0.0 | 2 | 0.0031 |
| 10h | 56,343 | 12.4182 | oficial | 51,742 | 91.8339 | 4,597 | 8.159 | 0 | 0.0 | 4 | 0.0071 |
| 11h | 42,304 | 9.3239 | oficial | 39,004 | 92.1993 | 3,298 | 7.796 | 0 | 0.0 | 2 | 0.0047 |
| 12h | 33,067 | 7.2881 | oficial | 30,256 | 91.4991 | 2,809 | 8.4949 | 0 | 0.0 | 2 | 0.006 |
| 13h | 32,515 | 7.1664 | oficial | 29,745 | 91.4809 | 2,769 | 8.5161 | 0 | 0.0 | 1 | 0.0031 |
| 14h | 27,140 | 5.9817 | oficial | 24,824 | 91.4665 | 2,315 | 8.5298 | 0 | 0.0 | 1 | 0.0037 |
| 15h | 127 | 0.028 | pós-encerramento | 109 | 85.8268 | 18 | 14.1732 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 484,471 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
