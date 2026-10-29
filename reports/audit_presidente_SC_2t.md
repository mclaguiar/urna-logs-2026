# Auditoria presidente — SC 2º turno

ZIP: `E:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_2t_SC.zip`
Urnas auditadas: **17,326** · OK: **17,326** · divergentes/erro: **0**

## Escopo

- Cargo: **presidente** apenas
- Checagem: recontar cada voto do RDV e comparar com totais do BU (por candidato / branco / nulo)

## Totais agregados (BU das urnas OK)

Votos contabilizados: **4,762,303**

| Tipo:número | Votos |
|---|---:|
| `nominal:22` | 3,220,071 |
| `nominal:13` | 1,418,314 |
| `nulo:-` | 75,244 |
| `branco:-` | 48,674 |

## Divergências / erros

Nenhuma divergência entre **RDV** e **BU** nas urnas processadas. Isso indica apenas que os **arquivos públicos da urna estão íntegros entre si** (o recontar do RDV bate com os totais do BU) — não avalia origem do voto nem inconsistência com o mundo físico.

## Método

- Schemas ASN.1 oficiais TSE 2026 (`bu.asn1`, `rdv.asn1`)
- RDV: cada `Voto` do cargo presidente é contado
- Tipos especiais RDV (nulo/branco após suspensão etc.) normalizados para o enum do BU
- Legenda (se houver): digitação do RDV reduzida aos 2 dígitos do partido
- Sem divergência = **integridade entre arquivos públicos** (RDV ≡ BU), não auditoria do hardware nem da origem do voto
