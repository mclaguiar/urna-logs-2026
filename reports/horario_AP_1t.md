# Curva horária — AP 1º turno

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

- Habilitações no dia: **476,856**
  - **294** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **278** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **16** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **451,274** (94.6353%)
- Pós-encerramento ≥17h: **25,582** (% entre oficial+pós: **5.3647**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **1,914** · urnas: **1,917**
- Pico (hora local): **11h** (53,947)
- Faixas ≥17h (ref. brasilia): 17–18h **4.438** · 18–19h **0.8692** · 19h+ **0.0575**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **476,856**
- Votos computados no log (`O voto do eleitor foi computado`): **476,562**
- Votos de presidente no BU: **476,562**
  - nominais **464,875** · brancos **4,415** · nulos **7,272**

**+294** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**476,562** = **476,562**). O +294 está fora dessa conta.
- **278** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
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

- Com digital: **438,059** (91.86% do dia)
- Manual: **38,787** (8.13% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **10** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 43,329 | 9.0864 | oficial | 39,418 | 90.9737 | 3,910 | 9.024 | 0 | 0.0 | 1 | 0.0023 |
| 09h | 48,795 | 10.2326 | oficial | 44,729 | 91.6672 | 4,066 | 8.3328 | 0 | 0.0 | 0 | 0.0 |
| 10h | 52,089 | 10.9234 | oficial | 47,798 | 91.7622 | 4,291 | 8.2378 | 0 | 0.0 | 0 | 0.0 |
| 11h | 53,947 | 11.3131 | oficial | 49,669 | 92.07 | 4,277 | 7.9282 | 0 | 0.0 | 1 | 0.0019 |
| 12h | 51,019 | 10.699 | oficial | 46,904 | 91.9344 | 4,115 | 8.0656 | 0 | 0.0 | 0 | 0.0 |
| 13h | 48,773 | 10.228 | oficial | 44,856 | 91.9689 | 3,915 | 8.027 | 0 | 0.0 | 2 | 0.0041 |
| 14h | 50,106 | 10.5076 | oficial | 46,099 | 92.003 | 4,003 | 7.9891 | 0 | 0.0 | 4 | 0.008 |
| 15h | 51,339 | 10.7661 | oficial | 47,209 | 91.9554 | 4,130 | 8.0446 | 0 | 0.0 | 0 | 0.0 |
| 16h | 51,877 | 10.879 | oficial | 47,864 | 92.2644 | 4,012 | 7.7337 | 0 | 0.0 | 1 | 0.0019 |
| 17h | 21,163 | 4.438 | pós-encerramento | 19,426 | 91.7923 | 1,736 | 8.203 | 0 | 0.0 | 1 | 0.0047 |
| 18h | 4,145 | 0.8692 | pós-encerramento | 3,834 | 92.497 | 311 | 7.503 | 0 | 0.0 | 0 | 0.0 |
| 19h | 271 | 0.0568 | pós-encerramento | 250 | 92.2509 | 21 | 7.7491 | 0 | 0.0 | 0 | 0.0 |
| 20h | 3 | 0.0006 | pós-encerramento | 3 | 100.0 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
