# Auditoria presidente — MS 1º turno

ZIP: `E:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_MS.zip`
Urnas auditadas: **7,106** · OK: **7,106** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **1,541,220**

| Tipo:número | Votos |
|---|---:|
| `nominal:22` | 873,351 |
| `nominal:13` | 516,855 |
| `nominal:70` | 39,148 |
| `nominal:14` | 31,847 |
| `nulo:-` | 29,596 |
| `nominal:55` | 23,291 |
| `branco:-` | 21,270 |
| `nominal:30` | 2,792 |
| `nominal:80` | 1,291 |
| `nominal:27` | 626 |
| `nominal:16` | 353 |
| `nominal:21` | 332 |
| `nominal:35` | 209 |
| `nominal:29` | 183 |
| `nominal:28` | 76 |

## Divergências / erros

Nenhuma divergência encontrada.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
