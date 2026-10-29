# Curva horária — TO 1º turno

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

- Habilitações no dia: **965,768**
  - **572** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **541** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **31** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **950,764** (98.4464%)
- Pós-encerramento ≥17h: **15,004** (% entre oficial+pós: **1.5536**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **4,384** · urnas: **4,388**
- Pico (hora local): **11h** (118,730)
- Faixas ≥17h (ref. brasilia): 17–18h **1.4393** · 18–19h **0.1087** · 19h+ **0.0056**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **965,768**
- Votos computados no log (`O voto do eleitor foi computado`): **965,196**
- Votos de presidente no BU: **965,196**
  - nominais **930,475** · brancos **8,344** · nulos **26,377**

**+572** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**965,196** = **965,196**). O +572 está fora dessa conta.
- **541** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **31** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **887,279** (91.87% do dia)
- Manual: **78,464** (8.12% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **25** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 92,963 | 9.6258 | oficial | 84,255 | 90.6328 | 8,705 | 9.3639 | 0 | 0.0 | 3 | 0.0032 |
| 09h | 107,644 | 11.1459 | oficial | 98,082 | 91.117 | 9,560 | 8.8811 | 0 | 0.0 | 2 | 0.0019 |
| 10h | 116,492 | 12.0621 | oficial | 106,933 | 91.7943 | 9,555 | 8.2023 | 0 | 0.0 | 4 | 0.0034 |
| 11h | 118,730 | 12.2938 | oficial | 109,946 | 92.6017 | 8,780 | 7.3949 | 0 | 0.0 | 4 | 0.0034 |
| 12h | 111,341 | 11.5288 | oficial | 102,991 | 92.5005 | 8,345 | 7.495 | 0 | 0.0 | 5 | 0.0045 |
| 13h | 105,353 | 10.9087 | oficial | 97,057 | 92.1255 | 8,295 | 7.8735 | 0 | 0.0 | 1 | 0.0009 |
| 14h | 103,295 | 10.6956 | oficial | 95,083 | 92.05 | 8,212 | 7.95 | 0 | 0.0 | 0 | 0.0 |
| 15h | 102,419 | 10.6049 | oficial | 94,006 | 91.7857 | 8,410 | 8.2114 | 0 | 0.0 | 3 | 0.0029 |
| 16h | 92,527 | 9.5807 | oficial | 85,136 | 92.0121 | 7,388 | 7.9847 | 0 | 0.0 | 3 | 0.0032 |
| 17h | 13,900 | 1.4393 | pós-encerramento | 12,780 | 91.9424 | 1,120 | 8.0576 | 0 | 0.0 | 0 | 0.0 |
| 18h | 1,050 | 0.1087 | pós-encerramento | 963 | 91.7143 | 87 | 8.2857 | 0 | 0.0 | 0 | 0.0 |
| 19h | 54 | 0.0056 | pós-encerramento | 47 | 87.037 | 7 | 12.963 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
