# Auditoria presidente — SC 1º turno

ZIP: `E:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_SC.zip`
Urnas auditadas: **17,326** · OK: **17,326** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **4,648,159**

| Tipo:número | Votos |
|---|---:|
| `nominal:22` | 3,000,020 |
| `nominal:13` | 1,127,168 |
| `nominal:70` | 134,273 |
| `nominal:14` | 132,795 |
| `nominal:55` | 79,911 |
| `nulo:-` | 78,071 |
| `branco:-` | 69,007 |
| `nominal:30` | 16,718 |
| `nominal:80` | 5,049 |
| `nominal:16` | 1,503 |
| `nominal:27` | 1,429 |
| `nominal:21` | 828 |
| `nominal:29` | 643 |
| `nominal:35` | 560 |
| `nominal:28` | 184 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
