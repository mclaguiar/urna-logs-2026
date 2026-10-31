# Auditoria presidente — BA 1º turno

ZIP: `D:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_BA.zip`
Urnas auditadas: **35,476** · OK: **35,476** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **9,053,601**

| Tipo:número | Votos |
|---|---:|
| `nominal:13` | 5,664,771 |
| `nominal:22` | 2,442,585 |
| `nulo:-` | 338,123 |
| `nominal:70` | 195,451 |
| `branco:-` | 154,936 |
| `nominal:55` | 122,705 |
| `nominal:14` | 117,518 |
| `nominal:30` | 6,497 |
| `nominal:80` | 4,649 |
| `nominal:16` | 1,791 |
| `nominal:27` | 1,676 |
| `nominal:21` | 1,299 |
| `nominal:29` | 724 |
| `nominal:35` | 625 |
| `nominal:28` | 251 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
