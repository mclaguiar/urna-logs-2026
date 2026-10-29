# Curva horária — PI 2º turno

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

- Habilitações no dia: **2,240,076**
  - **246** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **214** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **32** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **2,239,778** (99.9867%)
- Pós-encerramento ≥17h: **298** (% entre oficial+pós: **0.0133**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **10,225** · urnas: **10,321**
- Pico (hora local): **8h** (470,363)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0133** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **2,236,212** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **2,240,076**
- Votos computados no log (`O voto do eleitor foi computado`): **2,239,829**
- Votos de presidente no BU: **2,239,830**
  - nominais **2,179,848** · brancos **16,137** · nulos **43,845**

**+246** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**2,239,829**) e votos do BU (**2,239,830**) diferem em **-1**.
- **214** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **32** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **1,993,587** (89.0% do dia)
- Manual: **246,401** (11.0% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **88** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 470,363 | 20.9976 | oficial | 413,613 | 87.9349 | 56,731 | 12.0611 | 0 | 0.0 | 19 | 0.004 |
| 09h | 411,171 | 18.3552 | oficial | 364,346 | 88.6118 | 46,814 | 11.3855 | 0 | 0.0 | 11 | 0.0027 |
| 10h | 326,915 | 14.5939 | oficial | 291,894 | 89.2874 | 35,003 | 10.7071 | 0 | 0.0 | 18 | 0.0055 |
| 11h | 230,913 | 10.3083 | oficial | 207,038 | 89.6606 | 23,863 | 10.3342 | 0 | 0.0 | 12 | 0.0052 |
| 12h | 169,538 | 7.5684 | oficial | 152,166 | 89.7533 | 17,367 | 10.2437 | 0 | 0.0 | 5 | 0.0029 |
| 13h | 154,298 | 6.8881 | oficial | 137,932 | 89.3933 | 16,362 | 10.6042 | 0 | 0.0 | 4 | 0.0026 |
| 14h | 166,662 | 7.44 | oficial | 148,587 | 89.1547 | 18,068 | 10.8411 | 0 | 0.0 | 7 | 0.0042 |
| 15h | 182,644 | 8.1535 | oficial | 163,363 | 89.4434 | 19,274 | 10.5528 | 0 | 0.0 | 7 | 0.0038 |
| 16h | 127,274 | 5.6817 | oficial | 114,398 | 89.8832 | 12,871 | 10.1128 | 0 | 0.0 | 5 | 0.0039 |
| 17h | 297 | 0.0133 | pós-encerramento | 249 | 83.8384 | 48 | 16.1616 | 0 | 0.0 | 0 | 0.0 |
| 18h | 1 | 0.0 | pós-encerramento | 1 | 100.0 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 2,236,212 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
