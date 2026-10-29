# Curva horária — SE 2º turno

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

- Habilitações no dia: **1,466,760**
  - **101** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **93** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **8** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **1,466,506** (99.9827%)
- Pós-encerramento ≥17h: **254** (% entre oficial+pós: **0.0173**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **5,923** · urnas: **6,037**
- Pico (hora local): **8h** (269,945)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0168** · 18–19h **0.0005** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **1,434,112** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **1,466,760**
- Votos computados no log (`O voto do eleitor foi computado`): **1,466,659**
- Votos de presidente no BU: **1,466,659**
  - nominais **1,422,395** · brancos **13,135** · nulos **31,129**

**+101** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**1,466,659** = **1,466,659**). O +101 está fora dessa conta.
- **93** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **8** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **1,311,670** (89.43% do dia)
- Manual: **155,038** (10.57% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **52** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 269,945 | 18.4042 | oficial | 241,114 | 89.3197 | 28,817 | 10.6751 | 0 | 0.0 | 14 | 0.0052 |
| 09h | 244,522 | 16.6709 | oficial | 217,887 | 89.1073 | 26,630 | 10.8906 | 0 | 0.0 | 5 | 0.002 |
| 10h | 226,063 | 15.4124 | oficial | 202,113 | 89.4056 | 23,942 | 10.5909 | 0 | 0.0 | 8 | 0.0035 |
| 11h | 177,468 | 12.0993 | oficial | 159,249 | 89.7339 | 18,217 | 10.2649 | 0 | 0.0 | 2 | 0.0011 |
| 12h | 119,863 | 8.172 | oficial | 107,449 | 89.6432 | 12,409 | 10.3527 | 0 | 0.0 | 5 | 0.0042 |
| 13h | 104,063 | 7.0948 | oficial | 93,066 | 89.4324 | 10,997 | 10.5676 | 0 | 0.0 | 0 | 0.0 |
| 14h | 114,891 | 7.833 | oficial | 102,661 | 89.3551 | 12,224 | 10.6396 | 0 | 0.0 | 6 | 0.0052 |
| 15h | 121,444 | 8.2797 | oficial | 108,596 | 89.4206 | 12,838 | 10.5711 | 0 | 0.0 | 10 | 0.0082 |
| 16h | 88,247 | 6.0165 | oficial | 79,316 | 89.8795 | 8,929 | 10.1182 | 0 | 0.0 | 2 | 0.0023 |
| 17h | 247 | 0.0168 | pós-encerramento | 213 | 86.2348 | 34 | 13.7652 | 0 | 0.0 | 0 | 0.0 |
| 18h | 7 | 0.0005 | pós-encerramento | 6 | 85.7143 | 1 | 14.2857 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 1,434,112 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
