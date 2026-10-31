# Verificar `.vsc` — MG 2º turno

Nível solicitado: **níveis 1+2** (omitir = hashes e Ed521; 1 = só hashes; 2 = só Ed521).

## Resumo

- Stems no ZIP: **52,062**
- Com `-vota.vsc`: **52,062**
- Nível ≥1 (auto-hash + hashes dos arquivos presentes + críticos): **52,062**
- Nível 2 (Ed521: certificado + auto + hashes): **42,981**
- Assinatura HW falhou: **9,081**
- Críticos (bu/rdv/log) OK: **52,062**
- Algum hash presente falhou: **0**

Arquivos listados na assinatura mas **ausentes** no ZIP público (jufa, wsq*, mr.ver, …) contam como `ausente_pacote` — esperado no CDN.

## Método

- Spec ASN.1: `urna_logs/spec/assinatura.asn1` (TSE 2026)
- Hash: SHA-512 do conteúdo = campo `AssinaturaDigital.hash`
- Nível 2: Ed521 sobre SHA-512 desse hash, com a chave do certificado embutido; o certificado é conferido com a AC UE2020 ou UE2022. Não valida a chave de software da cerimônia.

## Falhas / pendências (até 40)

- `o03221mg4015000640001` jk=`MG:40150:0064:0001` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4015000640002` jk=`MG:40150:0064:0002` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4015000640003` jk=`MG:40150:0064:0003` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4015000640004` jk=`MG:40150:0064:0004` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4015000640005` jk=`MG:40150:0064:0005` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4015000640006` jk=`MG:40150:0064:0006` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4015000640007` jk=`MG:40150:0064:0007` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4015000640134` jk=`MG:40150:0064:0134` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4015000640139` jk=`MG:40150:0064:0139` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4015000640156` jk=`MG:40150:0064:0156` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4015000640183` jk=`MG:40150:0064:0183` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4015000640188` jk=`MG:40150:0064:0188` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4015000640192` jk=`MG:40150:0064:0192` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720016` jk=`MG:40320:0172:0016` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720017` jk=`MG:40320:0172:0017` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720018` jk=`MG:40320:0172:0018` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720019` jk=`MG:40320:0172:0019` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720020` jk=`MG:40320:0172:0020` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720021` jk=`MG:40320:0172:0021` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720022` jk=`MG:40320:0172:0022` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720023` jk=`MG:40320:0172:0023` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720024` jk=`MG:40320:0172:0024` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720038` jk=`MG:40320:0172:0038` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720039` jk=`MG:40320:0172:0039` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720040` jk=`MG:40320:0172:0040` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720046` jk=`MG:40320:0172:0046` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720049` jk=`MG:40320:0172:0049` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720050` jk=`MG:40320:0172:0050` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720051` jk=`MG:40320:0172:0051` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720052` jk=`MG:40320:0172:0052` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720054` jk=`MG:40320:0172:0054` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720056` jk=`MG:40320:0172:0056` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720058` jk=`MG:40320:0172:0058` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720059` jk=`MG:40320:0172:0059` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720062` jk=`MG:40320:0172:0062` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720063` jk=`MG:40320:0172:0063` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720066` jk=`MG:40320:0172:0066` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720067` jk=`MG:40320:0172:0067` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720068` jk=`MG:40320:0172:0068` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221mg4032001720069` jk=`MG:40320:0172:0069` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`

## Arquivos

- `verificar_vsc_MG_2t.parquet`
- `verificar_vsc_MG_2t.csv`
