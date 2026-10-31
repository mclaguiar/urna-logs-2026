# Verificar `.vsc` — ES 2º turno

Nível solicitado: **níveis 1+2** (omitir = hashes e Ed521; 1 = só hashes; 2 = só Ed521).

## Resumo

- Stems no ZIP: **9,844**
- Com `-vota.vsc`: **9,844**
- Nível ≥1 (auto-hash + hashes dos arquivos presentes + críticos): **9,844**
- Nível 2 (Ed521: certificado + auto + hashes): **7,362**
- Assinatura HW falhou: **2,482**
- Críticos (bu/rdv/log) OK: **9,844**
- Algum hash presente falhou: **0**

Arquivos listados na assinatura mas **ausentes** no ZIP público (jufa, wsq*, mr.ver, …) contam como `ausente_pacote` — esperado no CDN.

## Método

- Spec ASN.1: `urna_logs/spec/assinatura.asn1` (TSE 2026)
- Hash: SHA-512 do conteúdo = campo `AssinaturaDigital.hash`
- Nível 2: Ed521 sobre SHA-512 desse hash, com a chave do certificado embutido; o certificado é conferido com a AC UE2020 ou UE2022. Não valida a chave de software da cerimônia.

## Falhas / pendências (até 40)

- `o03221es5605700120001` jk=`ES:56057:0012:0001` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120002` jk=`ES:56057:0012:0002` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120003` jk=`ES:56057:0012:0003` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120004` jk=`ES:56057:0012:0004` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120005` jk=`ES:56057:0012:0005` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120006` jk=`ES:56057:0012:0006` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120007` jk=`ES:56057:0012:0007` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120008` jk=`ES:56057:0012:0008` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120009` jk=`ES:56057:0012:0009` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120010` jk=`ES:56057:0012:0010` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120011` jk=`ES:56057:0012:0011` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120012` jk=`ES:56057:0012:0012` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120013` jk=`ES:56057:0012:0013` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120014` jk=`ES:56057:0012:0014` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120015` jk=`ES:56057:0012:0015` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120016` jk=`ES:56057:0012:0016` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120017` jk=`ES:56057:0012:0017` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120018` jk=`ES:56057:0012:0018` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120019` jk=`ES:56057:0012:0019` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120020` jk=`ES:56057:0012:0020` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120021` jk=`ES:56057:0012:0021` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120022` jk=`ES:56057:0012:0022` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120023` jk=`ES:56057:0012:0023` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120024` jk=`ES:56057:0012:0024` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120025` jk=`ES:56057:0012:0025` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120026` jk=`ES:56057:0012:0026` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120027` jk=`ES:56057:0012:0027` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120028` jk=`ES:56057:0012:0028` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120029` jk=`ES:56057:0012:0029` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120030` jk=`ES:56057:0012:0030` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120031` jk=`ES:56057:0012:0031` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120032` jk=`ES:56057:0012:0032` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120033` jk=`ES:56057:0012:0033` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120034` jk=`ES:56057:0012:0034` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120035` jk=`ES:56057:0012:0035` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120037` jk=`ES:56057:0012:0037` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120038` jk=`ES:56057:0012:0038` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120039` jk=`ES:56057:0012:0039` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120040` jk=`ES:56057:0012:0040` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`
- `o03221es5605700120041` jk=`ES:56057:0012:0041` nivel_ok=1 erro=`algoritmo do certificado não é Ed521 (1.2.840.10045.2.1)` criticos=`bu.dat=ok;rdv.dat=ok;log.jez=ok`

## Arquivos

- `verificar_vsc_ES_2t.parquet`
- `verificar_vsc_ES_2t.csv`
