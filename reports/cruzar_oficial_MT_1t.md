# Cruzamento oficial — presidente — MT 1º turno

Camada: **BU (audit)** × **CSV oficial** (`votacao_secao_*_BR`, cargo presidente).

## Resumo

- Seções: **8,287** · OK: **8,287** · divergentes: **0**
- Linhas (seção × votável): **60,750** · OK: **60,750** · divergentes: **0**
- Votos BU: **2,052,133** · oficial: **2,052,133**
- Só na audit: **0** · só no oficial: **0**

## Divergências

Nenhuma divergência entre totais do **BU** (audit) e o **CSV oficial** de votação por seção. Isso indica apenas que os **arquivos disponibilizados pelo TSE estão consistentes entre si** nessa chave (seção × votável) — não prova ausência de anomalia operacional nem migração eleitor a eleitor.

## Método

- Chave: `join_key` = UF:municipio:zona:secao
- Votável: número do candidato; branco=`95`; nulo=`96` (padrão TSE)
- Fonte oficial: [Resultados 2026 — presidente por seção](https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip)
