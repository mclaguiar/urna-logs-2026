# Curva horária — PB 1º turno

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

- Habilitações no dia: **2,685,567**
  - **1,579** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **1,465** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **114** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **2,579,506** (96.0507%)
- Pós-encerramento ≥17h: **106,061** (% entre oficial+pós: **3.9493**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **10,712** · urnas: **10,766**
- Pico (hora local): **11h** (304,359)
- Faixas ≥17h (ref. brasilia): 17–18h **3.3701** · 18–19h **0.526** · 19h+ **0.0532**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **2,685,567**
- Votos computados no log (`O voto do eleitor foi computado`): **2,683,988**
- Votos de presidente no BU: **2,683,988**
  - nominais **2,513,837** · brancos **52,297** · nulos **117,854**

**+1,579** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**2,683,988** = **2,683,988**). O +1,579 está fora dessa conta.
- **1,465** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **114** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **2,417,130** (90.0% do dia)
- Manual: **268,345** (9.99% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **92** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 246,782 | 9.1892 | oficial | 217,191 | 88.0093 | 29,576 | 11.9847 | 0 | 0.0 | 15 | 0.0061 |
| 09h | 272,043 | 10.1298 | oficial | 241,395 | 88.7341 | 30,644 | 11.2644 | 0 | 0.0 | 4 | 0.0015 |
| 10h | 291,872 | 10.8682 | oficial | 261,099 | 89.4567 | 30,768 | 10.5416 | 0 | 0.0 | 5 | 0.0017 |
| 11h | 304,359 | 11.3331 | oficial | 274,577 | 90.2148 | 29,775 | 9.7829 | 0 | 0.0 | 7 | 0.0023 |
| 12h | 303,076 | 11.2854 | oficial | 274,832 | 90.6809 | 28,231 | 9.3148 | 0 | 0.0 | 13 | 0.0043 |
| 13h | 295,103 | 10.9885 | oficial | 267,214 | 90.5494 | 27,876 | 9.4462 | 0 | 0.0 | 13 | 0.0044 |
| 14h | 292,597 | 10.8952 | oficial | 264,292 | 90.3263 | 28,299 | 9.6717 | 0 | 0.0 | 6 | 0.0021 |
| 15h | 296,021 | 11.0227 | oficial | 267,046 | 90.2118 | 28,967 | 9.7855 | 0 | 0.0 | 8 | 0.0027 |
| 16h | 277,653 | 10.3387 | oficial | 252,339 | 90.8829 | 25,299 | 9.1117 | 0 | 0.0 | 15 | 0.0054 |
| 17h | 90,507 | 3.3701 | pós-encerramento | 82,887 | 91.5808 | 7,618 | 8.417 | 0 | 0.0 | 2 | 0.0022 |
| 18h | 14,125 | 0.526 | pós-encerramento | 12,953 | 91.7027 | 1,169 | 8.2761 | 0 | 0.0 | 3 | 0.0212 |
| 19h | 1,327 | 0.0494 | pós-encerramento | 1,212 | 91.3338 | 115 | 8.6662 | 0 | 0.0 | 0 | 0.0 |
| 20h | 101 | 0.0038 | pós-encerramento | 92 | 91.0891 | 8 | 7.9208 | 0 | 0.0 | 1 | 0.9901 |
| 21h | 1 | 0.0 | pós-encerramento | 1 | 100.0 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
