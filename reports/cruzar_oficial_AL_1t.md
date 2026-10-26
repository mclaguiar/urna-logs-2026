# Cruzamento oficial — presidente — AL 1º turno

Camada: **BU (audit)** × **CSV oficial** (`votacao_secao_*_BR`, cargo presidente).

## Resumo

- Seções: **7,101** · OK: **7,101** · divergentes: **0**
- Linhas (seção × votável): **50,972** · OK: **50,972** · divergentes: **0**
- Votos BU: **1,938,428** · oficial: **1,938,428**
- Só na audit: **0** · só no oficial: **0**

## Divergências

Nenhuma divergência encontrada.

## Método

- Chave: `join_key` = UF:municipio:zona:secao
- Votável: número do candidato; branco=`95`; nulo=`96` (padrão TSE)
- Fonte oficial: [Resultados 2026 — presidente por seção](https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip)
