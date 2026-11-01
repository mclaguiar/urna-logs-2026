# Verificar `.vsc` — AM 1º turno

Nível solicitado: **níveis 1+2** (omitir = hashes e assinatura HW; 1 = só hashes; 2 = só assinatura HW).

## Resumo

- Stems no ZIP: **8,157**
- Com `-vota.vsc`: **8,157**
- Nível ≥1 (auto-hash + hashes dos arquivos presentes + críticos): **8,157**
- Nível 2 Ed521 (UE2020/UE2022, AC UE2020 ou UE2022): **5,983**
- Nível 2 ECDSA (UE2013/UE2015, cadeia AC URNA): **2,145**
- ECDSA cadeia pendente (assinatura ok, AC URNA não fixada): **0**
- Assinatura HW falhou: **29**
- Críticos (bu/rdv/log) OK: **8,157**
- Algum hash presente falhou: **0**

Arquivos listados na assinatura mas **ausentes** no ZIP público (jufa, wsq*, mr.ver, …) contam como `ausente_pacote` — esperado no CDN.

## Método

- Spec ASN.1: `urna_logs/spec/assinatura.asn1` (TSE 2026)
- Hash: SHA-512 do conteúdo = campo `AssinaturaDigital.hash`
- Nível 2 segue o par declarado em `origemAssinaturaHW`. UE2020/UE2022 com `eddsa`: Ed521 e AC UE2020 ou UE2022. UE2013/UE2015 com `ecdsa`: ECDSA P-521; a mensagem dos arquivos é SHA-512 do hash gravado. O certificado da urna é conferido com a AC URNA publicada em http://acurna.tse.jus.br/crt/acurna.crt (válido até 2026-07-18; a conta confere a assinatura, não a data). Certificado de outro algoritmo é falha, sem segunda tentativa. Não valida a chave de software da cerimônia.

## Falhas / pendências (até 40)

- `o03220am0255000010684` jk=`AM:02550:0001:0684` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000010698` jk=`AM:02550:0001:0698` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000010743` jk=`AM:02550:0001:0743` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000010898` jk=`AM:02550:0001:0898` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000010924` jk=`AM:02550:0001:0924` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000020783` jk=`AM:02550:0002:0783` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000310408` jk=`AM:02550:0031:0408` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000310696` jk=`AM:02550:0031:0696` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000320878` jk=`AM:02550:0032:0878` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000320932` jk=`AM:02550:0032:0932` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000370502` jk=`AM:02550:0037:0502` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000370576` jk=`AM:02550:0037:0576` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000580743` jk=`AM:02550:0058:0743` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000580834` jk=`AM:02550:0058:0834` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000581052` jk=`AM:02550:0058:1052` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000581063` jk=`AM:02550:0058:1063` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000590698` jk=`AM:02550:0059:0698` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000590776` jk=`AM:02550:0059:0776` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000620321` jk=`AM:02550:0062:0321` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000620489` jk=`AM:02550:0062:0489` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000630332` jk=`AM:02550:0063:0332` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000630704` jk=`AM:02550:0063:0704` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000630712` jk=`AM:02550:0063:0712` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000630809` jk=`AM:02550:0063:0809` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000650494` jk=`AM:02550:0065:0494` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000650639` jk=`AM:02550:0065:0639` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000680657` jk=`AM:02550:0068:0657` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000680666` jk=`AM:02550:0068:0666` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220am0255000700751` jk=`AM:02550:0070:0751` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`

## Arquivos

- `verificar_vsc_AM_1t.parquet`
- `verificar_vsc_AM_1t.csv`
