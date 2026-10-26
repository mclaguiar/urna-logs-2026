# Auditoria presidente — GO 1º turno

ZIP: `E:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_GO.zip`
Urnas auditadas: **15,686** · OK: **15,686** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **3,971,587**

| Tipo:número | Votos |
|---|---:|
| `nominal:22` | 2,051,888 |
| `nominal:13` | 1,188,880 |
| `nominal:55` | 472,041 |
| `nulo:-` | 98,014 |
| `nominal:14` | 54,105 |
| `nominal:70` | 53,849 |
| `branco:-` | 45,643 |
| `nominal:30` | 2,672 |
| `nominal:80` | 2,087 |
| `nominal:16` | 668 |
| `nominal:27` | 559 |
| `nominal:21` | 468 |
| `nominal:35` | 346 |
| `nominal:29` | 260 |
| `nominal:28` | 107 |

## Divergências / erros

Nenhuma divergência encontrada.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
