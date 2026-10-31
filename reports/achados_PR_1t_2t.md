# Achados de auditoria — PR (1º×2º)

Protocolo **2026.10.31-b** · pacote `0.1.0`

A=inconsistência entre arquivos públicos; B=dois ou mais sinais independentes no p99 da UF; C=um sinal no p99 da UF. Sinais: |Δ abstenção|, |Δ margem|, % sem digital no 1º turno, % após 17h no 1º ou no 2º. A cauda só conta se o percentil é maior que zero e a série varia.

## Resumo

- Total classificado: **1,335**
- Nível A (documental): **0**
- Nível B (operacional): **98**
- Nível C (contexto): **1,237**

## Hierarquia

| Nível | Significado | Uso em auditoria |
|---|---|---|
| **A** | Inconsistência entre arquivos públicos / cobertura | Indício documental — listar e checar cadeia |
| **B** | Confluência de sinais operacionais | Dois ou mais sinais no extremo da UF |
| **C** | Flag isolada do comparativo | Um sinal no extremo da UF, sem confluência |

## Fichas (até 40 por UF, A→B→C)

### Ficha 1 — Nível B — `PR:75663:0146:0434`

- **Códigos:** `B_margem_x_pos17|B_margem_x_abstencao|B_confluencia_3`
- **Status turno:** ambos
- Δ margem: **59** · Δ abstenção: **-60**
- % sem digital 1º: **2.0** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 2 — Nível B — `PR:75663:0146:0435`

- **Códigos:** `B_margem_x_pos17|B_margem_x_abstencao|B_confluencia_3`
- **Status turno:** ambos
- Δ margem: **51** · Δ abstenção: **-45**
- % sem digital 1º: **4.4534** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 3 — Nível B — `PR:74934:0068:0532`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **49** · Δ abstenção: **-26**
- % sem digital 1º: **4.7138** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 4 — Nível B — `PR:84573:0119:0089`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **46** · Δ abstenção: **-30**
- % sem digital 1º: **8.9965** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 5 — Nível B — `PR:74900:0017:0047`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **45** · Δ abstenção: **-5**
- % sem digital 1º: **8.6455** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 6 — Nível B — `PR:77330:0032:0113`

- **Códigos:** `B_margem_x_pos17|B_margem_x_abstencao|B_confluencia_3`
- **Status turno:** ambos
- Δ margem: **43** · Δ abstenção: **-31**
- % sem digital 1º: **6.6914** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 7 — Nível B — `PR:77330:0032:0100`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **42** · Δ abstenção: **-13**
- % sem digital 1º: **5.8091** · % ≥17h 2º: **0.3937**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 8 — Nível B — `PR:74446:0156:0216`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **41** · Δ abstenção: **-9**
- % sem digital 1º: **6.7485** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 9 — Nível B — `PR:75310:0091:0010`

- **Códigos:** `B_sem_digital_x_margem|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **41** · Δ abstenção: **-20**
- % sem digital 1º: **22.4066** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|sem_digital|sem_digital_x_margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 10 — Nível B — `PR:78093:0140:0123`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **41** · Δ abstenção: **-34**
- % sem digital 1º: **6.8404** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 11 — Nível B — `PR:78115:0039:0026`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **38** · Δ abstenção: **-30**
- % sem digital 1º: **4.1667** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 12 — Nível B — `PR:76597:0045:0117`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **37** · Δ abstenção: **-25**
- % sem digital 1º: **1.7391** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 13 — Nível B — `PR:74446:0156:0188`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **36** · Δ abstenção: **-15**
- % sem digital 1º: **6.1728** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 14 — Nível B — `PR:74446:0156:0222`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **35** · Δ abstenção: **-16**
- % sem digital 1º: **9.6677** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 15 — Nível B — `PR:76597:0045:0011`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **35** · Δ abstenção: **-25**
- % sem digital 1º: **10.8374** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 16 — Nível B — `PR:77275:0167:0010`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **35** · Δ abstenção: **-11**
- % sem digital 1º: **6.1611** · % ≥17h 2º: **0.4484**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 17 — Nível B — `PR:77330:0032:0105`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **35** · Δ abstenção: **-24**
- % sem digital 1º: **5.1282** · % ≥17h 2º: **0.3876**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 18 — Nível B — `PR:74535:0077:0049`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **34** · Δ abstenção: **-34**
- % sem digital 1º: **12.6761** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 19 — Nível B — `PR:78212:0156:0221`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **-34** · Δ abstenção: **92**
- % sem digital 1º: **7.2727** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 20 — Nível B — `PR:78590:0022:0059`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **34** · Δ abstenção: **-26**
- % sem digital 1º: **14.9254** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 21 — Nível B — `PR:84611:0206:0188`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **34** · Δ abstenção: **-30**
- % sem digital 1º: **9.1703** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 22 — Nível B — `PR:74713:0078:0219`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **33** · Δ abstenção: **-26**
- % sem digital 1º: **12.8302** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 23 — Nível B — `PR:75833:0044:0326`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **33** · Δ abstenção: **-28**
- % sem digital 1º: **7.1942** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 24 — Nível B — `PR:76678:0042:0413`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **33** · Δ abstenção: **-26**
- % sem digital 1º: **3.321** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 25 — Nível B — `PR:77453:0005:0403`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **33** · Δ abstenção: **-2**
- % sem digital 1º: **4.9383** · % ≥17h 2º: **0.4082**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 26 — Nível B — `PR:77496:0072:0135`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **33** · Δ abstenção: **-25**
- % sem digital 1º: **11.25** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 27 — Nível B — `PR:77690:0155:0465`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **33** · Δ abstenção: **-21**
- % sem digital 1º: **3.9648** · % ≥17h 2º: **0.4032**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 28 — Nível B — `PR:78174:0062:0046`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **33** · Δ abstenção: **5**
- % sem digital 1º: **7.2727** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 29 — Nível B — `PR:74446:0156:0150`

- **Códigos:** `B_margem_x_pos17|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **32** · Δ abstenção: **-13**
- % sem digital 1º: **7.1651** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 30 — Nível B — `PR:75639:0147:0255`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **32** · Δ abstenção: **-29**
- % sem digital 1º: **7.3913** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 31 — Nível B — `PR:77313:0154:0274`

- **Códigos:** `B_margem_x_abstencao|B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **32** · Δ abstenção: **-26**
- % sem digital 1º: **8.3333** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|margem`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 32 — Nível B — `PR:77879:0071:0072`

- **Códigos:** `B_sem_digital_x_margem|B_margem_x_pos17|B_confluencia_3`
- **Status turno:** ambos
- Δ margem: **32** · Δ abstenção: **-22**
- % sem digital 1º: **24.8848** · % ≥17h 2º: **0.0**
- Flags comparar: `margem|sem_digital|sem_digital_x_margem|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 33 — Nível B — `PR:78158:0082:0046`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **31** · Δ abstenção: **-32**
- % sem digital 1º: **8.8889** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 34 — Nível B — `PR:74446:0156:0271`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **30** · Δ abstenção: **-28**
- % sem digital 1º: **9.699** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 35 — Nível B — `PR:74764:0165:0033`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **29** · Δ abstenção: **-31**
- % sem digital 1º: **5.9801** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 36 — Nível B — `PR:78514:0130:0121`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **28** · Δ abstenção: **-10**
- % sem digital 1º: **22.5589** · % ≥17h 2º: **0.0**
- Flags comparar: `sem_digital|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 37 — Nível B — `PR:74446:0156:0262`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **27** · Δ abstenção: **-32**
- % sem digital 1º: **13.2653** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 38 — Nível B — `PR:78158:0082:0075`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **27** · Δ abstenção: **-25**
- % sem digital 1º: **8.8328** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 39 — Nível B — `PR:78255:0059:0160`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **27** · Δ abstenção: **-27**
- % sem digital 1º: **21.875** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|sem_digital`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

### Ficha 40 — Nível B — `PR:74446:0156:0144`

- **Códigos:** `B_confluencia_2`
- **Status turno:** ambos
- Δ margem: **25** · Δ abstenção: **-34**
- % sem digital 1º: **9.697** · % ≥17h 2º: **0.0**
- Flags comparar: `abstencao|pos17`
- **Fato:** Dois ou mais sinais desta seção estão no extremo da distribuição da própria UF.
- **Escopo:** totais agregados da seção (sem microdado de eleitor).

_… e mais 1295 no Parquet `achados_PR_1t_2t.parquet`_

## Reprodução

```bash
urna-logs comparar-turnos --ufs PR
urna-logs achados --ufs PR
```

Artefatos: `achados_PR_1t_2t.parquet`, `achados_summary_PR_1t_2t.csv`
