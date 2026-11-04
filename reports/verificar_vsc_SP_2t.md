# Verificar `.vsc` — SP 2º turno

Nível solicitado: **níveis 1+2** (omitir = hashes e assinatura HW; 1 = só hashes; 2 = só assinatura HW).

## Resumo

- Stems no ZIP: **103,656**
- Com `-vota.vsc`: **103,656**
- Nível ≥1 (auto-hash + hashes dos arquivos presentes + críticos): **103,655**
- Nível 2 Ed521 (UE2020/UE2022, AC UE2020 ou UE2022): **81,813**
- Nível 2 ECDSA (UE2013/UE2015, cadeia AC URNA): **21,842**
- ECDSA cadeia pendente (assinatura ok, AC URNA não fixada): **0**
- Assinatura HW falhou: **0**
- Críticos (bu/rdv/log) OK: **103,655**
- Algum hash presente falhou: **0**

Arquivos listados na assinatura mas **ausentes** no ZIP público (jufa, wsq*, mr.ver, …) contam como `ausente_pacote` — esperado no CDN.

## Método

- Spec ASN.1: `urna_logs/spec/assinatura.asn1` (TSE 2026)
- Hash: SHA-512 do conteúdo = campo `AssinaturaDigital.hash`
- Nível 2 segue o par declarado em `origemAssinaturaHW`. UE2020/UE2022 com `eddsa`: Ed521 e AC UE2020 ou UE2022. UE2013/UE2015 com `ecdsa`: ECDSA P-521; a mensagem dos arquivos é SHA-512 do hash gravado. O certificado da urna é conferido com a AC URNA publicada em http://acurna.tse.jus.br/crt/acurna.crt (válido até 2026-07-18; a conta confere a assinatura, não a data). Certificado de outro algoritmo é falha, sem segunda tentativa. Não valida a chave de software da cerimônia.

## Urnas que a verificação não fechou

Arquivo ausente no pacote não é assinatura inválida: a conta não chegou a conferir a assinatura.

- GUARULHOS (64777), zona 395, seção 298. Urna `o03221sp6477703950298`. Falta `log.jez` no pacote. Os hashes de `bu.dat` e `rdv.dat` fecharam. A assinatura de hardware não foi conferida. No ZIP: bu.dat, imgbu.dat, rdv.dat, vota.vsc. Comparecimento 268 de 350 aptos. Nominal 13: 135. Nominal 22: 125. Branco: 2. Nulo: 6. BU e RDV com os mesmos totais.

## Arquivos

- `verificar_vsc_SP_2t.parquet`
- `verificar_vsc_SP_2t.csv`
