# Validação fluxo ecológico — 1º→2º

Verdict global: **GO** (6/6 UFs passaram nos checks hard)

Objetivo: sanidade do algoritmo no piloto antes de escalar ao país. Não valida preferência eleitoral nem ausência de anomalia política.

## Por UF

### AC — GO (2270 seções)

| Check | Sev | OK | Detalhe |
|---|---|:---:|---|
| `min_secoes` | hard | sim | 2270 seções (mínimo 50) |
| `identidade` | hard | sim | 2270/2270 seções com margens coerentes (100.00%; mín 99.5%) |
| `ipf_margens` | hard | sim | max |IPF−origem|=0.000 · max |IPF−destino|=0.000 (tol 2.0) |
| `ipf_dentro_bounds` | hard | sim | 0 violações em 45400 células (max fora=0.000, tol=2.0) |
| `taxas_validas` | hard | sim | todas as origens-foco OK |
| `sem_colapso_5050` | hard | sim | |Fa2−Fb2|/N=0.233 · |pElimFa−pElimFb|=0.242 |
| `estabilidade` | hard | sim | taxas IPF idênticas=True · bootstrap seed=True |
| `residuo_preditivo` | soft | sim | mean|resid|/mean(dest) → fa:0.189, fb:0.137, abst:0.207 (tol 0.35) |
| `compat_elim_fa` | hard | sim | Elim×p(Elim→Fa)=7,518.4 ≤ Fa2=144,513.0 |
| `artefatos` | soft | sim | OK |
| `cruzar_oficial_2t` | soft | sim | seções divergentes BU×oficial=0 |

### RR — GO (1519 seções)

| Check | Sev | OK | Detalhe |
|---|---|:---:|---|
| `min_secoes` | hard | sim | 1519 seções (mínimo 50) |
| `identidade` | hard | sim | 1519/1519 seções com margens coerentes (100.00%; mín 99.5%) |
| `ipf_margens` | hard | sim | max |IPF−origem|=0.000 · max |IPF−destino|=0.000 (tol 2.0) |
| `ipf_dentro_bounds` | hard | sim | 0 violações em 30380 células (max fora=0.000, tol=2.0) |
| `taxas_validas` | hard | sim | todas as origens-foco OK |
| `sem_colapso_5050` | hard | sim | |Fa2−Fb2|/N=0.339 · |pElimFa−pElimFb|=0.370 |
| `estabilidade` | hard | sim | taxas IPF idênticas=True · bootstrap seed=True |
| `residuo_preditivo` | soft | sim | mean|resid|/mean(dest) → fa:0.279, fb:0.128, abst:0.221 (tol 0.35) |
| `compat_elim_fa` | hard | sim | Elim×p(Elim→Fa)=3,879.9 ≤ Fa2=83,505.0 |
| `artefatos` | soft | sim | OK |
| `cruzar_oficial_2t` | soft | sim | seções divergentes BU×oficial=0 |

### AP — GO (1914 seções)

| Check | Sev | OK | Detalhe |
|---|---|:---:|---|
| `min_secoes` | hard | sim | 1914 seções (mínimo 50) |
| `identidade` | hard | sim | 1914/1914 seções com margens coerentes (100.00%; mín 99.5%) |
| `ipf_margens` | hard | sim | max |IPF−origem|=0.000 · max |IPF−destino|=0.000 (tol 2.0) |
| `ipf_dentro_bounds` | hard | sim | 0 violações em 38280 células (max fora=0.000, tol=2.0) |
| `taxas_validas` | hard | sim | todas as origens-foco OK |
| `sem_colapso_5050` | hard | sim | |Fa2−Fb2|/N=0.042 · |pElimFa−pElimFb|=0.022 |
| `estabilidade` | hard | sim | taxas IPF idênticas=True · bootstrap seed=True |
| `residuo_preditivo` | soft | sim | mean|resid|/mean(dest) → fa:0.124, fb:0.191, abst:0.247 (tol 0.35) |
| `compat_elim_fa` | hard | sim | Elim×p(Elim→Fa)=15,303.1 ≤ Fa2=222,968.0 |
| `artefatos` | soft | sim | OK |
| `cruzar_oficial_2t` | soft | sim | seções divergentes BU×oficial=0 |

### ZZ — GO (1310 seções)

| Check | Sev | OK | Detalhe |
|---|---|:---:|---|
| `min_secoes` | hard | sim | 1310 seções (mínimo 50) |
| `identidade` | hard | sim | 1308/1310 seções com margens coerentes (99.85%; mín 99.5%) |
| `ipf_margens` | hard | sim | max |IPF−origem|=0.000 · max |IPF−destino|=0.000 (tol 2.0) |
| `ipf_dentro_bounds` | hard | sim | 0 violações em 26160 células (max fora=0.000, tol=2.0) |
| `taxas_validas` | hard | sim | todas as origens-foco OK |
| `sem_colapso_5050` | hard | sim | |Fa2−Fb2|/N=0.031 · |pElimFa−pElimFb|=0.038 |
| `estabilidade` | hard | sim | taxas IPF idênticas=True · bootstrap seed=True |
| `residuo_preditivo` | soft | **não** | mean|resid|/mean(dest) → fa:0.443, fb:0.363, abst:0.161 (tol 0.35) |
| `compat_elim_fa` | hard | sim | Elim×p(Elim→Fa)=7,141.6 ≤ Fa2=200,154.0 |
| `artefatos` | soft | sim | OK |
| `cruzar_oficial_2t` | soft | sim | seções divergentes BU×oficial=0 |

### RO — GO (4698 seções)

| Check | Sev | OK | Detalhe |
|---|---|:---:|---|
| `min_secoes` | hard | sim | 4698 seções (mínimo 50) |
| `identidade` | hard | sim | 4698/4698 seções com margens coerentes (100.00%; mín 99.5%) |
| `ipf_margens` | hard | sim | max |IPF−origem|=0.000 · max |IPF−destino|=0.000 (tol 2.0) |
| `ipf_dentro_bounds` | hard | sim | 0 violações em 93960 células (max fora=0.000, tol=2.0) |
| `taxas_validas` | hard | sim | todas as origens-foco OK |
| `sem_colapso_5050` | hard | sim | |Fa2−Fb2|/N=0.300 · |pElimFa−pElimFb|=0.278 |
| `estabilidade` | hard | sim | taxas IPF idênticas=True · bootstrap seed=True |
| `residuo_preditivo` | soft | sim | mean|resid|/mean(dest) → fa:0.257, fb:0.113, abst:0.159 (tol 0.35) |
| `compat_elim_fa` | hard | sim | Elim×p(Elim→Fa)=15,759.8 ≤ Fa2=294,446.0 |
| `artefatos` | soft | sim | OK |
| `cruzar_oficial_2t` | soft | sim | seções divergentes BU×oficial=0 |

### SE — GO (5923 seções)

| Check | Sev | OK | Detalhe |
|---|---|:---:|---|
| `min_secoes` | hard | sim | 5923 seções (mínimo 50) |
| `identidade` | hard | sim | 5923/5923 seções com margens coerentes (100.00%; mín 99.5%) |
| `ipf_margens` | hard | sim | max |IPF−origem|=0.000 · max |IPF−destino|=0.000 (tol 2.0) |
| `ipf_dentro_bounds` | hard | sim | 0 violações em 118460 células (max fora=0.000, tol=2.0) |
| `taxas_validas` | hard | sim | todas as origens-foco OK |
| `sem_colapso_5050` | hard | sim | |Fa2−Fb2|/N=0.319 · |pElimFa−pElimFb|=0.293 |
| `estabilidade` | hard | sim | taxas IPF idênticas=True · bootstrap seed=True |
| `residuo_preditivo` | soft | sim | mean|resid|/mean(dest) → fa:0.101, fb:0.250, abst:0.202 (tol 0.35) |
| `compat_elim_fa` | hard | sim | Elim×p(Elim→Fa)=50,306.3 ≤ Fa2=989,041.0 |
| `artefatos` | soft | sim | OK |
| `cruzar_oficial_2t` | soft | sim | seções divergentes BU×oficial=0 |

## Critérios hard (bloqueiam GO)

- Mínimo 50 seções em ambos os turnos
- Identidade das margens em ≥99.5% das seções
- IPF fecha origens/destinos (tol 2.0; Δ aptos absorvido em abst)
- IPF cabe nos bounds Duncan–Davis (tol 2.0)
- Taxas ∈ [0,1] e somam ~1 (tol 0.02)
- Sem colapso 50/50 artificial quando destinos 2º são desbalanceados
- Estabilidade determinística (mesmo input → mesmo output)
- Elim×p(Elim→Fa) ≤ Fa2 agregado

## Soft (aviso, não bloqueia)

- Resíduo preditivo médio relativo (tol 0.35) — taxas UF não reproduzem cada seção
- Artefatos `fluxo_*` gravados
- Cruzar oficial 2º sem divergências

## Próximo passo se GO

1. Regravar `fluxo-ecologico` no piloto (IPF atualizado) se os Parquets forem antigos
2. Validar 1–2 UFs médias (`RO` / `SE`) após `audit --turno 2`
3. Só então `fluxo-ecologico --ufs ALL` (e comparar-turnos nacional)
