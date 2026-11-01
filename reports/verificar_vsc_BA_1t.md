# Verificar `.vsc` — BA 1º turno

Nível solicitado: **níveis 1+2** (omitir = hashes e assinatura HW; 1 = só hashes; 2 = só assinatura HW).

## Resumo

- Stems no ZIP: **35,476**
- Com `-vota.vsc`: **35,476**
- Nível ≥1 (auto-hash + hashes dos arquivos presentes + críticos): **35,476**
- Nível 2 Ed521 (UE2020/UE2022, AC UE2020 ou UE2022): **27,487**
- Nível 2 ECDSA (UE2013/UE2015, cadeia AC URNA): **7,883**
- ECDSA cadeia pendente (assinatura ok, AC URNA não fixada): **0**
- Assinatura HW falhou: **106**
- Críticos (bu/rdv/log) OK: **35,476**
- Algum hash presente falhou: **0**

Arquivos listados na assinatura mas **ausentes** no ZIP público (jufa, wsq*, mr.ver, …) contam como `ausente_pacote` — esperado no CDN.

## Método

- Spec ASN.1: `urna_logs/spec/assinatura.asn1` (TSE 2026)
- Hash: SHA-512 do conteúdo = campo `AssinaturaDigital.hash`
- Nível 2 segue o par declarado em `origemAssinaturaHW`. UE2020/UE2022 com `eddsa`: Ed521 e AC UE2020 ou UE2022. UE2013/UE2015 com `ecdsa`: ECDSA P-521; a mensagem dos arquivos é SHA-512 do hash gravado. O certificado da urna é conferido com a AC URNA publicada em http://acurna.tse.jus.br/crt/acurna.crt (válido até 2026-07-18; a conta confere a assinatura, não a data). Certificado de outro algoritmo é falha, sem segunda tentativa. Não valida a chave de software da cerimônia.

## Falhas / pendências (até 40)

- `o03220ba3077501500180` jk=`BA:30775:0150:0180` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3307300740009` jk=`BA:33073:0074:0009` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3307300740271` jk=`BA:33073:0074:0271` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3321901920174` jk=`BA:33219:0192:0174` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3341301230108` jk=`BA:33413:0123:0108` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3341301230154` jk=`BA:33413:0123:0154` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3341301230173` jk=`BA:33413:0123:0173` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3341301230191` jk=`BA:33413:0123:0191` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3377400710245` jk=`BA:33774:0071:0245` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3377400710310` jk=`BA:33774:0071:0310` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3407000310015` jk=`BA:34070:0031:0015` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3413401700066` jk=`BA:34134:0170:0066` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3413401700067` jk=`BA:34134:0170:0067` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3413401700093` jk=`BA:34134:0170:0093` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3413401700223` jk=`BA:34134:0170:0223` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3413401700259` jk=`BA:34134:0170:0259` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3413401710043` jk=`BA:34134:0171:0043` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3413401710070` jk=`BA:34134:0171:0070` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3413401710098` jk=`BA:34134:0171:0098` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3415000780005` jk=`BA:34150:0078:0005` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3415000780042` jk=`BA:34150:0078:0042` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3415000780077` jk=`BA:34150:0078:0077` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3429001270046` jk=`BA:34290:0127:0046` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3429001270217` jk=`BA:34290:0127:0217` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3429001270328` jk=`BA:34290:0127:0328` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3453301580029` jk=`BA:34533:0158:0029` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3461400610100` jk=`BA:34614:0061:0100` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3469001920041` jk=`BA:34690:0192:0041` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3469001920042` jk=`BA:34690:0192:0042` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3469001920212` jk=`BA:34690:0192:0212` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3477001300042` jk=`BA:34770:0130:0042` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3477001300089` jk=`BA:34770:0130:0089` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3481900610115` jk=`BA:34819:0061:0115` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3485101240039` jk=`BA:34851:0124:0039` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3485101240058` jk=`BA:34851:0124:0058` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3515701540307` jk=`BA:35157:0154:0307` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3515701550055` jk=`BA:35157:0155:0055` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3515701550235` jk=`BA:35157:0155:0235` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3515701550276` jk=`BA:35157:0155:0276` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03220ba3515701550884` jk=`BA:35157:0155:0884` nivel_ok=1 erro=`certificado não confere com AC URNA` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`

## Arquivos

- `verificar_vsc_BA_1t.parquet`
- `verificar_vsc_BA_1t.csv`
