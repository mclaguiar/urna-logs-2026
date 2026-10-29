# Curva horária — SP 2º turno

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

- Habilitações no dia: **27,365,555**
  - **1,166** habilitações não viraram voto no BU: a habilitação foi feita e a votação foi interrompida antes do registro.
  - **1,190** com a frase «Eleitor foi suspenso e não confirmou nenhum voto».
- Oficial [8h,17h): **27,357,411** (99.9702%)
- Pós-encerramento ≥17h: **8,144** (% entre oficial+pós: **0.0298**)
- Fora do previsto (&lt;8h no dia): **0** (0.0%)
- Seções: **103,655** · urnas: **104,455**
- Pico (hora local): **10h** (3,975,348)
- Faixas ≥17h (ref. brasilia): 17–18h **0.0274** · 18–19h **0.0023** · 19h+ **0.0**
- Histórico de **outras datas** no mesmo log (ignorado neste turno): **26,337,783** — ver seção abaixo / `curva_horaria_dia_*`

## Habilitações × votos de presidente (BU)

Apontamento. Cada habilitação no dia oficial deveria corresponder a um voto de presidente no boletim: nominal, branco ou nulo.

- Habilitações no log: **27,365,555**
- Votos computados no log (`O voto do eleitor foi computado`): **27,364,121**
- Votos de presidente no BU: **27,364,389**
  - nominais **26,258,452** · brancos **389,606** · nulos **716,331**

**+1,166** são habilitações feitas em que o voto **não foi registrado**. A votação foi interrompida antes da confirmação. O boletim não recebe esse voto.
Votos computados no log (**27,364,121**) e votos do BU (**27,364,389**) diferem em **-268**.
- **1,190** — o mesário suspendeu o eleitor. O log diz «Eleitor foi suspenso e não confirmou nenhum voto».
- A frase de suspensão aparece **24** vezes a mais do que essa diferença.

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

- Com digital: **24,502,456** (89.54% do dia)
- Manual: **2,862,117** (10.46% do dia)
- Sem biometria: **0** (0.0% do dia)
- Não classificada: **982** (0.0% do dia)

## Distribuição horária (dia oficial · relógio local)

Percentuais de tipo são **dentro da hora**.

| Hora local | Habilitações | % no dia | Janela | Biom. | % | Manual | % | Sem biom. | % | Não class. | % |
|---:|---:|---:|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 08h | 3,847,337 | 14.059 | oficial | 3,414,773 | 88.7568 | 432,350 | 11.2376 | 0 | 0.0 | 214 | 0.0056 |
| 09h | 3,696,324 | 13.5072 | oficial | 3,279,875 | 88.7334 | 416,340 | 11.2636 | 0 | 0.0 | 109 | 0.0029 |
| 10h | 3,975,348 | 14.5268 | oficial | 3,549,176 | 89.2796 | 426,069 | 10.7178 | 0 | 0.0 | 103 | 0.0026 |
| 11h | 3,952,093 | 14.4419 | oficial | 3,550,323 | 89.834 | 401,626 | 10.1624 | 0 | 0.0 | 144 | 0.0036 |
| 12h | 3,433,218 | 12.5458 | oficial | 3,094,574 | 90.1363 | 338,526 | 9.8603 | 0 | 0.0 | 118 | 0.0034 |
| 13h | 2,763,838 | 10.0997 | oficial | 2,489,742 | 90.0828 | 273,991 | 9.9134 | 0 | 0.0 | 105 | 0.0038 |
| 14h | 2,275,537 | 8.3153 | oficial | 2,047,035 | 89.9583 | 228,424 | 10.0382 | 0 | 0.0 | 78 | 0.0034 |
| 15h | 2,008,720 | 7.3403 | oficial | 1,804,183 | 89.8175 | 204,470 | 10.1791 | 0 | 0.0 | 67 | 0.0033 |
| 16h | 1,404,996 | 5.1342 | oficial | 1,265,699 | 90.0856 | 139,253 | 9.9113 | 0 | 0.0 | 44 | 0.0031 |
| 17h | 7,505 | 0.0274 | pós-encerramento | 6,495 | 86.5423 | 1,010 | 13.4577 | 0 | 0.0 | 0 | 0.0 |
| 18h | 634 | 0.0023 | pós-encerramento | 576 | 90.8517 | 58 | 9.1483 | 0 | 0.0 | 0 | 0.0 |
| 19h | 5 | 0.0 | pós-encerramento | 5 | 100.0 | 0 | 0.0 | 0 | 0.0 | 0 | 0.0 |

## Histórico no `.jez` (outras datas — não é deste turno)

O pacote pode trazer o log acumulado. Estes totais **não** entram nas métricas acima nem no `comparar-turnos`.

| Data | Habs |
|---|---:|
| 2026-10-04 | 26,337,783 |

Detalhe hora a hora: CSV `curva_horaria_dia_*` (coluna `janela=historico_outro_dia`).

\* Exterior (ZZ): referência = horário **local**. Demais UFs: **Brasília**.

## Nota

Janela legal: 8h–17h no dia do turno. Pós-17h = fila. Comparar 1º×2º só com métricas do respectivo dia oficial.
