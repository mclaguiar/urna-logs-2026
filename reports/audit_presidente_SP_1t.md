# Auditoria presidente — SP 1º turno

ZIP: `D:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_SP.zip`
Urnas auditadas: **103,656** · OK: **103,656** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **26,431,992**

| Tipo:número | Votos |
|---|---:|
| `nominal:22` | 12,922,023 |
| `nominal:13` | 9,505,413 |
| `nulo:-` | 914,888 |
| `nominal:70` | 892,368 |
| `nominal:14` | 804,310 |
| `branco:-` | 632,801 |
| `nominal:55` | 579,571 |
| `nominal:30` | 94,635 |
| `nominal:80` | 42,532 |
| `nominal:16` | 15,815 |
| `nominal:27` | 10,563 |
| `nominal:21` | 6,129 |
| `nominal:35` | 5,160 |
| `nominal:29` | 4,429 |
| `nominal:28` | 1,355 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
