# Auditoria presidente — PE 1º turno

ZIP: `E:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_PE.zip`
Urnas auditadas: **21,418** · OK: **21,418** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **5,911,062**

| Tipo:número | Votos |
|---|---:|
| `nominal:13` | 3,553,971 |
| `nominal:22` | 1,738,043 |
| `nulo:-` | 200,416 |
| `nominal:70` | 137,960 |
| `branco:-` | 109,491 |
| `nominal:14` | 85,865 |
| `nominal:55` | 73,176 |
| `nominal:30` | 6,060 |
| `nominal:80` | 2,387 |
| `nominal:16` | 1,114 |
| `nominal:27` | 869 |
| `nominal:21` | 705 |
| `nominal:35` | 457 |
| `nominal:29` | 410 |
| `nominal:28` | 138 |

## Divergências / erros

Nenhuma divergência encontrada.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
