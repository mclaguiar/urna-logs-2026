# Curva horária — SE 1º turno

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

- Habilitações no dia: **1,439,763**
  - **681** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **631** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **50** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **1,397,626** (97.0733%)
- Pós-encerramento ≥17h: **42,137** (% entre oficial+pós: **2.9267**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **5,923** · urnas: **5,959**
- Pico (hora local): **11h** (172,327)
- Faixas ≥17h (ref. brasilia): 17–18h **2.4271** · 18–19h **0.431** · 19h+ **0.0686**

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **1,439,763**
- Votos computados no log (`O voto do eleitor foi computado`): **1,439,082**
- Votos de presidente no BU: **1,439,082**
  - nominais **1,364,253** · brancos **24,859** · nulos **49,970**

**+681** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**1,439,082** = **1,439,082**). O +681 está fora dessa conta.
- **631** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **50** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **1,289,963** (89.6% do dia)
- Manual: **149,762** (10.4% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **38** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 142,585 | 9.9034 | oficial | 126,314 | 88.5886 | 16,263 | 11.4058 | 0 | 0.0 | 8 | 0.0056 |
| 09h | 156,880 | 10.8962 | oficial | 139,267 | 88.7729 | 17,609 | 11.2245 | 0 | 0.0 | 4 | 0.0025 |
| 10h | 166,869 | 11.59 | oficial | 149,115 | 89.3605 | 17,750 | 10.6371 | 0 | 0.0 | 4 | 0.0024 |
| 11h | 172,327 | 11.9691 | oficial | 154,926 | 89.9023 | 17,399 | 10.0965 | 0 | 0.0 | 2 | 0.0012 |
| 12h | 163,869 | 11.3817 | oficial | 147,524 | 90.0256 | 16,340 | 9.9714 | 0 | 0.0 | 5 | 0.0031 |
| 13h | 152,091 | 10.5636 | oficial | 136,742 | 89.908 | 15,343 | 10.088 | 0 | 0.0 | 6 | 0.0039 |
| 14h | 152,658 | 10.603 | oficial | 136,905 | 89.6809 | 15,749 | 10.3165 | 0 | 0.0 | 4 | 0.0026 |
| 15h | 154,827 | 10.7536 | oficial | 138,919 | 89.7253 | 15,906 | 10.2734 | 0 | 0.0 | 2 | 0.0013 |
| 16h | 135,520 | 9.4127 | oficial | 122,114 | 90.1077 | 13,403 | 9.8901 | 0 | 0.0 | 3 | 0.0022 |
| 17h | 34,945 | 2.4271 | pós-encerramento | 31,622 | 90.4908 | 3,323 | 9.5092 | 0 | 0.0 | 0 | 0.0 |
| 18h | 6,205 | 0.431 | pós-encerramento | 5,603 | 90.2981 | 602 | 9.7019 | 0 | 0.0 | 0 | 0.0 |
| 19h | 883 | 0.0613 | pós-encerramento | 813 | 92.0725 | 70 | 7.9275 | 0 | 0.0 | 0 | 0.0 |
| 20h | 102 | 0.0071 | pós-encerramento | 99 | 97.0588 | 3 | 2.9412 | 0 | 0.0 | 0 | 0.0 |
| 21h | 2 | 0.0001 | pós-encerramento | 0 | 0.0 | 2 | 100.0 | 0 | 0.0 | 0 | 0.0 |

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
