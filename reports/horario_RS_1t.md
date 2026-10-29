# Curva horária — RS 1º turno

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

- Habilitações no dia: **6,704,686**
  - **1,783** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **1,410** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **373** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **6,673,469** (99.5344%)
- Pós-encerramento ≥17h: **31,217** (% entre oficial+pós: **0.4656**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **27,547** · urnas: **27,677**
- Pico (hora local): **11h** (871,594)
- Faixas ≥17h (ref. brasilia): 17–18h **0.4437** · 18–19h **0.0204** · 19h+ **0.0015**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **6,704,686**
- Votos computados no log (`O voto do eleitor foi computado`): **6,702,992**
- Votos de presidente no BU: **6,702,903**
  - nominais **6,423,299** · brancos **148,339** · nulos **131,265**

**+1,783** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**6,702,992**) e votos do BU (**6,702,903**) diferem em **+89**.
- **1,410** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **373** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **5,622,086** (83.85% do dia)
- Manual: **1,082,418** (16.14% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **182** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 669,940 | 9.9921 | oficial | 554,792 | 82.8122 | 115,106 | 17.1815 | 0 | 0.0 | 42 | 0.0063 |
| 09h | 769,635 | 11.4791 | oficial | 640,510 | 83.2226 | 129,107 | 16.7751 | 0 | 0.0 | 18 | 0.0023 |
| 10h | 853,444 | 12.7291 | oficial | 717,317 | 84.0497 | 136,100 | 15.9472 | 0 | 0.0 | 27 | 0.0032 |
| 11h | 871,594 | 12.9998 | oficial | 737,036 | 84.5618 | 134,547 | 15.4369 | 0 | 0.0 | 11 | 0.0013 |
| 12h | 810,676 | 12.0912 | oficial | 683,736 | 84.3415 | 126,925 | 15.6567 | 0 | 0.0 | 15 | 0.0019 |
| 13h | 767,401 | 11.4457 | oficial | 644,826 | 84.0273 | 122,554 | 15.97 | 0 | 0.0 | 21 | 0.0027 |
| 14h | 754,811 | 11.258 | oficial | 633,190 | 83.8872 | 121,605 | 16.1107 | 0 | 0.0 | 16 | 0.0021 |
| 15h | 682,588 | 10.1808 | oficial | 571,705 | 83.7555 | 110,866 | 16.242 | 0 | 0.0 | 17 | 0.0025 |
| 16h | 493,380 | 7.3587 | oficial | 412,680 | 83.6434 | 80,686 | 16.3537 | 0 | 0.0 | 14 | 0.0028 |
| 17h | 29,748 | 0.4437 | pós-encerramento | 25,078 | 84.3015 | 4,669 | 15.6952 | 0 | 0.0 | 1 | 0.0034 |
| 18h | 1,369 | 0.0204 | pós-encerramento | 1,151 | 84.076 | 218 | 15.924 | 0 | 0.0 | 0 | 0.0 |
| 19h | 88 | 0.0013 | pós-encerramento | 56 | 63.6364 | 32 | 36.3636 | 0 | 0.0 | 0 | 0.0 |
| 20h | 12 | 0.0002 | pós-encerramento | 9 | 75.0 | 3 | 25.0 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
