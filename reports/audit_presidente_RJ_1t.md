# Auditoria presidente — RJ 1º turno

ZIP: `D:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_RJ.zip`
Urnas auditadas: **37,675** · OK: **37,675** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **9,859,802**

| Tipo:número | Votos |
|---|---:|
| `nominal:22` | 4,966,844 |
| `nominal:13` | 3,693,021 |
| `nulo:-` | 287,736 |
| `nominal:70` | 247,397 |
| `nominal:14` | 211,843 |
| `branco:-` | 201,979 |
| `nominal:55` | 199,844 |
| `nominal:30` | 21,907 |
| `nominal:80` | 14,186 |
| `nominal:27` | 4,082 |
| `nominal:16` | 3,999 |
| `nominal:21` | 2,854 |
| `nominal:35` | 1,930 |
| `nominal:29` | 1,793 |
| `nominal:28` | 387 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
