# Verificar `.vsc` — MG 1º turno

Nível solicitado: **níveis 1+2** (omitir = hashes e assinatura HW; 1 = só hashes; 2 = só assinatura HW).

## Resumo

- Stems no ZIP: **52,062**
- Com `-vota.vsc`: **52,062**
- Nível ≥1 (auto-hash + hashes dos arquivos presentes + críticos): **52,062**
- Nível 2 Ed521 (UE2020/UE2022, AC UE2020 ou UE2022): **42,981**
- Nível 2 ECDSA (UE2013/UE2015, cadeia AC URNA): **9,081**
- ECDSA cadeia pendente (assinatura ok, AC URNA não fixada): **0**
- Assinatura HW falhou: **0**
- Críticos (bu/rdv/log) OK: **52,062**
- Algum hash presente falhou: **0**

Arquivos listados na assinatura mas **ausentes** no ZIP público (jufa, wsq*, mr.ver, …) contam como `ausente_pacote` — esperado no CDN.

## Método

- Spec ASN.1: `urna_logs/spec/assinatura.asn1` (TSE 2026)
- Hash: SHA-512 do conteúdo = campo `AssinaturaDigital.hash`
- Nível 2 segue o par declarado em `origemAssinaturaHW`. UE2020/UE2022 com `eddsa`: Ed521 e AC UE2020 ou UE2022. UE2013/UE2015 com `ecdsa`: ECDSA P-521; a mensagem dos arquivos é SHA-512 do hash gravado. O certificado da urna é conferido com a AC URNA publicada em http://acurna.tse.jus.br/crt/acurna.crt (válido até 2026-07-18; a conta confere a assinatura, não a data). Certificado de outro algoritmo é falha, sem segunda tentativa. Não valida a chave de software da cerimônia.

## Pendências

Nenhuma.

## Sistema de apuração

O sufixo `sa` é o boletim do sistema de apuração, não um arquivo de seção com o nome trocado. No boletim, a urna é de contingência e o bloco é o de SA: junta, turma e, quando existe, o número interno da urna de origem que não pôde ser usada.

2 urnas publicam `-sa.vsc`, `-busa.dat` e `-logsa.jez` no lugar de `-vota.vsc`, `-bu.dat` e `-log.jez`. Assinatura de hardware fechou em 2.

- BELO HORIZONTE (41238), zona 39, seção 168. Urna `o03220mg4123800390168`. Assinatura fechou. Comparecimento 281 de 501 aptos. Nominal 13: 130. Nominal 22: 117. Branco: 4. Nulo: 13. BU e RDV com os mesmos totais.
- PIEDADE DOS GERAIS (50075), zona 47, seção 41. Urna `o03220mg5007500470041`. Assinatura fechou. Comparecimento 278 de 379 aptos. Nominal 13: 103. Nominal 22: 125. Branco: 9. Nulo: 15. BU e RDV com os mesmos totais.

## Arquivos

- `verificar_vsc_MG_1t.parquet`
- `verificar_vsc_MG_1t.csv`
