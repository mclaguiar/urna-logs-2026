# Fluxo ecológico 1º→2º — AP

Inferência **agregada por seção** (Duncan–Davis + taxas médias com bootstrap).
Não identifica eleitor a eleitor. Intervalos factíveis ≠ certeza individual.

Fa é o candidato **13**, LUIZ INÁCIO LULA DA SILVA. Fb é o candidato **22**, FLAVIO NANTES BOLSONARO. São os dois números nominais do 2º turno, em ordem numérica.

## Resumo

- Seções (ambos): **1,914** · identidade OK: **1,914**
- Seções com maioria de células “estreitas” (largura ≤ 25%): **0**
- Eliminados *forçados* (limite inf. > 50%) → Fa (13): **0** · → Fb (22): **0**

## Taxas médias UF (Elim / Branco / Nulo / Abst → destinos)

Estimativa = média ponderada das células de uma matriz IPF por seção (casa totais de origem e destino; semente = independência); IC = percentis 5–95 do bootstrap (400 reamostragens de seções). Duncan–Davis (Parquet de bounds) continua sendo o intervalo factível sem modelo.

| Origem 1º | → Fa (13) | → Fb (22) | → Branco | → Nulo | → Abst |
|---|---|---|---|---|---|
| Eliminados | 38.17% [37.95–38.38] | 35.94% [35.69–36.21] | 0.63% [0.61–0.64] | 0.92% [0.90–0.95] | 24.34% [24.07–24.62] |
| Branco | 37.96% [37.70–38.22] | 35.89% [35.57–36.21] | 0.68% [0.65–0.70] | 0.91% [0.88–0.95] | 24.56% [24.20–24.88] |
| Nulo | 38.73% [38.40–39.04] | 34.36% [33.99–34.74] | 0.58% [0.56–0.60] | 0.98% [0.94–1.01] | 25.35% [25.04–25.65] |
| Abstenção | 37.82% [37.54–38.09] | 33.58% [33.29–33.89] | 0.57% [0.55–0.58] | 0.85% [0.82–0.88] | 27.30% [26.92–27.63] |

## Abstenção seletiva (correlação seção)

- corr(% eliminados 1º, Δ abstenção): **-0.2632**
- corr(margem 1º, Δ abstenção): **0.2443**

## Hipóteses (evidência agregada, não prova)

| Hipótese | Leitura neste UF |
|---|---|
| Eliminados → sobretudo Fa (13) | taxa Elim→Fa 38.17% [37.95–38.38]; seções forçadas Fa=0 |
| Eliminados → sobretudo Fb (22) | taxa Elim→Fb 35.94% [35.69–36.21]; seções forçadas Fb=0 |
| Branco 1º permanece / migra | →Branco 0.68% [0.65–0.70]; →Fa (13) 37.96% [37.70–38.22]; →Fb (22) 35.89% [35.57–36.21] |
| Nulo 1º | →Nulo 0.98% [0.94–1.01]; →Fa (13) 38.73% [38.40–39.04]; →Fb (22) 34.36% [33.99–34.74] |
| Abstenção seletiva | correlações acima; residual `resid_abst` no Parquet |

## Limites metodológicos

- Duncan–Davis: o que é **matematicamente possível** dados só os totais da seção.
- Taxa média + IC: estimativa sob a hipótese de que o ponto médio do intervalo é um resumo útil e que as seções são trocáveis no bootstrap (troca ecológica).
- RDV≡BU≡CSV comparam a integridade entre os arquivos públicos.

## Arquivos

- Limites por seção: `fluxo_bounds_AP_1t_2t.parquet`
- Taxas bootstrap: `fluxo_taxas_AP_1t_2t.csv`
- Resíduos preditivos: `fluxo_residuos_AP_1t_2t.parquet`
