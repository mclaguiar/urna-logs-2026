# Auditoria presidente — PI 1º turno

ZIP: `D:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_PI.zip`
Urnas auditadas: **10,225** · OK: **10,225** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **2,240,883**

| Tipo:número | Votos |
|---|---:|
| `nominal:13` | 1,523,710 |
| `nominal:22` | 517,028 |
| `nulo:-` | 66,108 |
| `nominal:70` | 47,692 |
| `nominal:14` | 32,274 |
| `branco:-` | 28,329 |
| `nominal:55` | 21,629 |
| `nominal:30` | 1,357 |
| `nominal:80` | 1,099 |
| `nominal:27` | 504 |
| `nominal:16` | 443 |
| `nominal:21` | 319 |
| `nominal:35` | 193 |
| `nominal:29` | 146 |
| `nominal:28` | 52 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
