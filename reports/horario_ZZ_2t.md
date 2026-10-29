# Curva horária — ZZ 2º turno

Modo: **curva** (agregado; sem Parquet detalhado)

Fonte: timestamps de **habilitação** no log (`Eleitor foi habilitado`).
Não é horário do voto em cada cargo.

Relógio do log = **hora local** da urna (metadado fuso UTC-3).
Critério: janela 8h–17h no **horário local** (exterior); ≥17h = pós-encerramento.

Métricas deste relatório = **somente o dia oficial deste turno**.
Janelas no dia: **oficial** [8h,17h) · **pós-encerramento** ≥17h · **fora do previsto** &lt;8h.
Eventos de **outra data** no `.jez` = histórico (não entram nos totais nem no comparativo 1º×2º).
Dia oficial deste turno: **2026-10-25**.

## Resumo (só o dia do turno)

- Habilitações no dia: **380,683**
  - O BU registra **760** votos de presidente a mais do que as habilitações do log.
- Oficial [8h,17h): **380,293** (99.8976%)
- Pós-encerramento ≥17h: **390** (% entre oficial+pós: **0.1024**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **1,310** · urnas: **1,295**
- Pico (hora local): **11h** (52,695)
- Faixas ≥17h (ref. local): 17–18h **0.1024** · 18–19h **0.0** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **341,086** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **380,683**
- Votos computados no log (`O voto do eleitor foi computado`): **380,612**
- Votos de presidente no BU: **381,443**
  - nominais **371,651** · brancos **4,675** · nulos **5,117**

**-760**: o BU tem **760** votos de presidente a mais do que as habilitações do log.

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

- Com digital: **0** (0.0% do dia)
- Manual: **380,683** (100.0% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **0** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 49,397 | 12.9759 | oficial | 0 | 0.0 | 49,397 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 09h | 46,799 | 12.2934 | oficial | 0 | 0.0 | 46,799 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 10h | 51,401 | 13.5023 | oficial | 0 | 0.0 | 51,401 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 11h | 52,695 | 13.8422 | oficial | 0 | 0.0 | 52,695 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 12h | 48,261 | 12.6775 | oficial | 0 | 0.0 | 48,261 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 13h | 42,058 | 11.048 | oficial | 0 | 0.0 | 42,058 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 14h | 37,340 | 9.8087 | oficial | 0 | 0.0 | 37,340 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 15h | 31,518 | 8.2793 | oficial | 0 | 0.0 | 31,518 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 16h | 20,824 | 5.4702 | oficial | 0 | 0.0 | 20,824 | 100.0 | 0 | 0.0 | 0 | 0.0 |
| 17h | 390 | 0.1024 | pós-encerramento | 0 | 0.0 | 390 | 100.0 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 341,086 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
