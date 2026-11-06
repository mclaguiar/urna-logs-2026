# Anomalias — MG

Versão dos limiares: 2026.11.01.
O código 22 de 2022 não é o mesmo candidato do código 22 de 2026. A comparação é a contagem de alertas do mesmo procedimento.

## Sonda de formato

- 2026 MG 1º bu: ok
- 2026 MG 1º log: ok
- 2026 MG 1º rdv: ok
- 2026 MG 1º vsc: ok
- 2026 MG 2º bu: ok
- 2026 MG 2º log: ok
- 2026 MG 2º rdv: ok
- 2026 MG 2º vsc: ok

## Falha verificável

| teste | candidato | 2026 1º | 2026 2º | 2022 1º | 2022 2º | esperados | linha de base |
|---|---|---:|---:|---:|---:|---:|---|
| arquivo_ausente | — | 0 | 0 | 0 | 0 | — |  |
| arquivo_corrompido | — | 0 | 0 | 0 | 0 | — |  |
| assinatura_invalida | — | 0 | 0 | 0 | 0 | — |  |
| bu_csv | — | 0 | 0 | 0 | 0 | — |  |
| bu_rdv | — | 0 | 0 | 0 | 0 | — |  |
| formato_nao_decodificado | — | 0 | 0 | 0 | 0 | — |  |
| hash_divergente | — | 0 | 0 | 0 | 0 | — |  |

## Padrão estatístico

| teste | candidato | 2026 1º | 2026 2º | 2022 1º | 2022 2º | esperados | linha de base |
|---|---|---:|---:|---:|---:|---:|---|
| ajuste_hora | — | 61 | 57 | 0 | 0 | — |  |
| contingencia | — | 210 | 164 | 0 | 0 | — |  |
| fingerprint | 13 | 0 | 0 | 0 | 0 | — | Sem base de 2022 decodificada; o histograma não foi comparado. |
| fingerprint | 22 | 0 | 0 | 0 | 0 | — | Sem base de 2022 decodificada; o histograma não foi comparado. |
| intervalo_curto | — | 0 | 0 | 0 | 0 | — |  |
| log_diferente_bu | — | 4 | 1 | 0 | 0 | — |  |
| mebane | — | 1 | 1 | 0 | 0 | 0.05 |  |
| mebane | 13 | 1 | 1 | 0 | 0 | 0.05 |  |
| mebane | 22 | 1 | 1 | 0 | 0 | 0.05 |  |
| numero_redondo | — | 0 | 0 | 0 | 0 | — |  |
| numero_redondo | 13 | 0 | 0 | 0 | 0 | — |  |
| numero_redondo | 22 | 0 | 0 | 0 | 0 | — |  |
| reinicio | — | 203 | 160 | 0 | 0 | — |  |
| residuo_2t | 13 | 0 | 88 | 0 | 0 | 24.22 |  |
| residuo_2t | 22 | 0 | 28 | 0 | 0 | 24.22 |  |
| sem_digital | — | 1859 | 1913 | 0 | 0 | 21.83 |  |
| ultimo_digito | — | 0 | 0 | 0 | 0 | — |  |
| ultimo_digito | 13 | 0 | 0 | 0 | 0 | — |  |
| ultimo_digito | 22 | 0 | 0 | 0 | 0 | — |  |
| voto_fora_janela | — | 0 | 0 | 0 | 0 | — |  |
| z_candidato | 13 | 1406 | 1362 | 0 | 0 | 21.83 |  |
| z_candidato | 22 | 1313 | 1421 | 0 | 0 | 21.83 |  |
| z_comparecimento | — | 1666 | 1579 | 0 | 0 | 21.83 |  |

## Efeito fixo de local

- 2026 MG: 13: efeito fixo de local mantém 12 de 88; 22: efeito fixo de local mantém 6 de 28
