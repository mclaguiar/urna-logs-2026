# Verificar `.vsc` — ZZ 1º turno

Nível solicitado: **níveis 1+2** (omitir = hashes e assinatura HW; 1 = só hashes; 2 = só assinatura HW).

## Resumo

- Stems no ZIP: **1,310**
- Com `-vota.vsc`: **1,310**
- Nível ≥1 (auto-hash + hashes dos arquivos presentes + críticos): **1,310**
- Nível 2 Ed521 (UE2020/UE2022, AC UE2020 ou UE2022): **0**
- Nível 2 ECDSA (UE2013/UE2015, cadeia AC URNA): **1,310**
- ECDSA cadeia pendente (assinatura ok, AC URNA não fixada): **0**
- Assinatura HW falhou: **0**
- Críticos (bu/rdv/log) OK: **1,310**
- Algum hash presente falhou: **0**

Arquivos listados na assinatura mas **ausentes** no ZIP público (jufa, wsq*, mr.ver, …) contam como `ausente_pacote` — esperado no CDN.

## Método

- Spec ASN.1: `urna_logs/spec/assinatura.asn1` (TSE 2026)
- Hash: SHA-512 do conteúdo = campo `AssinaturaDigital.hash`
- Nível 2 segue o par declarado em `origemAssinaturaHW`. UE2020/UE2022 com `eddsa`: Ed521 e AC UE2020 ou UE2022. UE2013/UE2015 com `ecdsa`: ECDSA P-521; a mensagem dos arquivos é SHA-512 do hash gravado. O certificado da urna é conferido com a AC URNA publicada em http://acurna.tse.jus.br/crt/acurna.crt (válido até 2026-07-18; a conta confere a assinatura, não a data). Certificado de outro algoritmo é falha, sem segunda tentativa. Não valida a chave de software da cerimônia.

## Pendências

Nenhuma.

## Seção agregada

29 urnas publicam `-sa.vsc`, `-busa.dat` e `-logsa.jez` em vez de `-vota.vsc`, `-bu.dat` e `-log.jez`. Assinatura de hardware fechou em 29.

- KATMANDU (29173), zona 1, seção 494. Urna `o03220zz2917300010494`. Assinatura fechou. Comparecimento 13 de 32 aptos. Nominal 13: 1. Nominal 22: 11. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- ABIDJÃ (29254), zona 1, seção 1. Urna `o03220zz2925400010001`. Assinatura fechou. Comparecimento 44 de 91 aptos. Nominal 13: 24. Nominal 22: 13. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- ACCRA (29270), zona 1, seção 3. Urna `o03220zz2927000010003`. Assinatura fechou. Comparecimento 13 de 43 aptos. Nominal 13: 8. Nominal 22: 2. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- ANCARA (29297), zona 1, seção 495. Urna `o03220zz2929700010495`. Assinatura fechou. Comparecimento 37 de 77 aptos. Nominal 13: 24. Nominal 22: 7. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- ARGEL (29300), zona 1, seção 6. Urna `o03220zz2930000010006`. Assinatura fechou. Comparecimento 31 de 48 aptos. Nominal 13: 27. Nominal 22: 3. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- BISSAU (29394), zona 1, seção 28. Urna `o03220zz2939400010028`. Assinatura fechou. Comparecimento 37 de 88 aptos. Nominal 13: 17. Nominal 22: 17. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- CIUDAD GUAYANA (29564), zona 1, seção 91. Urna `o03220zz2956400010091`. Assinatura fechou. Comparecimento 0 de 72 aptos.
- CONCEPCIÓN (29580), zona 1, seção 96. Urna `o03220zz2958000010096`. Assinatura fechou. Comparecimento 36 de 78 aptos. Nominal 13: 2. Nominal 22: 32. Branco: 1. Nulo: 0. BU e RDV com os mesmos totais.
- DÍLI (29645), zona 1, seção 380. Urna `o03220zz2964500010380`. Assinatura fechou. Comparecimento 47 de 89 aptos. Nominal 13: 16. Nominal 22: 27. Branco: 1. Nulo: 0. BU e RDV com os mesmos totais.
- HANÓI (29750), zona 1, seção 1703. Urna `o03220zz2975000011703`. Assinatura fechou. Comparecimento 32 de 82 aptos. Nominal 13: 13. Nominal 22: 14. Branco: 1. Nulo: 2. BU e RDV com os mesmos totais.
- HAVANA (29777), zona 1, seção 127. Urna `o03220zz2977700010127`. Assinatura fechou. Comparecimento 40 de 92 aptos. Nominal 13: 36. Nominal 22: 1. Branco: 1. Nulo: 1. BU e RDV com os mesmos totais.
- KIEV (29858), zona 1, seção 1183. Urna `o03220zz2985800011183`. Assinatura fechou. Comparecimento 23 de 65 aptos. Nominal 13: 4. Nominal 22: 19. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- LAGOS (29912), zona 1, seção 150. Urna `o03220zz2991200010150`. Assinatura fechou. Comparecimento 33 de 82 aptos. Nominal 13: 26. Nominal 22: 6. Branco: 1. Nulo: 0. BU e RDV com os mesmos totais.
- MOSCOU (30163), zona 1, seção 647. Urna `o03220zz3016300010647`. Assinatura fechou. Comparecimento 85 de 252 aptos. Nominal 13: 49. Nominal 22: 25. Branco: 0. Nulo: 4. BU e RDV com os mesmos totais.
- MUMBAI (30171), zona 1, seção 1340. Urna `o03220zz3017100011340`. Assinatura fechou. Comparecimento 11 de 55 aptos. Nominal 13: 5. Nominal 22: 1. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- PASO LOS LIBRES (30295), zona 1, seção 348. Urna `o03220zz3029500010348`. Assinatura fechou. Comparecimento 5 de 41 aptos. Nominal 13: 2. Nominal 22: 3. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- PORT OF SPAIN (30325), zona 1, seção 352. Urna `o03220zz3032500010352`. Assinatura fechou. Comparecimento 19 de 87 aptos. Nominal 13: 4. Nominal 22: 10. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- PORTO PRÍNCIPE (30333), zona 1, seção 353. Urna `o03220zz3033300010353`. Assinatura fechou. Comparecimento 5 de 33 aptos. Nominal 13: 5. Nominal 22: 0. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- RIO BRANCO (30430), zona 1, seção 384. Urna `o03220zz3043000010384`. Assinatura fechou. Comparecimento 23 de 58 aptos. Nominal 13: 7. Nominal 22: 9. Branco: 2. Nulo: 0. BU e RDV com os mesmos totais.
- SÓFIA (30546), zona 1, seção 1764. Urna `o03220zz3054600011764`. Assinatura fechou. Comparecimento 49 de 98 aptos. Nominal 13: 34. Nominal 22: 8. Branco: 0. Nulo: 2. BU e RDV com os mesmos totais.
- TEERÃ (30597), zona 1, seção 1182. Urna `o03220zz3059700011182`. Assinatura fechou. Comparecimento 25 de 45 aptos. Nominal 13: 14. Nominal 22: 11. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- TRÍPOLI (30686), zona 1, seção 443. Urna `o03220zz3068600010443`. Assinatura fechou. Comparecimento 2 de 30 aptos. Nominal 13: 2. Nominal 22: 0. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- TUNIS (30708), zona 1, seção 444. Urna `o03220zz3070800010444`. Assinatura fechou. Comparecimento 22 de 47 aptos. Nominal 13: 12. Nominal 22: 9. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- WINDHOEK (30821), zona 1, seção 1524. Urna `o03220zz3082100011524`. Assinatura fechou. Comparecimento 13 de 37 aptos. Nominal 13: 6. Nominal 22: 5. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- DAR ES SALAAM (38962), zona 1, seção 558. Urna `o03220zz3896200010558`. Assinatura fechou. Comparecimento 16 de 34 aptos. Nominal 13: 11. Nominal 22: 5. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- MASCATE (39102), zona 1, seção 712. Urna `o03220zz3910200010712`. Assinatura fechou. Comparecimento 38 de 97 aptos. Nominal 13: 12. Nominal 22: 20. Branco: 1. Nulo: 1. BU e RDV com os mesmos totais.
- PUERTO IGUAZÚ (99155), zona 1, seção 1504. Urna `o03220zz9915500011504`. Assinatura fechou. Comparecimento 22 de 62 aptos. Nominal 13: 7. Nominal 22: 15. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- NASSAU (99180), zona 1, seção 1228. Urna `o03220zz9918000011228`. Assinatura fechou. Comparecimento 19 de 69 aptos. Nominal 13: 6. Nominal 22: 10. Branco: 0. Nulo: 0. BU e RDV com os mesmos totais.
- BAREIN (99473), zona 1, seção 1327. Urna `o03220zz9947300011327`. Assinatura fechou. Comparecimento 49 de 69 aptos. Nominal 13: 17. Nominal 22: 27. Branco: 0. Nulo: 2. BU e RDV com os mesmos totais.

## Arquivos

- `verificar_vsc_ZZ_1t.parquet`
- `verificar_vsc_ZZ_1t.csv`
