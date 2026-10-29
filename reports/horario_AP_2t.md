# Curva horária — AP 2º turno

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

- Habilitações no dia: **430,018**
  - **43** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **39** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **4** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **429,890** (99.9702%)
- Pós-encerramento ≥17h: **128** (% entre oficial+pós: **0.0298**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **1,914** · urnas: **1,924**
- Pico (hora local): **8h** (73,361)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0298** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **472,232** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **430,018**
- Votos computados no log (`O voto do eleitor foi computado`): **429,975**
- Votos de presidente no BU: **429,975**
  - nominais **421,642** · brancos **3,320** · nulos **5,013**

**+43** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**429,975** = **429,975**). O +43 está fora dessa conta.
- **39** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **4** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **394,998** (91.86% do dia)
- Manual: **35,013** (8.14% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **7** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 73,361 | 17.06 | oficial | 67,328 | 91.7763 | 6,032 | 8.2224 | 0 | 0.0 | 1 | 0.0014 |
| 09h | 67,818 | 15.771 | oficial | 62,391 | 91.9977 | 5,427 | 8.0023 | 0 | 0.0 | 0 | 0.0 |
| 10h | 63,710 | 14.8157 | oficial | 58,833 | 92.345 | 4,876 | 7.6534 | 0 | 0.0 | 1 | 0.0016 |
| 11h | 51,279 | 11.9248 | oficial | 47,262 | 92.1664 | 4,017 | 7.8336 | 0 | 0.0 | 0 | 0.0 |
| 12h | 36,098 | 8.3945 | oficial | 33,211 | 92.0023 | 2,887 | 7.9977 | 0 | 0.0 | 0 | 0.0 |
| 13h | 31,913 | 7.4213 | oficial | 29,244 | 91.6366 | 2,669 | 8.3634 | 0 | 0.0 | 0 | 0.0 |
| 14h | 34,857 | 8.1059 | oficial | 31,872 | 91.4364 | 2,984 | 8.5607 | 0 | 0.0 | 1 | 0.0029 |
| 15h | 38,121 | 8.865 | oficial | 34,874 | 91.4824 | 3,244 | 8.5097 | 0 | 0.0 | 3 | 0.0079 |
| 16h | 32,733 | 7.612 | oficial | 29,868 | 91.2474 | 2,864 | 8.7496 | 0 | 0.0 | 1 | 0.0031 |
| 17h | 128 | 0.0298 | pós-encerramento | 115 | 89.8438 | 13 | 10.1562 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 472,232 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
