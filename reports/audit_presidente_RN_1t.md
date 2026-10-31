# Auditoria presidente — RN 1º turno

ZIP: `D:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_RN.zip`
Urnas auditadas: **8,115** · OK: **8,115** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **2,171,013**

| Tipo:número | Votos |
|---|---:|
| `nominal:13` | 1,237,963 |
| `nominal:22` | 720,493 |
| `nulo:-` | 65,880 |
| `nominal:70` | 57,367 |
| `nominal:14` | 35,261 |
| `branco:-` | 33,172 |
| `nominal:55` | 16,407 |
| `nominal:30` | 1,525 |
| `nominal:80` | 1,228 |
| `nominal:16` | 572 |
| `nominal:27` | 405 |
| `nominal:21` | 315 |
| `nominal:35` | 185 |
| `nominal:29` | 177 |
| `nominal:28` | 63 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
