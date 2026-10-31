# Auditoria presidente — DF 1º turno

ZIP: `D:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_DF.zip`
Urnas auditadas: **6,969** · OK: **6,969** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **1,831,396**

| Tipo:número | Votos |
|---|---:|
| `nominal:22` | 909,616 |
| `nominal:13` | 675,627 |
| `nominal:55` | 85,076 |
| `nominal:14` | 46,714 |
| `nominal:70` | 45,979 |
| `nulo:-` | 33,169 |
| `branco:-` | 25,362 |
| `nominal:30` | 4,915 |
| `nominal:80` | 2,297 |
| `nominal:16` | 828 |
| `nominal:27` | 716 |
| `nominal:29` | 382 |
| `nominal:21` | 334 |
| `nominal:35` | 324 |
| `nominal:28` | 57 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
