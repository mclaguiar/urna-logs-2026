# Auditoria presidente — AC 1º turno

ZIP: `D:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_AC.zip`
Urnas auditadas: **2,270** · OK: **2,270** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **488,330**

| Tipo:número | Votos |
|---|---:|
| `nominal:22` | 302,807 |
| `nominal:13` | 134,770 |
| `nulo:-` | 13,662 |
| `nominal:70` | 13,523 |
| `nominal:55` | 8,594 |
| `nominal:14` | 7,980 |
| `branco:-` | 5,579 |
| `nominal:30` | 573 |
| `nominal:80` | 314 |
| `nominal:27` | 215 |
| `nominal:21` | 140 |
| `nominal:16` | 71 |
| `nominal:29` | 40 |
| `nominal:35` | 39 |
| `nominal:28` | 23 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
