# Anomalias — SP

Versão dos limiares: 2026.11.01.
O código 22 de 2022 não é o mesmo candidato do código 22 de 2026. A comparação é a contagem de alertas do mesmo procedimento.

## Sonda de formato

- 2026 SP 1º bu: ok
- 2026 SP 1º log: ok
- 2026 SP 1º rdv: ok
- 2026 SP 1º vsc: ok
- 2026 SP 2º bu: ok
- 2026 SP 2º log: ok
- 2026 SP 2º rdv: ok
- 2026 SP 2º vsc: ok

## Falha verificável

| teste | candidato | 2026 1º | 2026 2º | 2022 1º | 2022 2º | esperados | linha de base |
|---|---|---:|---:|---:|---:|---:|---|
| arquivo_ausente | — | 0 | 1 | 0 | 0 | — |  |
| arquivo_corrompido | — | 0 | 0 | 0 | 0 | — |  |
| assinatura_invalida | — | 0 | 0 | 0 | 0 | — |  |
| bu_csv | — | 0 | 0 | 0 | 0 | — |  |
| bu_rdv | — | 0 | 0 | 0 | 0 | — |  |
| formato_nao_decodificado | — | 0 | 0 | 0 | 0 | — |  |
| hash_divergente | — | 0 | 0 | 0 | 0 | — |  |

## Padrão estatístico

| teste | candidato | 2026 1º | 2026 2º | 2022 1º | 2022 2º | esperados | linha de base |
|---|---|---:|---:|---:|---:|---:|---|
| ajuste_hora | — | 338 | 135 | 0 | 0 | — |  |
| contingencia | — | 620 | 435 | 0 | 0 | — |  |
| fingerprint | 13 | 0 | 0 | 0 | 0 | — | Sem base de 2022 decodificada; o histograma não foi comparado. |
| fingerprint | 22 | 0 | 0 | 0 | 0 | — | Sem base de 2022 decodificada; o histograma não foi comparado. |
| intervalo_curto | — | 0 | 0 | 0 | 0 | — |  |
| log_diferente_bu | — | 4 | 0 | 0 | 0 | — |  |
| mebane | — | 1 | 1 | 0 | 0 | 0.05 |  |
| mebane | 13 | 1 | 1 | 0 | 0 | 0.05 |  |
| mebane | 22 | 1 | 1 | 0 | 0 | 0.05 |  |
| numero_redondo | — | 0 | 0 | 0 | 0 | — |  |
| numero_redondo | 13 | 0 | 0 | 0 | 0 | — |  |
| numero_redondo | 22 | 0 | 0 | 0 | 0 | — |  |
| reinicio | — | 566 | 389 | 0 | 0 | — |  |
| residuo_2t | 13 | 0 | 66 | 0 | 0 | 48.23 |  |
| residuo_2t | 22 | 0 | 37 | 0 | 0 | 48.23 |  |
| sem_digital | — | 2434 | 2373 | 0 | 0 | 47.64 |  |
| ultimo_digito | — | 0 | 0 | 0 | 0 | — |  |
| ultimo_digito | 13 | 0 | 0 | 0 | 0 | — |  |
| ultimo_digito | 22 | 0 | 0 | 0 | 0 | — |  |
| voto_fora_janela | — | 0 | 0 | 0 | 0 | — |  |
| z_candidato | 13 | 2180 | 2244 | 0 | 0 | 47.64 |  |
| z_candidato | 22 | 2213 | 2167 | 0 | 0 | 47.64 |  |
| z_comparecimento | — | 2651 | 2679 | 0 | 0 | 47.64 |  |

## Efeito fixo de local

- 2026 SP: 13: efeito fixo de local mantém 39 de 66; 22: efeito fixo de local mantém 24 de 37
