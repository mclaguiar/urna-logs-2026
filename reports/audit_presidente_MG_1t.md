# Auditoria presidente — MG 1º turno

ZIP: `D:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_MG.zip`
Urnas auditadas: **52,062** · OK: **52,062** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **12,637,274**

| Tipo:número | Votos |
|---|---:|
| `nominal:22` | 5,777,548 |
| `nominal:13` | 5,188,936 |
| `nominal:70` | 409,737 |
| `nulo:-` | 392,176 |
| `branco:-` | 268,302 |
| `nominal:14` | 247,209 |
| `nominal:55` | 230,423 |
| `nominal:30` | 98,407 |
| `nominal:80` | 11,026 |
| `nominal:16` | 4,085 |
| `nominal:27` | 3,411 |
| `nominal:21` | 2,300 |
| `nominal:35` | 1,732 |
| `nominal:29` | 1,421 |
| `nominal:28` | 561 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
