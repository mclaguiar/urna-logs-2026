# Auditoria presidente — AL 1º turno

ZIP: `E:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_AL.zip`
Urnas auditadas: **7,101** · OK: **7,101** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **1,938,428**

| Tipo:número | Votos |
|---|---:|
| `nominal:13` | 995,459 |
| `nominal:22` | 735,718 |
| `nulo:-` | 85,787 |
| `nominal:70` | 42,427 |
| `branco:-` | 33,712 |
| `nominal:14` | 26,851 |
| `nominal:55` | 14,198 |
| `nominal:80` | 1,345 |
| `nominal:30` | 1,168 |
| `nominal:27` | 636 |
| `nominal:16` | 431 |
| `nominal:21` | 267 |
| `nominal:35` | 246 |
| `nominal:29` | 110 |
| `nominal:28` | 73 |

## Divergências / erros

Nenhuma divergência encontrada.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
