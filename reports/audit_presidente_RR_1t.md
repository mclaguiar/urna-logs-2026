# Auditoria presidente — RR 1º turno

ZIP: `E:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_RR.zip`
Urnas auditadas: **1,519** · OK: **1,519** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **332,772**

| Tipo:número | Votos |
|---|---:|
| `nominal:22` | 231,322 |
| `nominal:13` | 74,420 |
| `nominal:70` | 8,579 |
| `nominal:14` | 6,623 |
| `nulo:-` | 4,595 |
| `nominal:55` | 3,639 |
| `branco:-` | 2,618 |
| `nominal:30` | 337 |
| `nominal:80` | 280 |
| `nominal:27` | 168 |
| `nominal:16` | 60 |
| `nominal:21` | 42 |
| `nominal:35` | 41 |
| `nominal:29` | 34 |
| `nominal:28` | 14 |

## Divergências / erros

Nenhuma divergência encontrada.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
