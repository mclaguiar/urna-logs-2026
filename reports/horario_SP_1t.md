# Curva horária — SP 1º turno

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

- Habilitações no dia: **26,439,279**
  - **7,287** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **6,158** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **1,129** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **26,342,418** (99.6336%)
- Pós-encerramento ≥17h: **96,861** (% entre oficial+pós: **0.3664**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **103,656** · urnas: **104,073**
- Pico (hora local): **11h** (3,437,597)
- Faixas ≥17h (ref. brasilia): 17–18h **0.3584** · 18–19h **0.0074** · 19h+ **0.0006**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **26,439,279**
- Votos computados no log (`O voto do eleitor foi computado`): **26,431,974**
- Votos de presidente no BU: **26,431,992**
  - nominais **24,884,303** · brancos **632,801** · nulos **914,888**

**+7,287** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**26,431,974**) e votos do BU (**26,431,992**) diferem em **-18**.
- **6,158** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **1,129** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **23,696,041** (89.62% do dia)
- Manual: **2,742,350** (10.37% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **888** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 2,902,498 | 10.978 | oficial | 2,556,392 | 88.0756 | 345,930 | 11.9184 | 0 | 0.0 | 176 | 0.0061 |
| 09h | 3,140,855 | 11.8795 | oficial | 2,786,677 | 88.7235 | 354,090 | 11.2737 | 0 | 0.0 | 88 | 0.0028 |
| 10h | 3,313,353 | 12.5319 | oficial | 2,960,149 | 89.34 | 353,086 | 10.6565 | 0 | 0.0 | 118 | 0.0036 |
| 11h | 3,437,597 | 13.0019 | oficial | 3,094,105 | 90.0078 | 343,397 | 9.9894 | 0 | 0.0 | 95 | 0.0028 |
| 12h | 3,372,614 | 12.7561 | oficial | 3,052,360 | 90.5043 | 320,162 | 9.493 | 0 | 0.0 | 92 | 0.0027 |
| 13h | 3,070,517 | 11.6135 | oficial | 2,776,606 | 90.428 | 293,816 | 9.5689 | 0 | 0.0 | 95 | 0.0031 |
| 14h | 2,760,502 | 10.4409 | oficial | 2,487,348 | 90.1049 | 273,067 | 9.8919 | 0 | 0.0 | 87 | 0.0032 |
| 15h | 2,380,176 | 9.0024 | oficial | 2,135,891 | 89.7367 | 244,216 | 10.2604 | 0 | 0.0 | 69 | 0.0029 |
| 16h | 1,964,306 | 7.4295 | oficial | 1,759,653 | 89.5814 | 204,586 | 10.4152 | 0 | 0.0 | 67 | 0.0034 |
| 17h | 94,748 | 0.3584 | pós-encerramento | 84,956 | 89.6652 | 9,791 | 10.3337 | 0 | 0.0 | 1 | 0.0011 |
| 18h | 1,960 | 0.0074 | pós-encerramento | 1,770 | 90.3061 | 190 | 9.6939 | 0 | 0.0 | 0 | 0.0 |
| 19h | 105 | 0.0004 | pós-encerramento | 96 | 91.4286 | 9 | 8.5714 | 0 | 0.0 | 0 | 0.0 |
| 20h | 33 | 0.0001 | pós-encerramento | 26 | 78.7879 | 7 | 21.2121 | 0 | 0.0 | 0 | 0.0 |
| 21h | 15 | 0.0001 | pós-encerramento | 12 | 80.0 | 3 | 20.0 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
