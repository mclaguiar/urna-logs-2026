# Verificar `.vsc` — DF 2º turno

Nível solicitado: **níveis 1+2** (omitir = hashes e Ed521; 1 = só hashes; 2 = só Ed521).

## Resumo

- Stems no ZIP: **6,969**
- Com `-vota.vsc`: **6,969**
- Nível ≥1 (auto-hash + hashes dos arquivos presentes + críticos): **6,969**
- Nível 2 (Ed521: certificado + auto + hashes): **5,596**
- Assinatura HW falhou: **1,373**
- Críticos (bu/rdv/log) OK: **6,969**
- Algum hash presente falhou: **0**

Arquivos listados na assinatura mas **ausentes** no ZIP público (jufa, wsq*, mr.ver, …) contam como `ausente_pacote` — esperado no CDN.

## Método

- Spec ASN.1: `urna_logs/spec/assinatura.asn1` (TSE 2026)
- Hash: SHA-512 do conteúdo = campo `AssinaturaDigital.hash`
- Nível 2: Ed521 sobre SHA-512 desse hash, com a chave do certificado embutido; o certificado é conferido com a AC UE2020 ou UE2022. Não valida a chave de software da cerimônia.

## Falhas / pendências (até 40)

- `o03221df9701200040242` jk=`DF:97012:0004:0242` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040243` jk=`DF:97012:0004:0243` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040244` jk=`DF:97012:0004:0244` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040245` jk=`DF:97012:0004:0245` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040246` jk=`DF:97012:0004:0246` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040247` jk=`DF:97012:0004:0247` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040248` jk=`DF:97012:0004:0248` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040249` jk=`DF:97012:0004:0249` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040251` jk=`DF:97012:0004:0251` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040253` jk=`DF:97012:0004:0253` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040254` jk=`DF:97012:0004:0254` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040256` jk=`DF:97012:0004:0256` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040257` jk=`DF:97012:0004:0257` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040262` jk=`DF:97012:0004:0262` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040263` jk=`DF:97012:0004:0263` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040264` jk=`DF:97012:0004:0264` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040265` jk=`DF:97012:0004:0265` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040266` jk=`DF:97012:0004:0266` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040267` jk=`DF:97012:0004:0267` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040268` jk=`DF:97012:0004:0268` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040269` jk=`DF:97012:0004:0269` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040270` jk=`DF:97012:0004:0270` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040271` jk=`DF:97012:0004:0271` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040275` jk=`DF:97012:0004:0275` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040276` jk=`DF:97012:0004:0276` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040280` jk=`DF:97012:0004:0280` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040281` jk=`DF:97012:0004:0281` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040282` jk=`DF:97012:0004:0282` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040283` jk=`DF:97012:0004:0283` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040284` jk=`DF:97012:0004:0284` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040285` jk=`DF:97012:0004:0285` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040286` jk=`DF:97012:0004:0286` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040288` jk=`DF:97012:0004:0288` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040289` jk=`DF:97012:0004:0289` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040290` jk=`DF:97012:0004:0290` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040293` jk=`DF:97012:0004:0293` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040294` jk=`DF:97012:0004:0294` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040302` jk=`DF:97012:0004:0302` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040303` jk=`DF:97012:0004:0303` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221df9701200040304` jk=`DF:97012:0004:0304` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`

## Arquivos

- `verificar_vsc_DF_2t.parquet`
- `verificar_vsc_DF_2t.csv`
