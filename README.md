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
| Consolidado nacional / anomalias | Em andamento (audit nacional) |
| Cruzar totais × resultado oficial divulgado | Planejado (`audit` + CSV Resultados 2026) |
| Distribuição horária / impacto pós-17h | Planejado (log → Parquet hora × UF) |

## O que conseguimos auditar (e o que não)

Trabalhamos só com **arquivos públicos** do TSE. A ideia é encadear três camadas e ver se batem.

```text
Urna (RDV)  →  BU da urna  →  totalização divulgada (CSV aberto)
     ↑ recontar              ↑ cruzar seção a seção / UF
```

| Conseguimos | Como |
|---|---|
| Recontar votos de **presidente** urna a urna | Somar o RDV e comparar com o BU |
| Conferir aptos, comparecimento, abstenção, brancos/nulos da urna | Campos do BU |
| % habilitação **sem digital** (bio / biografia / sem biometria) | Detalhe do BU (faltando no exterior ZZ) |
| Totais por município / UF | Agregar os Parquets da `audit` |
| Cruzar com o **resultado oficial divulgado** | CSV “votação por seção” / mun-zona dos [Resultados 2026](https://dadosabertos.tse.jus.br/dataset/resultados-2026) × nosso Parquet (`join_key`) |
| Comparar 1º × 2º turno **por seção** (abstenção, mudança de totais) | Quando o 2º turno estiver publicado |
| Distribuição **hora a hora** das habilitações (por UF / município) | Timestamps do log (`Eleitor foi habilitado`); hora local da UF |
| Estimar impacto da **ampliação após 17h** | Contar habilitações ≥17h (e faixas 17–18h, 18–19h…) vs total da seção/UF |
| Ver se o pacote da urna foi adulterado depois (hashes/assinatura `.vsc`) | Planejado |

| Não conseguimos | Por quê |
|---|---|
| Saber *quem* votou em quem / migrou entre turnos | Sigilo do voto; RDV sem identificação do eleitor |
| Provar que o **hardware** da urna não foi comprometido antes de gravar o RDV | Exigiria cadeia de certificação / inspeção além dos arquivos abertos |
| Garantir que a mídia de resultado é a única cópia “verdadeira” do que saiu da urna | Só vemos o que foi **transmitido e publicado** |
| Auditar outros cargos neste pipeline (ainda) | Foco deliberado em presidente; o schema ASN.1 já permitiria expandir |
| Detectar fraude só pelo fato de RDV ≡ BU ≡ CSV oficial | Se as três camadas forem alteradas de forma coerente, o cruzamento **bate** e não acusa divergência |

Em resumo: auditar aqui = **consistência da cadeia pública** (RDV ↔ BU ↔ divulgação). Divergência é achado forte; concordância total **não** prova ausência de problema antes da publicação.

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
- **Horário da votação** (planejado): distribuição hora a hora por UF e peso do fluxo após 17h

## Requisitos

- Python 3.12+ (também testado com 3.15)
- Disco: ~250 GB livres se for baixar o 1º turno do país (≈ **95 GB** de ZIPs + folga)

## Setup

```bash
git clone https://github.com/mclaguiar/urna-logs-2026.git
cd urna-logs-2026
python3 -m venv .venv          # macOS / Linux
# Windows (use o launcher para não pegar o Python 3.10 da Store):
#   py -3.12 -m venv .venv
#   ou: py -3.15 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"
urna-logs --help
```

**Windows — se `urna-logs` quebrar com erro de NumPy / `cp315` vs Python 3.10:** o `.venv` misturou o interpretador da Microsoft Store com pacotes de outra versão. Recrie com o launcher explícito:

```powershell
Remove-Item -Recurse -Force .venv
py -3.15 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

Confira: `python --version` dentro do venv deve ser 3.12+ (o mesmo que você usou no `py -3.xx -m venv`).

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
- [ ] Fechar `audit` nacional 1º turno (todas as UFs)
- [ ] Incorporar na auditoria o cruzamento com o **resultado oficial** (votação por seção / mun-zona)
- [ ] Testar 2º turno assim que existir `…_2t_*.zip`

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

### Horário da votação e ampliação após 17h
Fonte: log da urna (horário de cada `Eleitor foi habilitado`). O BU só traz abertura/encerramento da seção; o RDV não tem hora por voto.

Objetivo: medir **quanto o fluxo depois das 17h** (fila / eventual ampliação do horário) pesou no comparecimento — por UF, município e seção — e se há padrões atípicos.

- [ ] Gerar Parquet de habilitações com `dt` + hora local da UF (respeitar fuso: AC −5, RR/AM −4, etc.)
- [ ] Comando/relatório: distribuição **hora a hora por UF** (% e contagem)
- [ ] Indicadores: % habilitações ≥17h; faixas 17–18h, 18h+; seções com encerramento tardio
- [ ] Cruzar seções com alto % pós-17h × resultado presidente / abstenção (só agregado)
- [ ] Comparar 1º × 2º turno no mesmo recorte horário (quando o 2º existir)

**Limite:** horário = momento da **habilitação**, não do voto em cada cargo; não dá para saber em quem votou quem chegou depois das 17h.

### Médio prazo
- [x] Site Quarto + GitHub Pages (piloto % sem digital por UF)
- [ ] Mais páginas: horário / pós-17h, municípios, cruzamento com oficial
- [ ] Alertas de anomalia: seções fora do padrão (% sem digital, pós-17h, comparecimento, mudança extrema 1º→2º)
- [ ] Cruzar log × BU (habilitações do log vs comparecimento)
- [ ] Validar assinaturas / hashes (`.vsc`) — integridade do pacote

### Fora de escopo (por enquanto)
- Recontagem de outros cargos (deputado, governador, …) — o schema já permite; o foco agora é presidente
- Seguir eleitor individual entre turnos (impossível com os arquivos públicos)
- Provar que o hardware da urna está correto
- Afirmar “eleição íntegra” só porque RDV, BU e CSV oficial coincidem

## Site (Quarto → GitHub Pages)

Gráficos públicos a partir de agregados leves (sem subir os ZIPs).

```bash
# Atualiza CSV do site com base nos reports/by_municipio_*.csv
python scripts/build_site_data.py

# Render local (requer Quarto: https://quarto.org)
quarto render site
```

- Fonte do site: `site/` (`index.qmd`, análises, `data/resumo_uf_1t.csv`)
- CI: `.github/workflows/quarto-publish.yml` → branch `gh-pages`
- URL esperada: `https://mclaguiar.github.io/urna-logs-2026/`

No GitHub: **Settings → Pages** com source = branch `gh-pages` (após o primeiro publish). Em **Settings → Actions → General**, permitir write para o workflow (`GITHUB_TOKEN`).

## Fontes

- [Arquivos transmitidos para totalização 2026](https://dadosabertos.tse.jus.br/dataset/resultados-2026-arquivos-transmitidos-para-totalizacao) — BU, RDV, log, assinatura (por UF)
- [Resultados 2026](https://dadosabertos.tse.jus.br/dataset/resultados-2026) — votação oficial por seção / município-zona (para cruzar com a `audit`)
- Schemas ASN.1 BU/RDV 2026 (em `src/urna_logs/spec/`)
