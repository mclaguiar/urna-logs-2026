# Fluxo ecológico 1º→2º — AC

Inferência **agregada por seção** (Duncan–Davis + taxas médias com bootstrap).
Não identifica eleitor a eleitor. Intervalos factíveis ≠ certeza individual.

Fa é o candidato **13**, LUIZ INÁCIO LULA DA SILVA. Fb é o candidato **22**, FLAVIO NANTES BOLSONARO. São os dois números nominais do 2º turno, em ordem numérica.

## Resumo

- Seções (ambos): **2,270** · identidade OK: **2,270**
- Seções com maioria de células “estreitas” (largura ≤ 25%): **0**
- Eliminados *forçados* (limite inf. > 50%) → Fa (13): **0** · → Fb (22): **0**

## Taxas médias UF (Elim / Branco / Nulo / Abst → destinos)

Estimativa = média ponderada das células de uma matriz IPF por seção (casa totais de origem e destino; semente = independência); IC = percentis 5–95 do bootstrap (400 reamostragens de seções). Duncan–Davis (Parquet de bounds) continua sendo o intervalo factível sem modelo.

| Origem 1º | → Fa (13) | → Fb (22) | → Branco | → Nulo | → Abst |
|---|---|---|---|---|---|
| Eliminados | 23.86% [23.69–24.05] | 48.05% [47.82–48.28] | 0.93% [0.90–0.95] | 2.53% [2.49–2.58] | 24.63% [24.39–24.85] |
| Branco | 23.58% [23.38–23.81] | 47.81% [47.52–48.08] | 0.95% [0.93–0.99] | 2.63% [2.58–2.68] | 25.02% [24.76–25.27] |
| Nulo | 23.82% [23.55–24.10] | 45.89% [45.51–46.31] | 0.79% [0.77–0.82] | 3.01% [2.95–3.07] | 26.48% [26.18–26.76] |
| Abstenção | 23.59% [23.35–23.83] | 45.97% [45.62–46.31] | 0.81% [0.79–0.83] | 2.70% [2.65–2.75] | 27.11% [26.83–27.37] |

## Abstenção seletiva (correlação seção)

- corr(% eliminados 1º, Δ abstenção): **-0.3874**
- corr(margem 1º, Δ abstenção): **0.1021**

## Hipóteses (evidência agregada, não prova)

| Hipótese | Leitura neste UF |
|---|---|
| Eliminados → sobretudo Fa (13) | taxa Elim→Fa 23.86% [23.69–24.05]; seções forçadas Fa=0 |
| Eliminados → sobretudo Fb (22) | taxa Elim→Fb 48.05% [47.82–48.28]; seções forçadas Fb=0 |
| Branco 1º permanece / migra | →Branco 0.95% [0.93–0.99]; →Fa (13) 23.58% [23.38–23.81]; →Fb (22) 47.81% [47.52–48.08] |
| Nulo 1º | →Nulo 3.01% [2.95–3.07]; →Fa (13) 23.82% [23.55–24.10]; →Fb (22) 45.89% [45.51–46.31] |
| Abstenção seletiva | correlações acima; residual `resid_abst` no Parquet |

## Limites metodológicos

- Duncan–Davis: o que é **matematicamente possível** dados só os totais da seção.
- Taxa média + IC: estimativa sob a hipótese de que o ponto médio do intervalo é um resumo útil e que as seções são trocáveis no bootstrap (troca ecológica).
- RDV≡BU≡CSV comparam a integridade entre os arquivos públicos.

## Arquivos

- Limites por seção: `fluxo_bounds_AC_1t_2t.parquet`
- Taxas bootstrap: `fluxo_taxas_AC_1t_2t.csv`
- Resíduos preditivos: `fluxo_residuos_AC_1t_2t.parquet`
