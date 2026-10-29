# Curva horária — AM 2º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-4).
Critério: janela **8h–17h Brasília** (local +1h → BRT); ≥17h = pós-encerramento (fila).

Métricas deste relatório = **somente o dia oficial deste turno**.
Janelas no dia: **oficial** [8h,17h) · **pós-encerramento** ≥17h · **fora do previsto** &lt;8h.
Eventos de **outra data** no `.jez` = histórico (não entram nos totais nem no comparativo 1º×2º).
Dia oficial deste turno: **2026-10-25**.

## Resumo (só o dia do turno)

- Habilitações no dia: **2,192,230**
  - **171** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **154** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **17** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **2,165,302** (98.7717%)
- Pós-encerramento ≥17h: **819** (% entre oficial+pós: **0.0378**)
- Fora do previsto (&lt;8h no dia): **26,109** (1.191%)
- Seções: **8,157** · urnas: **8,233**
- Pico (hora local): **8h** (341,845)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0378** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **2,229,394** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **2,192,230**
- Votos computados no log (`O voto do eleitor foi computado`): **2,192,059**
- Votos de presidente no BU: **2,192,059**
  - nominais **2,121,028** · brancos **18,324** · nulos **52,707**

**+171** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**2,192,059** = **2,192,059**). O +171 está fora dessa conta.
- **154** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **17** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **1,978,050** (90.23% do dia)
- Manual: **214,081** (9.77% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **99** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 06h | 26,109 | 1.191 | fora (<8h) | 23,798 | 91.1486 | 2,311 | 8.8514 | 0 | 0.0 | 0 | 0.0 |
| 07h | 337,778 | 15.408 | oficial | 305,678 | 90.4967 | 32,076 | 9.4962 | 0 | 0.0 | 24 | 0.0071 |
| 08h | 341,845 | 15.5935 | oficial | 308,926 | 90.3702 | 32,902 | 9.6248 | 0 | 0.0 | 17 | 0.005 |
| 09h | 335,332 | 15.2964 | oficial | 303,678 | 90.5604 | 31,646 | 9.4372 | 0 | 0.0 | 8 | 0.0024 |
| 10h | 292,250 | 13.3312 | oficial | 264,296 | 90.4349 | 27,944 | 9.5617 | 0 | 0.0 | 10 | 0.0034 |
| 11h | 227,393 | 10.3727 | oficial | 205,200 | 90.2402 | 22,180 | 9.754 | 0 | 0.0 | 13 | 0.0057 |
| 12h | 180,985 | 8.2557 | oficial | 162,673 | 89.882 | 18,307 | 10.1152 | 0 | 0.0 | 5 | 0.0028 |
| 13h | 171,865 | 7.8397 | oficial | 154,592 | 89.9497 | 17,264 | 10.0451 | 0 | 0.0 | 9 | 0.0052 |
| 14h | 164,943 | 7.524 | oficial | 147,638 | 89.5085 | 17,300 | 10.4885 | 0 | 0.0 | 5 | 0.003 |
| 15h | 112,911 | 5.1505 | oficial | 100,869 | 89.335 | 12,034 | 10.658 | 0 | 0.0 | 8 | 0.0071 |
| 16h | 819 | 0.0374 | pós-encerramento | 702 | 85.7143 | 117 | 14.2857 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 2,229,394 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
