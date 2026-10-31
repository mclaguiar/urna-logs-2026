# Auditoria presidente — AM 1º turno

ZIP: `D:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_AM.zip`
Urnas auditadas: **8,157** · OK: **8,157** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **2,234,549**

| Tipo:número | Votos |
|---|---:|
| `nominal:13` | 1,046,996 |
| `nominal:22` | 976,764 |
| `nominal:70` | 77,531 |
| `nulo:-` | 39,302 |
| `nominal:14` | 35,411 |
| `nominal:55` | 28,310 |
| `branco:-` | 24,402 |
| `nominal:80` | 1,867 |
| `nominal:30` | 1,781 |
| `nominal:27` | 929 |
| `nominal:16` | 457 |
| `nominal:35` | 291 |
| `nominal:21` | 265 |
| `nominal:29` | 161 |
| `nominal:28` | 82 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
