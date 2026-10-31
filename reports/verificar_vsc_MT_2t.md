# Verificar `.vsc` — MT 2º turno

Nível solicitado: **níveis 1+2** (omitir = hashes e Ed521; 1 = só hashes; 2 = só Ed521).

## Resumo

- Stems no ZIP: **8,287**
- Com `-vota.vsc`: **8,287**
- Nível ≥1 (auto-hash + hashes dos arquivos presentes + críticos): **8,287**
- Nível 2 (Ed521: certificado + auto + hashes): **6,865**
- Assinatura HW falhou: **1,422**
- Críticos (bu/rdv/log) OK: **8,287**
- Algum hash presente falhou: **0**

Arquivos listados na assinatura mas **ausentes** no ZIP público (jufa, wsq*, mr.ver, …) contam como `ausente_pacote` — esperado no CDN.

## Método

- Spec ASN.1: `urna_logs/spec/assinatura.asn1` (TSE 2026)
- Hash: SHA-512 do conteúdo = campo `AssinaturaDigital.hash`
- Nível 2: Ed521 sobre SHA-512 desse hash, com a chave do certificado embutido; o certificado é conferido com a AC UE2020 ou UE2022. Não valida a chave de software da cerimônia.

## Falhas / pendências (até 40)

- `o03221mt9067000010147` jk=`MT:90670:0001:0147` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010150` jk=`MT:90670:0001:0150` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010154` jk=`MT:90670:0001:0154` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010156` jk=`MT:90670:0001:0156` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010157` jk=`MT:90670:0001:0157` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010158` jk=`MT:90670:0001:0158` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010159` jk=`MT:90670:0001:0159` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010160` jk=`MT:90670:0001:0160` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010166` jk=`MT:90670:0001:0166` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010169` jk=`MT:90670:0001:0169` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010172` jk=`MT:90670:0001:0172` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010174` jk=`MT:90670:0001:0174` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010179` jk=`MT:90670:0001:0179` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010180` jk=`MT:90670:0001:0180` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010181` jk=`MT:90670:0001:0181` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010185` jk=`MT:90670:0001:0185` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010190` jk=`MT:90670:0001:0190` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010202` jk=`MT:90670:0001:0202` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010203` jk=`MT:90670:0001:0203` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010447` jk=`MT:90670:0001:0447` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010448` jk=`MT:90670:0001:0448` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010449` jk=`MT:90670:0001:0449` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010501` jk=`MT:90670:0001:0501` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010502` jk=`MT:90670:0001:0502` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010503` jk=`MT:90670:0001:0503` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010504` jk=`MT:90670:0001:0504` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010505` jk=`MT:90670:0001:0505` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010506` jk=`MT:90670:0001:0506` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010507` jk=`MT:90670:0001:0507` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010508` jk=`MT:90670:0001:0508` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010509` jk=`MT:90670:0001:0509` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010510` jk=`MT:90670:0001:0510` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010511` jk=`MT:90670:0001:0511` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010512` jk=`MT:90670:0001:0512` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010513` jk=`MT:90670:0001:0513` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010737` jk=`MT:90670:0001:0737` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010761` jk=`MT:90670:0001:0761` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010793` jk=`MT:90670:0001:0793` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010819` jk=`MT:90670:0001:0819` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mt9067000010838` jk=`MT:90670:0001:0838` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`

## Arquivos

- `verificar_vsc_MT_2t.parquet`
- `verificar_vsc_MT_2t.csv`
