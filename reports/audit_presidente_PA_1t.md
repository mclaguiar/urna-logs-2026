# Auditoria presidente — PA 1º turno

ZIP: `E:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_PA.zip`
Urnas auditadas: **20,827** · OK: **20,827** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **5,066,504**

| Tipo:número | Votos |
|---|---:|
| `nominal:13` | 2,427,237 |
| `nominal:22` | 2,163,957 |
| `nulo:-` | 148,946 |
| `nominal:70` | 125,172 |
| `nominal:14` | 84,165 |
| `branco:-` | 54,203 |
| `nominal:55` | 51,991 |
| `nominal:80` | 3,824 |
| `nominal:30` | 3,064 |
| `nominal:27` | 1,293 |
| `nominal:16` | 1,045 |
| `nominal:21` | 674 |
| `nominal:35` | 442 |
| `nominal:29` | 308 |
| `nominal:28` | 183 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
