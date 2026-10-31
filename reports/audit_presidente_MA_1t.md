# Auditoria presidente — MA 1º turno

ZIP: `D:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_MA.zip`
Urnas auditadas: **18,093** · OK: **18,092** · divergentes/erro: **1**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **4,160,124**

| Tipo:número | Votos |
|---|---:|
| `nominal:13` | 2,566,143 |
| `nominal:22` | 1,238,988 |
| `nulo:-` | 103,240 |
| `nominal:70` | 84,828 |
| `nominal:14` | 60,386 |
| `nominal:55` | 50,155 |
| `branco:-` | 46,313 |
| `nominal:30` | 4,584 |
| `nominal:80` | 1,795 |
| `nominal:16` | 1,459 |
| `nominal:27` | 895 |
| `nominal:21` | 475 |
| `nominal:28` | 345 |
| `nominal:35` | 307 |
| `nominal:29` | 211 |

## Divergências / erros

1 urna(s):

- `o03220ma0784600740228` seção `07846-0074-1228-0228`: RDV ausente ou sem presidente

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
