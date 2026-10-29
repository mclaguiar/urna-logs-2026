# Comparativo 1º × 2º turno — AP

Status: **pronto**

Comparativo 1º×2º preenchido (finalistas 13×22; saldo agregado por seção — não é migração eleitor a eleitor).

## Disponibilidade

- 1º turno (audit): sim · 1,914 seções
- 2º turno (audit): sim · 1,914 seções
- Finalistas (nominais no 2º): **13** e **22**
- Margem = votos(13) − votos(22)

## Métricas

- Seções em ambos: **1,914**
- Só no 1º: **0** · só no 2º: **0**
- Δ comparecimento (soma seções ambos): **-46587**
- Δ abstenção (pp, aptos ambos): **8.0641**
- % sem digital 1º→2º: **8.1286** → **8.1419** (Δ **0.0133**)

## Pós-17h (UF)

- % ≥17h no 1º: **5.3647**
- % ≥17h no 2º: **0.0298**
- Δ (2º − 1º): **-5.3349**

## Flags de anomalia (percentis na UF)

- `|Δ abstenção|` ≥ p95: **99**
- `|Δ margem|` ≥ p95: **103**
- alto % sem digital 1º × `|Δ margem|`: **28**
- cauda pós-17h atípica: **1914**
- só em um turno: **0**

## Seções que mais movem a margem (13−22)

| join_key | Δ margem | Δ abst | % sem dig 1º | %≥17h 2º | flags |
|---|---:|---:|---:|---:|---|
| `AP:06050:0002:0706` | 64 | 32 | 4.717 | 0.0 | margem|pos17 |
| `AP:06084:0011:0024` | 63 | 40 | 2.9762 | 0.0 | margem|pos17 |
| `AP:06050:0002:0481` | 52 | 17 | 3.7415 | 0.0 | margem|pos17 |
| `AP:06092:0004:0072` | -52 | 70 | 17.3709 | 0.0 | abstencao|margem|sem_digital_x_margem|pos17 |
| `AP:06050:0002:0962` | 52 | 41 | 7.0946 | 0.0 | margem|pos17 |
| `AP:06050:0014:0329` | 50 | 19 | 6.5934 | 0.0 | margem|pos17 |
| `AP:06050:0002:0310` | 49 | 22 | 9.6154 | 0.0 | margem|pos17 |
| `AP:06033:0001:0066` | 49 | 42 | 7.8652 | 0.4444 | margem|pos17 |
| `AP:06050:0010:0356` | 47 | 21 | 9.6154 | 0.0 | margem|pos17 |
| `AP:06050:0010:0435` | 46 | 30 | 8.2278 | 0.0 | margem|pos17 |
| `AP:06050:0010:0326` | 46 | 19 | 6.5217 | 0.0 | margem|pos17 |
| `AP:06009:0001:0014` | 46 | 42 | 7.5 | 0.0 | margem|pos17 |
| `AP:06050:0002:0355` | 45 | 27 | 8.254 | 0.0 | margem|pos17 |
| `AP:06050:0002:0558` | 45 | 39 | 10.0304 | 0.0 | margem|sem_digital_x_margem|pos17 |
| `AP:06050:0014:0135` | 45 | 24 | 16.5493 | 0.0 | margem|sem_digital_x_margem|pos17 |

## Seções com flag

1,914 seção(ões) (até 30):

- `AP:06009:0001:0004` · pos17 · Δmargem=7 · Δabst=12
- `AP:06009:0001:0013` · pos17 · Δmargem=23 · Δabst=32
- `AP:06009:0001:0014` · margem|pos17 · Δmargem=46 · Δabst=42
- `AP:06009:0001:0022` · abstencao|pos17 · Δmargem=23 · Δabst=72
- `AP:06009:0001:0026` · abstencao|pos17 · Δmargem=25 · Δabst=61
- `AP:06009:0001:0027` · pos17 · Δmargem=26 · Δabst=56
- `AP:06009:0001:0039` · abstencao|pos17 · Δmargem=16 · Δabst=60
- `AP:06009:0001:0040` · abstencao|pos17 · Δmargem=11 · Δabst=64
- `AP:06009:0001:0041` · pos17 · Δmargem=29 · Δabst=55
- `AP:06009:0001:0042` · abstencao|margem|pos17 · Δmargem=36 · Δabst=102
- `AP:06009:0001:0044` · abstencao|pos17 · Δmargem=21 · Δabst=70
- `AP:06009:0001:0046` · abstencao|margem|sem_digital_x_margem|pos17 · Δmargem=35 · Δabst=63
- `AP:06009:0001:0048` · abstencao|pos17 · Δmargem=21 · Δabst=67
- `AP:06009:0001:0078` · pos17 · Δmargem=-4 · Δabst=18
- `AP:06009:0001:0080` · pos17 · Δmargem=10 · Δabst=15
- `AP:06009:0001:0089` · pos17 · Δmargem=12 · Δabst=14
- `AP:06017:0001:0001` · pos17 · Δmargem=14 · Δabst=30
- `AP:06017:0001:0002` · pos17 · Δmargem=14 · Δabst=31
- `AP:06017:0001:0003` · pos17 · Δmargem=1 · Δabst=28
- `AP:06017:0001:0008` · pos17 · Δmargem=-24 · Δabst=44
- `AP:06017:0001:0012` · pos17 · Δmargem=11 · Δabst=40
- `AP:06017:0001:0017` · pos17 · Δmargem=11 · Δabst=48
- `AP:06017:0001:0018` · pos17 · Δmargem=8 · Δabst=45
- `AP:06017:0001:0019` · pos17 · Δmargem=24 · Δabst=44
- `AP:06017:0001:0020` · pos17 · Δmargem=11 · Δabst=45
- `AP:06017:0001:0021` · pos17 · Δmargem=4 · Δabst=46
- `AP:06017:0001:0029` · pos17 · Δmargem=15 · Δabst=43
- `AP:06017:0001:0030` · pos17 · Δmargem=10 · Δabst=36
- `AP:06017:0001:0031` · pos17 · Δmargem=-6 · Δabst=54
- `AP:06017:0001:0032` · pos17 · Δmargem=1 · Δabst=51
- … e mais 1884

## Hipóteses → observáveis (agregado; não conclusões)

| Hipótese | Observável |
|---|---|
| Transferência aparente dos eliminados | `votos_eliminados_1t` ≈ `ganho_finalistas` − `delta_comparecimento` (residual em `gap_transferencia`) |
| Abstenção seletiva | `|delta_abstencao|` alto com pouco Δ nos finalistas |
| Risco operacional | alto `% sem digital` × `|delta_margem|` |
| Cauda horária | alto `% ≥17h` × Δ comparecimento/margem |
| Contingência / troca de urna | status `so_1t` / `so_2t` |

## Limites

- Comparação é **agregada por seção** (`join_key`).
- Não dá para saber *quem* mudou de candidato entre turnos (sigilo do voto).
- “Migração” = mudança dos totais da seção (finalistas, eliminados, abstenção).
- RDV≡BU e BU≡CSV oficial comparam a **integridade entre arquivos públicos** disponibilizados.
