# Auditoria presidente — PB 1º turno

ZIP: `E:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_PB.zip`
Urnas auditadas: **10,712** · OK: **10,712** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **2,683,988**

| Tipo:número | Votos |
|---|---:|
| `nominal:13` | 1,541,127 |
| `nominal:22` | 831,377 |
| `nulo:-` | 117,854 |
| `nominal:70` | 73,831 |
| `branco:-` | 52,297 |
| `nominal:14` | 42,247 |
| `nominal:55` | 19,511 |
| `nominal:30` | 1,988 |
| `nominal:80` | 1,593 |
| `nominal:16` | 627 |
| `nominal:27` | 604 |
| `nominal:21` | 347 |
| `nominal:29` | 274 |
| `nominal:35` | 221 |
| `nominal:28` | 90 |

## Divergências / erros

Nenhuma divergência encontrada.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
