# Verificar `.vsc` — MA 2º turno

Nível solicitado: **níveis 1+2** (omitir = hashes e Ed521; 1 = só hashes; 2 = só Ed521).

## Resumo

- Stems no ZIP: **18,093**
- Com `-vota.vsc`: **18,093**
- Nível ≥1 (auto-hash + hashes dos arquivos presentes + críticos): **18,093**
- Nível 2 (Ed521: certificado + auto + hashes): **14,473**
- Assinatura HW falhou: **3,620**
- Críticos (bu/rdv/log) OK: **18,093**
- Algum hash presente falhou: **0**

Arquivos listados na assinatura mas **ausentes** no ZIP público (jufa, wsq*, mr.ver, …) contam como `ausente_pacote` — esperado no CDN.

## Método

- Spec ASN.1: `urna_logs/spec/assinatura.asn1` (TSE 2026)
- Hash: SHA-512 do conteúdo = campo `AssinaturaDigital.hash`
- Nível 2: Ed521 sobre SHA-512 desse hash, com a chave do certificado embutido; o certificado é conferido com a AC UE2020 ou UE2022. Não valida a chave de software da cerimônia.

## Falhas / pendências (até 40)

- `o03221ma0712900180040` jk=`MA:07129:0018:0040` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180041` jk=`MA:07129:0018:0041` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180042` jk=`MA:07129:0018:0042` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180043` jk=`MA:07129:0018:0043` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180047` jk=`MA:07129:0018:0047` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180048` jk=`MA:07129:0018:0048` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180049` jk=`MA:07129:0018:0049` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180050` jk=`MA:07129:0018:0050` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180051` jk=`MA:07129:0018:0051` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180052` jk=`MA:07129:0018:0052` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180053` jk=`MA:07129:0018:0053` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180054` jk=`MA:07129:0018:0054` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180060` jk=`MA:07129:0018:0060` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180066` jk=`MA:07129:0018:0066` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180067` jk=`MA:07129:0018:0067` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180076` jk=`MA:07129:0018:0076` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180082` jk=`MA:07129:0018:0082` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180088` jk=`MA:07129:0018:0088` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180093` jk=`MA:07129:0018:0093` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180096` jk=`MA:07129:0018:0096` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180097` jk=`MA:07129:0018:0097` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180104` jk=`MA:07129:0018:0104` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180105` jk=`MA:07129:0018:0105` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180109` jk=`MA:07129:0018:0109` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180110` jk=`MA:07129:0018:0110` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180114` jk=`MA:07129:0018:0114` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180125` jk=`MA:07129:0018:0125` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180127` jk=`MA:07129:0018:0127` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180128` jk=`MA:07129:0018:0128` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180132` jk=`MA:07129:0018:0132` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180137` jk=`MA:07129:0018:0137` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180138` jk=`MA:07129:0018:0138` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180139` jk=`MA:07129:0018:0139` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180140` jk=`MA:07129:0018:0140` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180141` jk=`MA:07129:0018:0141` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180164` jk=`MA:07129:0018:0164` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180174` jk=`MA:07129:0018:0174` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180175` jk=`MA:07129:0018:0175` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180183` jk=`MA:07129:0018:0183` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221ma0712900180195` jk=`MA:07129:0018:0195` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`

## Arquivos

- `verificar_vsc_MA_2t.parquet`
- `verificar_vsc_MA_2t.csv`
