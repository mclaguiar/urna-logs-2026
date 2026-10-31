# Verificar `.vsc` — AP 2º turno

Nível solicitado: **níveis 1+2** (omitir = hashes e assinatura HW; 1 = só hashes; 2 = só assinatura HW).

## Resumo

- Stems no ZIP: **1,914**
- Com `-vota.vsc`: **1,914**
- Nível ≥1 (auto-hash + hashes dos arquivos presentes + críticos): **1,914**
- Nível 2 Ed521 (UE2020/UE2022, AC UE2020 ou UE2022): **1,914**
- Nível 2 ECDSA (UE2013/UE2015, cadeia AC URNA): **0**
- ECDSA cadeia pendente (assinatura ok, AC URNA não fixada): **0**
- Assinatura HW falhou: **0**
- Críticos (bu/rdv/log) OK: **1,914**
- Algum hash presente falhou: **0**

Arquivos listados na assinatura mas **ausentes** no ZIP público (jufa, wsq*, mr.ver, …) contam como `ausente_pacote` — esperado no CDN.

## Método

- Spec ASN.1: `urna_logs/spec/assinatura.asn1` (TSE 2026)
- Hash: SHA-512 do conteúdo = campo `AssinaturaDigital.hash`
- Nível 2 segue o par declarado em `origemAssinaturaHW`. UE2020/UE2022 com `eddsa`: Ed521 e AC UE2020 ou UE2022. UE2013/UE2015 com `ecdsa`: ECDSA P-521; a mensagem dos arquivos é SHA-512 do hash gravado. Sem a AC URNA fixada, essa assinatura confere com a chave do certificado e a cadeia fica pendente (nível 1). Certificado de outro algoritmo é falha, sem segunda tentativa. Não valida a chave de software da cerimônia.

## Falhas

Nenhuma.

## Arquivos

- `verificar_vsc_AP_2t.parquet`
- `verificar_vsc_AP_2t.csv`
