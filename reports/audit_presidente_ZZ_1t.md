# Auditoria presidente — ZZ 1º turno

ZIP: `D:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_ZZ.zip`
Urnas auditadas: **1,310** · OK: **1,310** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **341,766**

| Tipo:número | Votos |
|---|---:|
| `nominal:13` | 157,387 |
| `nominal:22` | 143,900 |
| `nominal:70` | 9,734 |
| `nominal:14` | 8,580 |
| `branco:-` | 5,816 |
| `nulo:-` | 4,945 |
| `nominal:55` | 4,708 |
| `nominal:30` | 3,329 |
| `nominal:80` | 1,053 |
| `nominal:27` | 825 |
| `nominal:21` | 421 |
| `nominal:16` | 373 |
| `nominal:35` | 373 |
| `nominal:29` | 199 |
| `nominal:28` | 123 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
