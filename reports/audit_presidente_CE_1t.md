# Auditoria presidente — CE 1º turno

ZIP: `E:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_CE.zip`
Urnas auditadas: **23,765** · OK: **23,765** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **5,910,471**

| Tipo:número | Votos |
|---|---:|
| `nominal:13` | 3,555,263 |
| `nominal:22` | 1,756,850 |
| `nulo:-` | 189,185 |
| `nominal:70` | 140,524 |
| `nominal:14` | 107,587 |
| `branco:-` | 103,295 |
| `nominal:55` | 45,604 |
| `nominal:30` | 4,310 |
| `nominal:80` | 3,352 |
| `nominal:16` | 1,491 |
| `nominal:27` | 1,071 |
| `nominal:21` | 783 |
| `nominal:29` | 498 |
| `nominal:35` | 481 |
| `nominal:28` | 177 |

## Divergências / erros

Nenhuma divergência encontrada.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
