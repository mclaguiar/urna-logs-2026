# Achados de auditoria — MA (1º×2º)

Protocolo **2026.10.31-b** · pacote `0.1.0`

A=inconsistência entre arquivos públicos; B=dois ou mais sinais independentes no p99 da UF; C=um sinal no p99 da UF. Sinais: |Δ abstenção|, |Δ margem|, % sem digital no 1º turno, % após 17h no 1º ou no 2º. A cauda só conta se o percentil é maior que zero e a série varia.

## Resumo

- Total classificado: **892**
- Nível A (documental): **1**
- Nível B (operacional): **48**
- Nível C (contexto): **843**

## Hierarquia

| Nível | Significado | Uso em auditoria |
|---|---|---|
| **A** | Inconsistência entre arquivos públicos / cobertura | Indício documental — listar e checar cadeia |
| **B** | Confluência de sinais operacionais | Dois ou mais sinais no extremo da UF |
| **C** | Flag isolada do comparativo | Um sinal no extremo da UF, sem confluência |

## Fichas (até 40 por UF, A→B→C)

### Ficha 1 — Nível A — `MA:07846:0074:0228`

- **Códigos:** `A_audit_rdv_bu_1t`
- **Status turno:** ambos
- Δ margem: **2** · Δ abstenção: **2**
- % sem digital 1º: **6.8493** · % ≥17h 2º: **0.0**
- Flags comparar: `—`
- **Fato:** Os arquivos públicos desta seção não fecham entre si, ou a seção não aparece nos dois turnos.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 2 — Nível B — `MA:09393:0079:0131`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **57** · Δ abstenção: **-13**
- % sem digital 1º: **11.9342** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 3 — Nível B — `MA:09474:0050:0107`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **53** · Δ abstenção: **-23**
- % sem digital 1º: **6.8826** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 4 — Nível B — `MA:07234:0013:0098`

- **Códigos:** `B_margem_x_pos17|B_margem_x_abstencao|B_confluencia_3`
- **Status turno:** ambos
- Δ margem: **51** · Δ abstenção: **-33**
- % sem digital 1º: **12.5** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 5 — Nível B — `MA:07234:0013:0475`

- **Códigos:** `B_sem_digital_x_margem|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **48** · Δ abstenção: **-10**
- % sem digital 1º: **29.9639** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|sem_digital|sem_digital_x_margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 6 — Nível B — `MA:07978:0032:0035`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **-48** · Δ abstenção: **72**
- % sem digital 1º: **12.1795** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 7 — Nível B — `MA:08974:0070:0403`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **48** · Δ abstenção: **14**
- % sem digital 1º: **21.6783** · % ≥17h 2º: **3.876**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 8 — Nível B — `MA:09350:0007:0363`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **48** · Δ abstenção: **-26**
- % sem digital 1º: **4.6875** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 9 — Nível B — `MA:07633:0007:0139`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **47** · Δ abstenção: **-13**
- % sem digital 1º: **9.507** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 10 — Nível B — `MA:09156:0021:0040`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **47** · Δ abstenção: **-33**
- % sem digital 1º: **11.6788** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 11 — Nível B — `MA:07676:0029:0046`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **46** · Δ abstenção: **-8**
- % sem digital 1º: **16.6102** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 12 — Nível B — `MA:07005:0012:0022`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **45** · Δ abstenção: **-7**
- % sem digital 1º: **10.0358** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 13 — Nível B — `MA:07234:0013:0397`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **45** · Δ abstenção: **10**
- % sem digital 1º: **9.1185** · % ≥17h 2º: **0.627**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 14 — Nível B — `MA:08559:0036:0046`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **45** · Δ abstenção: **-26**
- % sem digital 1º: **6.7669** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 15 — Nível B — `MA:07277:0022:0213`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **44** · Δ abstenção: **-35**
- % sem digital 1º: **10.1449** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 16 — Nível B — `MA:09210:0010:0859`

- **Códigos:** `B_sem_digital_x_margem|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **44** · Δ abstenção: **-7**
- % sem digital 1º: **25.1701** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|sem_digital|sem_digital_x_margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 17 — Nível B — `MA:07234:0013:0356`

- **Códigos:** `B_margem_x_pos17|B_margem_x_abstencao|B_confluencia_3`
- **Status turno:** ambos
- Δ margem: **43** · Δ abstenção: **-40**
- % sem digital 1º: **8.9347** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 18 — Nível B — `MA:07617:0042:0148`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **43** · Δ abstenção: **-7**
- % sem digital 1º: **7.1146** · % ≥17h 2º: **0.3846**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 19 — Nível B — `MA:08052:0035:0021`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **42** · Δ abstenção: **-17**
- % sem digital 1º: **10.7623** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 20 — Nível B — `MA:08796:0054:0077`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **42** · Δ abstenção: **-17**
- % sem digital 1º: **7.3248** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 21 — Nível B — `MA:07765:0097:0157`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **41** · Δ abstenção: **-16**
- % sem digital 1º: **11.0714** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 22 — Nível B — `MA:08494:0093:0360`

- **Códigos:** `B_sem_digital_x_margem|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **41** · Δ abstenção: **3**
- % sem digital 1º: **33.1104** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|sem_digital|sem_digital_x_margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 23 — Nível B — `MA:09156:0021:0030`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **41** · Δ abstenção: **-18**
- % sem digital 1º: **15.2027** · % ≥17h 2º: **0.3185**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 24 — Nível B — `MA:07692:0008:0180`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **40** · Δ abstenção: **-13**
- % sem digital 1º: **50.1805** · % ≥17h 2º: **0.6897**
- Flags comparar: `sem_digital|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 25 — Nível B — `MA:08796:0054:0282`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **30** · Δ abstenção: **-6**
- % sem digital 1º: **26.6904** · % ≥17h 2º: **0.0**
- Flags comparar: `sem_digital|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 26 — Nível B — `MA:07498:0064:0178`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **-25** · Δ abstenção: **61**
- % sem digital 1º: **3.6145** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 27 — Nível B — `MA:07234:0013:0446`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **24** · Δ abstenção: **5**
- % sem digital 1º: **27.0833** · % ≥17h 2º: **1.0695**
- Flags comparar: `sem_digital|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 28 — Nível B — `MA:07234:0013:0449`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **20** · Δ abstenção: **1**
- % sem digital 1º: **25.1572** · % ≥17h 2º: **0.6329**
- Flags comparar: `sem_digital|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 29 — Nível B — `MA:07765:0097:0171`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **19** · Δ abstenção: **-10**
- % sem digital 1º: **24.8521** · % ≥17h 2º: **0.5587**
- Flags comparar: `sem_digital|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 30 — Nível B — `MA:07994:0031:0111`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **-17** · Δ abstenção: **62**
- % sem digital 1º: **7.7551** · % ≥17h 2º: **0.5464**
- Flags comparar: `abstencao|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 31 — Nível B — `MA:09172:0063:0070`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **14** · Δ abstenção: **34**
- % sem digital 1º: **14.2857** · % ≥17h 2º: **0.7874**
- Flags comparar: `abstencao|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 32 — Nível B — `MA:07692:0008:0163`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **-12** · Δ abstenção: **-5**
- % sem digital 1º: **25.6831** · % ≥17h 2º: **0.5319**
- Flags comparar: `sem_digital|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 33 — Nível B — `MA:08109:0030:0188`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **10** · Δ abstenção: **41**
- % sem digital 1º: **11.399** · % ≥17h 2º: **0.6579**
- Flags comparar: `abstencao|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 34 — Nível B — `MA:09415:0039:0168`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **-10** · Δ abstenção: **48**
- % sem digital 1º: **26.8657** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|sem_digital`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 35 — Nível B — `MA:07137:0109:0065`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **9** · Δ abstenção: **2**
- % sem digital 1º: **26.1628** · % ≥17h 2º: **0.5882**
- Flags comparar: `sem_digital|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 36 — Nível B — `MA:09172:0063:0037`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **-9** · Δ abstenção: **32**
- % sem digital 1º: **8.5227** · % ≥17h 2º: **0.6897**
- Flags comparar: `abstencao|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 37 — Nível B — `MA:07293:0021:0068`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **8** · Δ abstenção: **4**
- % sem digital 1º: **36.7188** · % ≥17h 2º: **0.8065**
- Flags comparar: `sem_digital|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 38 — Nível B — `MA:08249:0032:0117`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **-8** · Δ abstenção: **85**
- % sem digital 1º: **11.5108** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 39 — Nível B — `MA:09415:0039:0184`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **8** · Δ abstenção: **47**
- % sem digital 1º: **18.2119** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 40 — Nível B — `MA:07285:0066:0241`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **7** · Δ abstenção: **43**
- % sem digital 1º: **25.3165** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|sem_digital`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

_… e mais 852 no Parquet `achados_MA_1t_2t.parquet`_

## Reprodução

```bash
urna-logs comparar-turnos --ufs MA
urna-logs achados --ufs MA
```

Artefatos: `achados_MA_1t_2t.parquet`, `achados_summary_MA_1t_2t.csv`
