# urna-logs-2026

Auditoria independente dos arquivos transmitidos para totalização (TSE) — Eleições 2026.

Foco atual: **cargo presidente** (recontar RDV e comparar com o BU) e **habilitação sem digital** (detalhe do BU, por UF e município).

## Status (piloto)

| Etapa | Situação |
|---|---|
| Download com retomada (1º turno) | OK — URL `…_1t_{UF}.zip` |
| Download 2º turno | Ainda não publicado no CDN (`…_2t_…` → 404) |
| Leitura ASN.1 do BU/RDV (schemas TSE 2026) | OK |
| `audit` presidente urna a urna | OK — AC, RR, AP, ZZ: **7.013/7.013** RDV ≡ BU |
| `by-municipio` (votos + % sem digital) | OK — nomes pelo perfil do eleitorado TSE |
| Métricas do log (biometria / após 17h) | OK no AC (fase de viabilidade) |
| Consolidado nacional / anomalias | Planejado |

## O que entra na auditoria (e o que não)

**Entra:** o que está nos pacotes abertos do TSE depois da urna — recontar os votos do RDV, confrontar com o BU, cruzar habilitação biométrica e local (UF, município, zona, seção).

**Não entra:** o que aconteceu dentro do hardware antes de gravar o RDV (isso pediria checagem de assinatura de hardware / certificação).

## Formato dos dados (para montar vários recortes depois)

**Parquet** é o formato principal para análise: dá para filtrar e agregar depois por UF, município, zona, horário, candidato etc.

| Camada | Formato | Uso |
|---|---|---|
| Arquivo bruto do TSE | ZIP (`data/raw/`) | Fonte original; download retomável |
| Detalhe (1 linha por seção / por voto) | **Parquet** | Base para cruzamentos e totais |
| Relatório para leitura | Markdown + CSV curto | Texto e planilha rápida |
| Tabela auxiliar | CSV em `data/ref/` | Nome do município (código TSE) |

Por que Parquet: tipado, compacto, lê só as colunas necessárias; vai bem com pandas, polars ou DuckDB. CSV fica para exportação leve.

O `audit` grava **Parquet por seção** + **Parquet de votos** (uma linha por candidato/tipo na seção) e um CSV simples. Várias UFs juntas: `audit_presidente_MULTI_{t}t.parquet`. Chave entre turnos: `join_key = UF:municipio:zona:secao`.

## Análises

- Recontagem **presidente**: cada voto do RDV × totais do BU (por urna)
- Habilitação **sem digital** (BU): `bio` + `biografia` + `sem_biometria`  
  - *sem digital* = biografia + sem_biometria  
  - No exterior (ZZ) o BU em geral **não traz** esse detalhe
- Totais por **município** (código TSE + nome)
- Viabilidade pelo log: catálogo de mensagens, biometria no log, eventos após 17h

## Requisitos

- Python 3.12+ (também testado com 3.15)
- Disco: ~250 GB livres se for baixar o 1º turno do país (≈ **95 GB** de ZIPs + folga)

## Setup

```bash
git clone https://github.com/mclaguiar/urna-logs-2026.git
cd urna-logs-2026
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -e ".[dev]"
```

## Uso

```bash
# Download com retomada (UF pequena)
urna-logs download --ufs AC --turno 1

# Várias UFs / país inteiro (1º turno ≈ 95 GB)
urna-logs download --ufs "AC RR AP ZZ" --turno 1
urna-logs download --ufs ALL --turno 1

# Viabilidade (log): catálogo + métricas de biometria / após 17h
urna-logs viability --ufs AC --turno 1

# Auditoria presidente (RDV × BU) — use -v para listar divergências na hora
urna-logs audit --ufs "AC RR AP ZZ" --turno 1
urna-logs audit --ufs AC --turno 1 -v

# Por município (usa o CSV da audit + nomes do TSE)
urna-logs by-municipio --ufs "AC RR AP ZZ" --turno 1
```

O download e o `audit` mostram progresso por padrão (UF atual, tamanho, barra OK/falha).

## Arquivos gerados

| Caminho | Conteúdo |
|---|---|
| `data/raw/*.zip` | ZIPs do TSE (não versionados) |
| `data/raw/download_state.json` | Estado do download (para retomar) |
| `data/ref/municipios_tse.csv` | Cache código → nome do município |
| `reports/catalog_*_Nt.json` | Catálogo de mensagens do log |
| `reports/metrics_*_Nt.parquet` | Uma linha por habilitação (log) |
| `reports/metrics_summary_*_Nt.csv` | Resumo do log (% sem digital, % após 17h) |
| `reports/viability_*_Nt.md` | Parecer go/no-go (log) |
| `reports/audit_presidente_*_Nt.md` | Recontagem presidente RDV × BU |
| `reports/audit_presidente_*_Nt.csv` | Seções (para abrir no Excel) |
| `reports/audit_presidente_*_Nt.parquet` | Seções: aptos, comparecimento, abstenção, bio, `join_key` |
| `reports/audit_presidente_votos_*_Nt.parquet` | Votos detalhados: seção × tipo × número |
| `reports/audit_presidente_MULTI_*t.parquet` | Várias UFs juntas (seções + votos) |
| `reports/by_municipio_*_Nt.md` | Ranking por município (% sem digital, votos) |
| `reports/by_municipio_*_Nt.csv` | Totais por município |
| `src/urna_logs/spec/*.asn1` | Schemas oficiais BU/RDV 2026 |

## Ordem sugerida

1. `download` de UFs pequenas (AC → RR AP ZZ)
2. `audit` nessas UFs (conferir se RDV ≡ BU)
3. `by-municipio` (totais e % sem digital por cidade)
4. Ampliar para outras UFs / `ALL` no 1º turno
5. Quando o CDN publicar o 2º turno: `audit --turno 2` nas mesmas UFs
6. Comparar **seção a seção** 1º × 2º (abstenção, mudança de votos, etc.)
7. Unificar Parquets e caçar anomalias

## Plano

### Curto prazo
- [x] Gravar `audit` em **Parquet** (seções + votos + várias UFs juntas)
- [ ] Ampliar 1º turno (ondas: pequenas → médias → SP/MG/…)
- [ ] Testar 2º turno assim que existir `…_2t_*.zip`
- [ ] Conferir totais de presidente com o resultado oficial divulgado

### Comparativo 1º × 2º turno (seção a seção)
Chave de junção: `join_key` = `UF:municipio:zona:secao` (sem o local — ele pode mudar em contingência).

**Dá para medir (só no total da seção — não eleitor a eleitor):**
- [ ] Aptos, comparecimento e **abstenção** 1º vs 2º (diferença e %)
- [ ] Votos nos finalistas no 2º vs o que a seção tinha no 1º
- [ ] Mudança da margem na seção entre os dois finalistas
- [ ] Saldo aparente dos votos de quem ficou de fora no 1º (só como total da seção)
- [ ] Brancos/nulos 1º→2º; seções que aparecem ou somem (contingência, ZZ, etc.)

**Não dá (sigilo do voto):** saber *quem* mudou de um candidato para outro. O RDV não identifica eleitor entre turnos. Qualquer “migração” é só estimativa pelo total da seção.

Antes disso: Parquet de seção nos dois turnos + 2º turno publicado.

### Médio prazo
- [ ] Alertas de anomalia: seções fora do padrão (% sem digital, após 17h, comparecimento, mudança extrema 1º→2º)
- [ ] Cruzar log × BU (habilitações do log vs comparecimento)
- [ ] Validar assinaturas / hashes (`.vsc`) — integridade do pacote
- [ ] Dashboard ou notebook em cima do Parquet unificado

### Fora de escopo (por enquanto)
- Recontagem de outros cargos (deputado, governador, …) — o schema já permite; o foco agora é presidente
- Seguir eleitor individual entre turnos (impossível com os arquivos públicos)
- Provar que o hardware da urna está correto

## Fonte

- [Arquivos transmitidos para totalização 2026](https://dadosabertos.tse.jus.br/dataset/resultados-2026-arquivos-transmitidos-para-totalizacao)
- Schemas ASN.1 BU/RDV 2026 (em `src/urna_logs/spec/`)
