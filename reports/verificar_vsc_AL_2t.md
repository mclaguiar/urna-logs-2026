# Verificar `.vsc` — AL 2º turno

Nível solicitado: **níveis 1+2** (omitir = hashes e assinatura HW; 1 = só hashes; 2 = só assinatura HW).

## Resumo

- Stems no ZIP: **7,101**
- Com `-vota.vsc`: **7,101**
- Nível ≥1 (auto-hash + hashes dos arquivos presentes + críticos): **7,101**
- Nível 2 Ed521 (UE2020/UE2022, AC UE2020 ou UE2022): **5,606**
- Nível 2 ECDSA (UE2013/UE2015, cadeia AC URNA): **1,478**
- ECDSA cadeia pendente (assinatura ok, AC URNA não fixada): **0**
- Assinatura HW falhou: **17**
- Críticos (bu/rdv/log) OK: **7,101**
- Algum hash presente falhou: **0**

Arquivos listados na assinatura mas **ausentes** no ZIP público (jufa, wsq*, mr.ver, …) contam como `ausente_pacote` — esperado no CDN.

## Método

- Spec ASN.1: `urna_logs/spec/assinatura.asn1` (TSE 2026)
- Hash: SHA-512 do conteúdo = campo `AssinaturaDigital.hash`
- Nível 2 segue o par declarado em `origemAssinaturaHW`. UE2020/UE2022 com `eddsa`: Ed521 e AC UE2020 ou UE2022. UE2013/UE2015 com `ecdsa`: ECDSA P-521; a mensagem dos arquivos é SHA-512 do hash gravado. O certificado da urna é conferido com a AC URNA publicada em http://acurna.tse.jus.br/crt/acurna.crt (válido até 2026-07-18; a conta confere a assinatura, não a data). Certificado de outro algoritmo é falha, sem segunda tentativa. Não valida a chave de software da cerimônia.

## Falhas / pendências (até 40)

- `o03221al2701400390028` jk=`AL:27014:0039:0028` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2701400390126` jk=`AL:27014:0039:0126` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2704900460082` jk=`AL:27049:0046:0082` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2731600270012` jk=`AL:27316:0027:0012` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2747200400032` jk=`AL:27472:0040:0032` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2787100310160` jk=`AL:27871:0031:0160` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2787100310162` jk=`AL:27871:0031:0162` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2813400110099` jk=`AL:28134:0011:0099` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2813400110126` jk=`AL:28134:0011:0126` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2825800100070` jk=`AL:28258:0010:0070` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2825800100071` jk=`AL:28258:0010:0071` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2825800100093` jk=`AL:28258:0010:0093` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2825800100137` jk=`AL:28258:0010:0137` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2825800100302` jk=`AL:28258:0010:0302` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2843600500042` jk=`AL:28436:0050:0042` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2859200190180` jk=`AL:28592:0019:0180` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221al2859200190233` jk=`AL:28592:0019:0233` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`

## Arquivos

- `verificar_vsc_AL_2t.parquet`
- `verificar_vsc_AL_2t.csv`
