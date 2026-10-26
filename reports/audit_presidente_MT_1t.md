# Auditoria presidente — MT 1º turno

ZIP: `E:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_MT.zip`
Urnas auditadas: **8,287** · OK: **8,287** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **2,052,133**

| Tipo:número | Votos |
|---|---:|
| `nominal:22` | 1,298,581 |
| `nominal:13` | 581,681 |
| `nominal:70` | 40,019 |
| `nulo:-` | 37,994 |
| `nominal:14` | 33,170 |
| `nominal:55` | 33,079 |
| `branco:-` | 20,756 |
| `nominal:30` | 2,424 |
| `nominal:27` | 1,869 |
| `nominal:80` | 1,584 |
| `nominal:16` | 340 |
| `nominal:21` | 239 |
| `nominal:35` | 172 |
| `nominal:29` | 130 |
| `nominal:28` | 95 |

## Divergências / erros

Nenhuma divergência encontrada.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
