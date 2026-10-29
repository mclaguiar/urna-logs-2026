# Curva horária — RO 2º turno

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

- Habilitações no dia: **988,564**
  - **75** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **67** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **8** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **988,049** (99.9479%)
- Pós-encerramento ≥17h: **515** (% entre oficial+pós: **0.0521**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **4,698** · urnas: **4,729**
- Pico (hora local): **9h** (156,022)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0521** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **987,863** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **988,564**
- Votos computados no log (`O voto do eleitor foi computado`): **988,489**
- Votos de presidente no BU: **988,489**
  - nominais **968,828** · brancos **8,361** · nulos **11,300**

**+75** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Os votos que o log marca como computados fecham com o BU (**988,489** = **988,489**). O +75 está fora dessa conta.
- **67** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
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

- Com digital: **910,644** (92.12% do dia)
- Manual: **77,889** (7.88% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **31** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 07h | 149,887 | 15.1621 | oficial | 136,199 | 90.8678 | 13,682 | 9.1282 | 0 | 0.0 | 6 | 0.004 |
| 08h | 154,571 | 15.6359 | oficial | 141,095 | 91.2817 | 13,468 | 8.7131 | 0 | 0.0 | 8 | 0.0052 |
| 09h | 156,022 | 15.7827 | oficial | 143,882 | 92.219 | 12,133 | 7.7765 | 0 | 0.0 | 7 | 0.0045 |
| 10h | 134,980 | 13.6541 | oficial | 125,240 | 92.7841 | 9,736 | 7.2129 | 0 | 0.0 | 4 | 0.003 |
| 11h | 101,668 | 10.2844 | oficial | 94,595 | 93.043 | 7,072 | 6.956 | 0 | 0.0 | 1 | 0.001 |
| 12h | 76,745 | 7.7633 | oficial | 71,272 | 92.8686 | 5,472 | 7.1301 | 0 | 0.0 | 1 | 0.0013 |
| 13h | 72,033 | 7.2866 | oficial | 66,516 | 92.341 | 5,515 | 7.6562 | 0 | 0.0 | 2 | 0.0028 |
| 14h | 77,277 | 7.8171 | oficial | 71,375 | 92.3625 | 5,902 | 7.6375 | 0 | 0.0 | 0 | 0.0 |
| 15h | 64,866 | 6.5616 | oficial | 60,003 | 92.503 | 4,861 | 7.4939 | 0 | 0.0 | 2 | 0.0031 |
| 16h | 515 | 0.0521 | pós-encerramento | 467 | 90.6796 | 48 | 9.3204 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 987,863 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
