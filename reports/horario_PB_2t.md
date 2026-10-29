# Curva horária — PB 2º turno

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

- Habilitações no dia: **2,743,837**
  - **277** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **247** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
  - **30** sem essa frase; o voto também não foi computado.
- Oficial [8h,17h): **2,743,407** (99.9843%)
- Pós-encerramento ≥17h: **430** (% entre oficial+pós: **0.0157**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **10,712** · urnas: **10,814**
- Pico (hora local): **8h** (525,706)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0142** · 18–19h **0.0015** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **2,672,690** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **2,743,837**
- Votos computados no log (`O voto do eleitor foi computado`): **2,743,559**
- Votos de presidente no BU: **2,743,560**
  - nominais **2,659,269** · brancos **25,943** · nulos **58,348**

**+277** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**2,743,559**) e votos do BU (**2,743,560**) diferem em **-1**.
- **247** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- **30** — o voto também não foi registrado, e o log não traz essa frase.

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

- Com digital: **2,461,991** (89.73% do dia)
- Manual: **281,743** (10.27% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **103** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 525,706 | 19.1595 | oficial | 468,178 | 89.057 | 57,505 | 10.9386 | 0 | 0.0 | 23 | 0.0044 |
| 09h | 458,625 | 16.7147 | oficial | 409,868 | 89.3689 | 48,745 | 10.6285 | 0 | 0.0 | 12 | 0.0026 |
| 10h | 396,123 | 14.4368 | oficial | 355,594 | 89.7686 | 40,518 | 10.2286 | 0 | 0.0 | 11 | 0.0028 |
| 11h | 304,419 | 11.0946 | oficial | 274,609 | 90.2076 | 29,797 | 9.7882 | 0 | 0.0 | 13 | 0.0043 |
| 12h | 236,975 | 8.6366 | oficial | 214,028 | 90.3167 | 22,934 | 9.6778 | 0 | 0.0 | 13 | 0.0055 |
| 13h | 212,662 | 7.7505 | oficial | 191,566 | 90.08 | 21,087 | 9.9157 | 0 | 0.0 | 9 | 0.0042 |
| 14h | 224,040 | 8.1652 | oficial | 201,312 | 89.8554 | 22,717 | 10.1397 | 0 | 0.0 | 11 | 0.0049 |
| 15h | 234,142 | 8.5334 | oficial | 210,503 | 89.904 | 23,629 | 10.0917 | 0 | 0.0 | 10 | 0.0043 |
| 16h | 150,715 | 5.4929 | oficial | 135,974 | 90.2193 | 14,740 | 9.78 | 0 | 0.0 | 1 | 0.0007 |
| 17h | 389 | 0.0142 | pós-encerramento | 324 | 83.2905 | 65 | 16.7095 | 0 | 0.0 | 0 | 0.0 |
| 18h | 41 | 0.0015 | pós-encerramento | 35 | 85.3659 | 6 | 14.6341 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 2,672,690 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
