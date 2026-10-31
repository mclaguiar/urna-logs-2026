# Auditoria presidente — RO 1º turno

ZIP: `D:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_RO.zip`
Urnas auditadas: **4,698** · OK: **4,698** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **991,080**

| Tipo:número | Votos |
|---|---:|
| `nominal:22` | 652,988 |
| `nominal:13` | 250,667 |
| `nominal:70` | 25,280 |
| `nominal:14` | 19,187 |
| `nominal:55` | 16,929 |
| `nulo:-` | 13,109 |
| `branco:-` | 9,846 |
| `nominal:30` | 1,318 |
| `nominal:80` | 843 |
| `nominal:27` | 356 |
| `nominal:16` | 174 |
| `nominal:21` | 160 |
| `nominal:35` | 97 |
| `nominal:28` | 66 |
| `nominal:29` | 60 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
