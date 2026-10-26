# Cruzamento oficial — presidente — SC 1º turno

Camada: **BU (audit)** × **CSV oficial** (`votacao_secao_*_BR`, cargo presidente).

## Resumo

- Seções: **17,326** · OK: **17,326** · divergentes: **0**
- Linhas (seção × votável): **136,979** · OK: **136,979** · divergentes: **0**
- Votos BU: **4,648,159** · oficial: **4,648,159**
- Só na audit: **0** · só no oficial: **0**

## Divergências

Nenhuma divergência encontrada.

## Método

- Chave: `join_key` = UF:municipio:zona:secao
- Votável: número do candidato; branco=`95`; nulo=`96` (padrão TSE)
- Fonte oficial: [Resultados 2026 — presidente por seção](https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip)
