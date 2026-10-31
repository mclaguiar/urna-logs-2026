# Cruzamento oficial — presidente — RO 1º turno

Camada: **BU (audit)** × **CSV oficial** (`votacao_secao_*_BR`, cargo presidente).

## Resumo

- Seções: **4,698** · OK: **4,698** · divergentes: **0**
- Linhas (seção × votável): **33,649** · OK: **33,649** · divergentes: **0**
- Votos BU: **991,080** · oficial: **991,080**
- Só na audit: **0** · só no oficial: **0**

## Divergências

Nenhuma divergência entre totais do **BU** (audit) e o **CSV oficial** de votação por seção: as **camadas públicas batem** nesta chave (seção × votável). Os totais são agregados por seção.

## Método

- Chave: `join_key` = UF:municipio:zona:secao
- Votável: número do candidato; branco=`95`; nulo=`96` (padrão TSE)
- Fonte oficial: [Resultados 2026 — presidente por seção](https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip)
- Sem divergência = **consistência entre arquivos públicos** (BU ≡ CSV) na chave seção × votável
