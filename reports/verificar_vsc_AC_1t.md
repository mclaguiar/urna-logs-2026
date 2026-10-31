# Verificar `.vsc` — AC 1º turno

Nível solicitado: **níveis 1+2** (omitir = hashes e assinatura HW; 1 = só hashes; 2 = só assinatura HW).

## Resumo

- Stems no ZIP: **2,270**
- Com `-vota.vsc`: **2,270**
- Nível ≥1 (auto-hash + hashes dos arquivos presentes + críticos): **2,270**
- Nível 2 Ed521 (UE2020/UE2022, AC UE2020 ou UE2022): **2,270**
- Nível 2 ECDSA (UE2013/UE2015, cadeia AC URNA): **0**
- ECDSA cadeia pendente (assinatura ok, AC URNA não fixada): **0**
- Assinatura HW falhou: **0**
- Críticos (bu/rdv/log) OK: **2,270**
- Algum hash presente falhou: **0**

Arquivos listados na assinatura mas **ausentes** no ZIP público (jufa, wsq*, mr.ver, …) contam como `ausente_pacote` — esperado no CDN.

## Método

- Spec ASN.1: `urna_logs/spec/assinatura.asn1` (TSE 2026)
- Hash: SHA-512 do conteúdo = campo `AssinaturaDigital.hash`
- Nível 2 segue o par declarado em `origemAssinaturaHW`. UE2020/UE2022 com `eddsa`: Ed521 e AC UE2020 ou UE2022. UE2013/UE2015 com `ecdsa`: ECDSA P-521; a mensagem dos arquivos é SHA-512 do hash gravado. O certificado da urna é conferido com a AC URNA publicada em http://acurna.tse.jus.br/crt/acurna.crt (válido até 2026-07-18; a conta confere a assinatura, não a data). Certificado de outro algoritmo é falha, sem segunda tentativa. Não valida a chave de software da cerimônia.

## Falhas

Nenhuma.

## Arquivos

- `verificar_vsc_AC_1t.parquet`
- `verificar_vsc_AC_1t.csv`
