# Cruzamento oficial — presidente — PE 1º turno

Camada: **BU (audit)** × **CSV oficial** (`votacao_secao_*_BR`, cargo presidente).

## Resumo

- Seções: **21,418** · OK: **21,418** · divergentes: **0**
- Linhas (seção × votável): **156,699** · OK: **156,699** · divergentes: **0**
- Votos BU: **5,911,062** · oficial: **5,911,062**
- Só na audit: **0** · só no oficial: **0**

## Divergências

Nenhuma divergência encontrada.

## Método

- Chave: `join_key` = UF:municipio:zona:secao
- Votável: número do candidato; branco=`95`; nulo=`96` (padrão TSE)
- Fonte oficial: [Resultados 2026 — presidente por seção](https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip)
