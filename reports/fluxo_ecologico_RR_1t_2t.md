# Fluxo ecológico 1º→2º — RR

Inferência **agregada por seção** (Duncan–Davis + taxas médias com bootstrap).
Não identifica eleitor a eleitor. Intervalos factíveis ≠ certeza individual.

Fa é o candidato **13**, LUIZ INÁCIO LULA DA SILVA. Fb é o candidato **22**, FLAVIO NANTES BOLSONARO. São os dois números nominais do 2º turno, em ordem numérica.

## Resumo

- Seções (ambos): **1,519** · identidade OK: **1,519**
- Seções com maioria de células “estreitas” (largura ≤ 25%): **0**
- Eliminados *forçados* (limite inf. > 50%) → Fa (13): **0** · → Fb (22): **0**

## Taxas médias UF (Elim / Branco / Nulo / Abst → destinos)

Estimativa = média ponderada das células de uma matriz IPF por seção (casa totais de origem e destino; semente = independência); IC = percentis 5–95 do bootstrap (400 reamostragens de seções). Duncan–Davis (Parquet de bounds) continua sendo o intervalo factível sem modelo.

| Origem 1º | → Fa (13) | → Fb (22) | → Branco | → Nulo | → Abst |
|---|---|---|---|---|---|
| Eliminados | 19.58% [19.34–19.85] | 56.58% [56.24–56.89] | 0.62% [0.60–0.65] | 0.88% [0.85–0.91] | 22.34% [22.04–22.61] |
| Branco | 19.11% [18.83–19.42] | 56.78% [56.35–57.13] | 0.69% [0.66–0.72] | 0.87% [0.83–0.90] | 22.56% [22.23–22.89] |
| Nulo | 21.05% [20.46–21.67] | 53.99% [53.39–54.60] | 0.53% [0.51–0.56] | 0.94% [0.90–0.97] | 23.49% [23.13–23.83] |
| Abstenção | 19.80% [19.43–20.23] | 54.72% [54.25–55.16] | 0.54% [0.52–0.57] | 0.80% [0.78–0.83] | 24.31% [23.99–24.63] |

## Abstenção seletiva (correlação seção)

- corr(% eliminados 1º, Δ abstenção): **-0.299**
- corr(margem 1º, Δ abstenção): **0.0331**

## Hipóteses (evidência agregada, não prova)

| Hipótese | Leitura neste UF |
|---|---|
| Eliminados → sobretudo Fa (13) | taxa Elim→Fa 19.58% [19.34–19.85]; seções forçadas Fa=0 |
| Eliminados → sobretudo Fb (22) | taxa Elim→Fb 56.58% [56.24–56.89]; seções forçadas Fb=0 |
| Branco 1º permanece / migra | →Branco 0.69% [0.66–0.72]; →Fa (13) 19.11% [18.83–19.42]; →Fb (22) 56.78% [56.35–57.13] |
| Nulo 1º | →Nulo 0.94% [0.90–0.97]; →Fa (13) 21.05% [20.46–21.67]; →Fb (22) 53.99% [53.39–54.60] |
| Abstenção seletiva | correlações acima; residual `resid_abst` no Parquet |

## Limites metodológicos

- Duncan–Davis: o que é **matematicamente possível** dados só os totais da seção.
- Taxa média + IC: estimativa sob a hipótese de que o ponto médio do intervalo é um resumo útil e que as seções são trocáveis no bootstrap (troca ecológica).
- RDV≡BU≡CSV comparam a integridade entre os arquivos públicos.

## Arquivos

- Limites por seção: `fluxo_bounds_RR_1t_2t.parquet`
- Taxas bootstrap: `fluxo_taxas_RR_1t_2t.csv`
- Resíduos preditivos: `fluxo_residuos_RR_1t_2t.parquet`
