# Auditoria presidente — RS 1º turno

ZIP: `D:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_RS.zip`
Urnas auditadas: **27,547** · OK: **27,547** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **6,702,903**

| Tipo:número | Votos |
|---|---:|
| `nominal:22` | 3,573,783 |
| `nominal:13` | 2,294,759 |
| `nominal:70` | 195,296 |
| `nominal:14` | 167,558 |
| `nominal:55` | 158,821 |
| `branco:-` | 148,339 |
| `nulo:-` | 131,265 |
| `nominal:30` | 18,988 |
| `nominal:80` | 6,632 |
| `nominal:16` | 2,146 |
| `nominal:27` | 2,066 |
| `nominal:29` | 1,043 |
| `nominal:21` | 1,031 |
| `nominal:35` | 923 |
| `nominal:28` | 253 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
