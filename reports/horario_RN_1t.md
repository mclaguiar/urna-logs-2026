# Curva horária — RN 1º turno

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

- Habilitações no dia: **2,171,959**
  - **946** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **855** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **91** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **2,030,101** (93.4687%)
- Pós-encerramento ≥17h: **141,858** (% entre oficial+pós: **6.5313**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **8,115** · urnas: **8,140**
- Pico (hora local): **12h** (238,194)
- Faixas ≥17h (ref. brasilia): 17–18h **5.0376** · 18–19h **1.3137** · 19h+ **0.1801**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **2,171,959**
- Votos computados no log (`O voto do eleitor foi computado`): **2,171,012**
- Votos de presidente no BU: **2,171,013**
  - nominais **2,071,961** · brancos **33,172** · nulos **65,880**

**+946** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**2,171,012**) e votos do BU (**2,171,013**) diferem em **-1**.
- **855** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **91** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **1,918,638** (88.34% do dia)
- Manual: **253,240** (11.66% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **81** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 192,866 | 8.8798 | oficial | 165,951 | 86.0447 | 26,904 | 13.9496 | 0 | 0.0 | 11 | 0.0057 |
| 09h | 214,169 | 9.8606 | oficial | 186,283 | 86.9794 | 27,876 | 13.0159 | 0 | 0.0 | 10 | 0.0047 |
| 10h | 228,126 | 10.5032 | oficial | 200,236 | 87.7743 | 27,880 | 12.2213 | 0 | 0.0 | 10 | 0.0044 |
| 11h | 237,997 | 10.9577 | oficial | 211,106 | 88.7011 | 26,884 | 11.2959 | 0 | 0.0 | 7 | 0.0029 |
| 12h | 238,194 | 10.9668 | oficial | 212,033 | 89.0169 | 26,152 | 10.9793 | 0 | 0.0 | 9 | 0.0038 |
| 13h | 234,047 | 10.7758 | oficial | 208,415 | 89.0484 | 25,622 | 10.9474 | 0 | 0.0 | 10 | 0.0043 |
| 14h | 229,224 | 10.5538 | oficial | 203,174 | 88.6356 | 26,041 | 11.3605 | 0 | 0.0 | 9 | 0.0039 |
| 15h | 230,447 | 10.6101 | oficial | 203,955 | 88.5041 | 26,486 | 11.4933 | 0 | 0.0 | 6 | 0.0026 |
| 16h | 225,031 | 10.3607 | oficial | 200,123 | 88.9313 | 24,906 | 11.0678 | 0 | 0.0 | 2 | 0.0009 |
| 17h | 109,415 | 5.0376 | pós-encerramento | 98,315 | 89.8551 | 11,094 | 10.1394 | 0 | 0.0 | 6 | 0.0055 |
| 18h | 28,532 | 1.3137 | pós-encerramento | 25,565 | 89.6011 | 2,966 | 10.3953 | 0 | 0.0 | 1 | 0.0035 |
| 19h | 3,595 | 0.1655 | pós-encerramento | 3,191 | 88.7622 | 404 | 11.2378 | 0 | 0.0 | 0 | 0.0 |
| 20h | 251 | 0.0116 | pós-encerramento | 227 | 90.4382 | 24 | 9.5618 | 0 | 0.0 | 0 | 0.0 |
| 21h | 65 | 0.003 | pós-encerramento | 64 | 98.4615 | 1 | 1.5385 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
