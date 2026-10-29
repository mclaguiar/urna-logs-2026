# Curva horária — CE 2º turno

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

- Habilitações no dia: **6,025,338**
  - **495** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **447** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **48** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **6,024,377** (99.9841%)
- Pós-encerramento ≥17h: **961** (% entre oficial+pós: **0.0159**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **23,765** · urnas: **23,935**
- Pico (hora local): **8h** (1,169,866)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0159** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **5,889,644** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **6,025,338**
- Votos computados no log (`O voto do eleitor foi computado`): **6,024,843**
- Votos de presidente no BU: **6,024,843**
  - nominais **5,855,602** · brancos **56,386** · nulos **112,855**

**+495** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**6,024,843** = **6,024,843**). O +495 está fora dessa conta.
- **447** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **48** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **5,352,312** (88.83% do dia)
- Manual: **672,843** (11.17% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **183** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 1,169,866 | 19.4158 | oficial | 1,033,924 | 88.3797 | 135,901 | 11.6168 | 0 | 0.0 | 41 | 0.0035 |
| 09h | 1,052,635 | 17.4701 | oficial | 933,593 | 88.691 | 119,007 | 11.3056 | 0 | 0.0 | 35 | 0.0033 |
| 10h | 902,826 | 14.9838 | oficial | 803,859 | 89.0381 | 98,940 | 10.9589 | 0 | 0.0 | 27 | 0.003 |
| 11h | 666,950 | 11.0691 | oficial | 596,074 | 89.3731 | 70,859 | 10.6243 | 0 | 0.0 | 17 | 0.0025 |
| 12h | 494,098 | 8.2003 | oficial | 441,716 | 89.3985 | 52,370 | 10.5991 | 0 | 0.0 | 12 | 0.0024 |
| 13h | 443,333 | 7.3578 | oficial | 394,610 | 89.0098 | 48,711 | 10.9875 | 0 | 0.0 | 12 | 0.0027 |
| 14h | 456,994 | 7.5845 | oficial | 405,174 | 88.6607 | 51,803 | 11.3356 | 0 | 0.0 | 17 | 0.0037 |
| 15h | 499,250 | 8.2858 | oficial | 442,540 | 88.641 | 56,703 | 11.3576 | 0 | 0.0 | 7 | 0.0014 |
| 16h | 338,425 | 5.6167 | oficial | 300,012 | 88.6495 | 38,398 | 11.3461 | 0 | 0.0 | 15 | 0.0044 |
| 17h | 960 | 0.0159 | pós-encerramento | 809 | 84.2708 | 151 | 15.7292 | 0 | 0.0 | 0 | 0.0 |
| 18h | 1 | 0.0 | pós-encerramento | 1 | 100.0 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 5,889,644 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
