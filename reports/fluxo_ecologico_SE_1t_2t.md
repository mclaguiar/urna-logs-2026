# Fluxo ecológico 1º→2º — SE

Inferência **agregada por seção** (Duncan–Davis + taxas médias com bootstrap).
Não identifica eleitor a eleitor. Intervalos factíveis ≠ certeza individual.

Fa é o candidato **13**, LUIZ INÁCIO LULA DA SILVA. Fb é o candidato **22**, FLAVIO NANTES BOLSONARO. São os dois números nominais do 2º turno, em ordem numérica.

## Resumo

- Seções (ambos): **5,923** · identidade OK: **5,923**
- Seções com maioria de células “estreitas” (largura ≤ 25%): **1**
- Eliminados *forçados* (limite inf. > 50%) → Fa (13): **0** · → Fb (22): **0**

## Taxas médias UF (Elim / Branco / Nulo / Abst → destinos)

Estimativa = média ponderada das células de uma matriz IPF por seção (casa totais de origem e destino; semente = independência); IC = percentis 5–95 do bootstrap (400 reamostragens de seções). Duncan–Davis (Parquet de bounds) continua sendo o intervalo factível sem modelo.

| Origem 1º | → Fa (13) | → Fb (22) | → Branco | → Nulo | → Abst |
|---|---|---|---|---|---|
| Eliminados | 55.65% [55.51–55.80] | 26.40% [26.23–26.55] | 0.80% [0.79–0.81] | 1.85% [1.83–1.87] | 15.30% [15.21–15.39] |
| Branco | 56.87% [56.70–57.04] | 24.86% [24.66–25.01] | 0.87% [0.85–0.88] | 1.88% [1.85–1.90] | 15.53% [15.44–15.63] |
| Nulo | 57.15% [57.00–57.32] | 24.52% [24.34–24.68] | 0.78% [0.76–0.79] | 1.99% [1.97–2.02] | 15.55% [15.46–15.66] |
| Abstenção | 56.84% [56.69–57.00] | 24.22% [24.05–24.39] | 0.74% [0.73–0.75] | 1.78% [1.76–1.79] | 16.68% [16.58–16.78] |

## Abstenção seletiva (correlação seção)

- corr(% eliminados 1º, Δ abstenção): **-0.0114**
- corr(margem 1º, Δ abstenção): **-0.0441**

## Hipóteses (evidência agregada, não prova)

| Hipótese | Leitura neste UF |
|---|---|
| Eliminados → sobretudo Fa (13) | taxa Elim→Fa 55.65% [55.51–55.80]; seções forçadas Fa=0 |
| Eliminados → sobretudo Fb (22) | taxa Elim→Fb 26.40% [26.23–26.55]; seções forçadas Fb=0 |
| Branco 1º permanece / migra | →Branco 0.87% [0.85–0.88]; →Fa (13) 56.87% [56.70–57.04]; →Fb (22) 24.86% [24.66–25.01] |
| Nulo 1º | →Nulo 1.99% [1.97–2.02]; →Fa (13) 57.15% [57.00–57.32]; →Fb (22) 24.52% [24.34–24.68] |
| Abstenção seletiva | correlações acima; residual `resid_abst` no Parquet |

## Limites metodológicos

- Duncan–Davis: o que é **matematicamente possível** dados só os totais da seção.
- Taxa média + IC: estimativa sob a hipótese de que o ponto médio do intervalo é um resumo útil e que as seções são trocáveis no bootstrap (troca ecológica).
- RDV≡BU≡CSV comparam a integridade entre os arquivos públicos.

## Arquivos

- Limites por seção: `fluxo_bounds_SE_1t_2t.parquet`
- Taxas bootstrap: `fluxo_taxas_SE_1t_2t.csv`
- Resíduos preditivos: `fluxo_residuos_SE_1t_2t.parquet`
