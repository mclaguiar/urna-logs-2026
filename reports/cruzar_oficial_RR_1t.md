# Cruzamento oficial — presidente — RR 1º turno

Camada: **BU (audit)** × **CSV oficial** (`votacao_secao_*_BR`, cargo presidente).

## Resumo

- Seções: **1,519** · OK: **1,519** · divergentes: **0**
- Linhas (seção × votável): **10,588** · OK: **10,588** · divergentes: **0**
- Votos BU: **332,772** · oficial: **332,772**
- Só na audit: **0** · só no oficial: **0**

## Divergências

Nenhuma divergência encontrada.

## Método

- Chave: `join_key` = UF:municipio:zona:secao
- Votável: número do candidato; branco=`95`; nulo=`96` (padrão TSE)
- Fonte oficial: [Resultados 2026 — presidente por seção](https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip)
