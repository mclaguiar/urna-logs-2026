# Auditoria presidente — PR 1º turno

ZIP: `D:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_PR.zip`
Urnas auditadas: **27,142** · OK: **27,142** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **6,841,457**

| Tipo:número | Votos |
|---|---:|
| `nominal:22` | 3,945,345 |
| `nominal:13` | 2,054,597 |
| `nominal:70` | 205,095 |
| `nominal:14` | 177,434 |
| `nominal:55` | 171,294 |
| `nulo:-` | 133,447 |
| `branco:-` | 122,499 |
| `nominal:30` | 17,172 |
| `nominal:80` | 6,731 |
| `nominal:27` | 2,445 |
| `nominal:16` | 2,056 |
| `nominal:21` | 1,195 |
| `nominal:35` | 962 |
| `nominal:29` | 917 |
| `nominal:28` | 268 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
