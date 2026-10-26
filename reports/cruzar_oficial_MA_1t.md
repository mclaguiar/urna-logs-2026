# Cruzamento oficial — presidente — MA 1º turno

Camada: **BU (audit)** × **CSV oficial** (`votacao_secao_*_BR`, cargo presidente).

## Resumo

- Seções: **18,093** · OK: **18,092** · divergentes: **1**
- Linhas (seção × votável): **124,673** · OK: **124,667** · divergentes: **6**
- Votos BU: **4,160,124** · oficial: **4,160,343**
- Só na audit: **0** · só no oficial: **6**

## Divergências

6 linha(s) com diferença (até 40):

| join_key | votável | BU | oficial | diff | lado |
|---|---:|---:|---:|---:|---|
| `MA:07846:0074:0228` | 13 | 0 | 158 | -158 | só_oficial |
| `MA:07846:0074:0228` | 14 | 0 | 1 | -1 | só_oficial |
| `MA:07846:0074:0228` | 22 | 0 | 52 | -52 | só_oficial |
| `MA:07846:0074:0228` | 70 | 0 | 2 | -2 | só_oficial |
| `MA:07846:0074:0228` | 95 | 0 | 2 | -2 | só_oficial |
| `MA:07846:0074:0228` | 96 | 0 | 4 | -4 | só_oficial |

## Método

- Chave: `join_key` = UF:municipio:zona:secao
- Votável: número do candidato; branco=`95`; nulo=`96` (padrão TSE)
- Fonte oficial: [Resultados 2026 — presidente por seção](https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip)
