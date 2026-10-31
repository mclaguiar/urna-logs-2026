# Cruzamento oficial — presidente — GO 2º turno

Camada: **BU (audit)** × **CSV oficial** (`votacao_secao_*_BR`, cargo presidente).

## Resumo

- Seções: **15,686** · OK: **15,686** · divergentes: **0**
- Linhas (seção × votável): **61,031** · OK: **61,031** · divergentes: **0**
- Votos BU: **4,047,280** · oficial: **4,047,280**
- Só na audit: **0** · só no oficial: **0**

## Divergências

Nenhuma divergência entre totais do **BU** (audit) e o **CSV oficial** de votação por seção: as **camadas públicas batem** nesta chave (seção × votável). Os totais são agregados por seção.

## Método

- Chave: `join_key` = UF:municipio:zona:secao
- Votável: número do candidato; branco=`95`; nulo=`96` (padrão TSE)
- Fonte oficial: [Resultados 2026 — presidente por seção](https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip)
- Sem divergência = **consistência entre arquivos públicos** (BU ≡ CSV) na chave seção × votável
