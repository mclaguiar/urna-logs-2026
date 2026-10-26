# Auditoria presidente — TO 1º turno

ZIP: `E:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_TO.zip`
Urnas auditadas: **4,384** · OK: **4,384** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **965,196**

| Tipo:número | Votos |
|---|---:|
| `nominal:22` | 469,321 |
| `nominal:13` | 404,009 |
| `nulo:-` | 26,377 |
| `nominal:70` | 22,434 |
| `nominal:55` | 20,189 |
| `nominal:14` | 12,983 |
| `branco:-` | 8,344 |
| `nominal:30` | 595 |
| `nominal:80` | 395 |
| `nominal:27` | 171 |
| `nominal:21` | 117 |
| `nominal:16` | 101 |
| `nominal:35` | 67 |
| `nominal:29` | 65 |
| `nominal:28` | 28 |

## Divergências / erros

Nenhuma divergência encontrada.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
