# Auditoria presidente — AP 1º turno

ZIP: `D:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_AP.zip`
Urnas auditadas: **1,914** · OK: **1,914** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **476,562**

| Tipo:número | Votos |
|---|---:|
| `nominal:13` | 212,503 |
| `nominal:22` | 212,278 |
| `nominal:70` | 19,057 |
| `nominal:14` | 11,342 |
| `nominal:55` | 8,304 |
| `nulo:-` | 7,272 |
| `branco:-` | 4,415 |
| `nominal:80` | 508 |
| `nominal:30` | 341 |
| `nominal:27` | 229 |
| `nominal:16` | 132 |
| `nominal:21` | 62 |
| `nominal:29` | 53 |
| `nominal:35` | 49 |
| `nominal:28` | 17 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
