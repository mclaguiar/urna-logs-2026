# Fluxo ecológico 1º→2º — ZZ

Inferência **agregada por seção** (Duncan–Davis + taxas médias com bootstrap).
Não identifica eleitor a eleitor. Intervalos factíveis ≠ certeza individual.

Fa é o candidato **13**, LUIZ INÁCIO LULA DA SILVA. Fb é o candidato **22**, FLAVIO NANTES BOLSONARO. São os dois números nominais do 2º turno, em ordem numérica.

## Resumo

- Seções (ambos): **1,310** · identidade OK: **1,308**
- Seções com maioria de células “estreitas” (largura ≤ 25%): **3**
- Eliminados *forçados* (limite inf. > 50%) → Fa (13): **0** · → Fb (22): **0**

## Taxas médias UF (Elim / Branco / Nulo / Abst → destinos)

Estimativa = média ponderada das células de uma matriz IPF por seção (casa totais de origem e destino; semente = independência); IC = percentis 5–95 do bootstrap (400 reamostragens de seções). Duncan–Davis (Parquet de bounds) continua sendo o intervalo factível sem modelo.

| Origem 1º | → Fa (13) | → Fb (22) | → Branco | → Nulo | → Abst |
|---|---|---|---|---|---|
| Eliminados | 24.03% [23.41–24.73] | 20.27% [19.74–20.79] | 0.64% [0.61–0.67] | 0.69% [0.66–0.71] | 54.38% [53.84–54.91] |
| Branco | 21.06% [20.38–21.84] | 22.32% [21.46–23.10] | 0.82% [0.77–0.87] | 0.73% [0.69–0.76] | 55.07% [54.44–55.76] |
| Nulo | 23.24% [22.58–24.08] | 20.63% [19.93–21.23] | 0.68% [0.64–0.72] | 0.77% [0.74–0.80] | 54.67% [54.05–55.29] |
| Abstenção | 20.30% [19.78–20.84] | 18.06% [17.60–18.48] | 0.48% [0.46–0.50] | 0.52% [0.50–0.54] | 60.67% [60.13–61.19] |

## Abstenção seletiva (correlação seção)

- corr(% eliminados 1º, Δ abstenção): **0.2067**
- corr(margem 1º, Δ abstenção): **-0.2127**

## Hipóteses (evidência agregada, não prova)

| Hipótese | Leitura neste UF |
|---|---|
| Eliminados → sobretudo Fa (13) | taxa Elim→Fa 24.03% [23.41–24.73]; seções forçadas Fa=0 |
| Eliminados → sobretudo Fb (22) | taxa Elim→Fb 20.27% [19.74–20.79]; seções forçadas Fb=0 |
| Branco 1º permanece / migra | →Branco 0.82% [0.77–0.87]; →Fa (13) 21.06% [20.38–21.84]; →Fb (22) 22.32% [21.46–23.10] |
| Nulo 1º | →Nulo 0.77% [0.74–0.80]; →Fa (13) 23.24% [22.58–24.08]; →Fb (22) 20.63% [19.93–21.23] |
| Abstenção seletiva | correlações acima; residual `resid_abst` no Parquet |

## Limites metodológicos

- Duncan–Davis: o que é **matematicamente possível** dados só os totais da seção.
- Taxa média + IC: estimativa sob a hipótese de que o ponto médio do intervalo é um resumo útil e que as seções são trocáveis no bootstrap (troca ecológica).
- RDV≡BU≡CSV comparam a integridade entre os arquivos públicos.

## Arquivos

- Limites por seção: `fluxo_bounds_ZZ_1t_2t.parquet`
- Taxas bootstrap: `fluxo_taxas_ZZ_1t_2t.csv`
- Resíduos preditivos: `fluxo_residuos_ZZ_1t_2t.parquet`
