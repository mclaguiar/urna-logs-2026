# Fluxo ecológico 1º→2º — RO

Inferência **agregada por seção** (Duncan–Davis + taxas médias com bootstrap).
Não identifica eleitor a eleitor. Intervalos factíveis ≠ certeza individual.

Fa é o candidato **13**, LUIZ INÁCIO LULA DA SILVA. Fb é o candidato **22**, FLAVIO NANTES BOLSONARO. São os dois números nominais do 2º turno, em ordem numérica.

## Resumo

- Seções (ambos): **4,698** · identidade OK: **4,698**
- Seções com maioria de células “estreitas” (largura ≤ 25%): **0**
- Eliminados *forçados* (limite inf. > 50%) → Fa (13): **0** · → Fb (22): **0**

## Taxas médias UF (Elim / Branco / Nulo / Abst → destinos)

Estimativa = média ponderada das células de uma matriz IPF por seção (casa totais de origem e destino; semente = independência); IC = percentis 5–95 do bootstrap (400 reamostragens de seções). Duncan–Davis (Parquet de bounds) continua sendo o intervalo factível sem modelo.

| Origem 1º | → Fa (13) | → Fb (22) | → Branco | → Nulo | → Abst |
|---|---|---|---|---|---|
| Eliminados | 24.45% [24.27–24.63] | 52.21% [52.02–52.37] | 0.71% [0.70–0.72] | 0.96% [0.94–0.98] | 21.68% [21.56–21.79] |
| Branco | 24.09% [23.88–24.30] | 52.49% [52.27–52.72] | 0.79% [0.77–0.81] | 0.94% [0.92–0.96] | 21.68% [21.56–21.81] |
| Nulo | 24.52% [24.30–24.74] | 52.17% [51.94–52.37] | 0.69% [0.67–0.70] | 1.07% [1.05–1.09] | 21.56% [21.45–21.68] |
| Abstenção | 22.70% [22.53–22.87] | 53.13% [52.94–53.29] | 0.65% [0.64–0.66] | 0.88% [0.86–0.89] | 22.74% [22.63–22.84] |

## Abstenção seletiva (correlação seção)

- corr(% eliminados 1º, Δ abstenção): **0.1257**
- corr(margem 1º, Δ abstenção): **0.1677**

## Hipóteses (evidência agregada, não prova)

| Hipótese | Leitura neste UF |
|---|---|
| Eliminados → sobretudo Fa (13) | taxa Elim→Fa 24.45% [24.27–24.63]; seções forçadas Fa=0 |
| Eliminados → sobretudo Fb (22) | taxa Elim→Fb 52.21% [52.02–52.37]; seções forçadas Fb=0 |
| Branco 1º permanece / migra | →Branco 0.79% [0.77–0.81]; →Fa (13) 24.09% [23.88–24.30]; →Fb (22) 52.49% [52.27–52.72] |
| Nulo 1º | →Nulo 1.07% [1.05–1.09]; →Fa (13) 24.52% [24.30–24.74]; →Fb (22) 52.17% [51.94–52.37] |
| Abstenção seletiva | correlações acima; residual `resid_abst` no Parquet |

## Limites metodológicos

- Duncan–Davis: o que é **matematicamente possível** dados só os totais da seção.
- Taxa média + IC: estimativa sob a hipótese de que o ponto médio do intervalo é um resumo útil e que as seções são trocáveis no bootstrap (troca ecológica).
- RDV≡BU≡CSV comparam a integridade entre os arquivos públicos.

## Arquivos

- Limites por seção: `fluxo_bounds_RO_1t_2t.parquet`
- Taxas bootstrap: `fluxo_taxas_RO_1t_2t.csv`
- Resíduos preditivos: `fluxo_residuos_RO_1t_2t.parquet`
