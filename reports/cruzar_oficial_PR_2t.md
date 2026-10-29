# Cruzamento oficial — presidente — PR 2º turno

Camada: **BU (audit)** × **CSV oficial** (`votacao_secao_*_BR`, cargo presidente).

## Resumo

- Seções: **27,142** · OK: **27,142** · divergentes: **0**
- Linhas (seção × votável): **105,761** · OK: **105,761** · divergentes: **0**
- Votos BU: **7,059,339** · oficial: **7,059,339**
- Só na audit: **0** · só no oficial: **0**

## Divergências

Nenhuma divergência entre totais do **BU** (audit) e o **CSV oficial** de votação por seção. Isso indica apenas que os **arquivos disponibilizados pelo TSE estão consistentes entre si** nessa chave (seção × votável) — não prova ausência de anomalia operacional nem “migração” eleitor a eleitor.

## Método

- Chave: `join_key` = UF:municipio:zona:secao
- Votável: número do candidato; branco=`95`; nulo=`96` (padrão TSE)
- Fonte oficial: [Resultados 2026 — presidente por seção](https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip)
- Sem divergência = **consistência entre arquivos públicos** (BU ≡ CSV), não prova ausência de anomalia operacional
