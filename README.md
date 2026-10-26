# urna-logs-2026

Auditoria independente dos arquivos transmitidos para totalização (TSE) — Eleições 2026.

**Duas análises principais** (cargo presidente):

1. **Seção a seção, 1º × 2º** — o que mudou nos votos/abstenção e **de onde veio a diferença** (saldo agregado da seção; não “quem migrou”).
2. **Impacto do horário** — curva de habilitações e peso do fluxo **após 17h** (Brasília; ZZ = local), cruzado com resultado e comparecimento.

O resto do pipeline (RDV≡BU, CSV oficial, % sem digital) é **base e cruzamento de risco** para essas duas leituras.

## Status (piloto)

| Etapa | Situação |
|---|---|
| Download com retomada (1º turno) | OK — URL `…_1t_{UF}.zip` |
| Download 2º turno | Ainda não publicado (`…_2t_…` → 404). **Monitorar:** [arquivos transmitidos para totalização 2026](https://dadosabertos.tse.jus.br/dataset/resultados-2026-arquivos-transmitidos-para-totalizacao) |
| Leitura ASN.1 do BU/RDV (schemas TSE 2026) | OK |
| `audit` presidente urna a urna | OK — AC, RR, AP, ZZ: **7.013/7.013** RDV ≡ BU |
| `by-municipio` (votos + % sem digital) | OK — nomes pelo perfil do eleitorado TSE |
| Métricas do log (biometria / após 17h) | OK no AC (fase de viabilidade) |
| Consolidado nacional / anomalias | Em andamento (audit nacional) |
| Cruzar totais × resultado oficial divulgado | OK — `cruzar-oficial` (BU × `votacao_secao_*_BR`) |
| Distribuição horária / impacto pós-17h | OK no piloto (`horario`); curva por hora + esqueleto 1º×2º |

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

## Glossário

| Termo | Significado |
|---|---|
| **TSE** | Tribunal Superior Eleitoral — publica os arquivos abertos que auditamos |
| **UF** | Unidade da Federação (`AC`…`TO`); `ZZ` = zonas no exterior |
| **Seção** | Unidade de votação (urna/local) identificada por município + zona + seção |
| **Zona** | Circunscrição eleitoral dentro do município (ou agrupamento no exterior) |
| **BU** | Boletim de Urna — totais oficiais daquela urna (aptos, comparecimento, votos por candidato/branco/nulo, detalhe biométrico quando houver) |
| **RDV** | Registro Digital do Voto — sequência dos votos da urna **sem** identificar o eleitor; usamos para **recontar** e comparar com o BU |
| **Log / logjez** | Registro de eventos da urna (abertura, habilitação, etc.); fonte do horário e do tipo de habilitação |
| **Habilitação** | Momento em que o eleitor é liberado para votar na urna (`Eleitor foi habilitado` no log) |
| **Biometria / bio** | Habilitação com reconhecimento da digital do eleitor |
| **Biografia** | Habilitação por ano de nascimento (sem digital), quando o cadastro permite |
| **Sem biometria** | Eleitor sem biometria cadastrada |
| **Sem digital (BU)** | Canônico: **biografia + sem biometria** no BU (painel / `by-municipio`) |
| **Sem digital (log)** | Proxy: `sem_biometria` + `manual_falha` no log (`metrics` / `viability`) — não comparar direto com o % do BU |
| **Pós-17h** | ≥ 17:00 no **horário de Brasília** (ZZ = local do posto); helper `urna_logs.fuso` |
| **Comparecimento** | Quantidade de eleitores que votaram na seção (no BU) |
| **Aptos** | Eleitores aptos a votar na seção |
| **Abstenção** | Aptos − comparecimento |
| **Votável** | Código do candidato no CSV oficial; branco=`95`, nulo=`96` (padrão TSE) |
| **CSV oficial** | Resultado divulgado nos [dados abertos](https://dadosabertos.tse.jus.br/dataset/resultados-2026) (ex.: `votacao_secao_*_BR` para presidente) |
| **`join_key`** | Chave estável `UF:municipio:zona:secao` para cruzar 1º×2º turno e BU×oficial (sem o “local”, que pode mudar em contingência) |
| **Stem** | Prefixo do arquivo da urna no ZIP (ex.: `o03220ac0100700090001`) — de onde extraímos município/zona/seção |
| **ASN.1** | Formato binário dos arquivos `.bu` / `.rdv`; schemas oficiais em `src/urna_logs/spec/` |
| **Parquet** | Formato colunar dos nossos detalhes (seções, votos, horário) — base para análise |
| **`.vsc`** | Assinatura/integridade do pacote da urna (validação planejada) |
| **1º / 2º turno** | Arquivos `…_1t_{UF}.zip` e `…_2t_{UF}.zip` no CDN; o 2º só entra quando publicado |

Glossário completo também em [site/metodo.qmd](site/metodo.qmd) (painel Quarto).

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

# Cruzar BU × resultado oficial (CSV TSE presidente por seção)
urna-logs cruzar-oficial --ufs "AC RR AP ZZ" --turno 1
urna-logs cruzar-oficial --ufs ALL --turno 1

# Curva horária das habilitações (log) + % pós-17h
# Padrão = modo rápido (só agregados). --detalhe grava Parquet 1 linha/hab.
urna-logs horario --ufs ALL --turno 1
urna-logs horario --ufs AC --turno 1 --detalhe   # cruzamento fino por seção

# Esqueleto 1º × 2º (preenche quando existir audit do 2º)
urna-logs comparar-turnos --ufs "AC RR AP ZZ"
```

O download e o `audit` mostram progresso por padrão (UF atual, tamanho, barra OK/falha).
O `cruzar-oficial` baixa uma vez o ZIP nacional (~160 MB) em `data/ref/` e cacheia Parquet por UF.

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
| `data/ref/votacao_secao_*_BR.zip` | CSV oficial presidente × seção (cache) |
| `data/ref/oficial_presidente_votos_*_Nt.parquet` | Oficial filtrado por UF |
| `reports/cruzar_oficial_*_Nt.md` | BU × oficial (seções / votáveis) |
| `reports/cruzar_oficial_*_Nt.parquet` | Detalhe do cruzamento |
| `src/urna_logs/spec/*.asn1` | Schemas oficiais BU/RDV 2026 |

## Passo a passo

Cadeia auditada: **RDV → BU → CSV oficial** (`join_key` = `UF:municipio:zona:secao`).

| # | Comando | O que faz |
|---|---|---|
| 1 | `urna-logs download --ufs AC --turno 1` | Baixa o ZIP da UF (retomável). País: `--ufs ALL` (~95 GB). |
| 2 | `urna-logs audit --ufs AC --turno 1` | Por urna: lê BU + RDV, reconta presidente, compara RDV ≡ BU. `-v` lista divergências. |
| 3 | `urna-logs by-municipio --ufs AC --turno 1` | Agrega a audit por município (% sem digital, votos). |
| 4 | `urna-logs cruzar-oficial --ufs AC --turno 1` | Cruza BU × CSV oficial (`votacao_secao_*_BR`). Baixa o ZIP oficial uma vez em `data/ref/`. |
| 5 | `urna-logs horario --ufs AC --turno 1` | (Opcional) Curva hora a hora das habilitações + % pós-17h (log). |
| 6 | `urna-logs viability --ufs AC --turno 1` | (Opcional) Catálogo do log + métricas de biometria / pós-17h. |
| 7 | Quando o CDN publicar o 2º: `download` + `audit --turno 2`, depois `urna-logs comparar-turnos --ufs AC` | Seção a seção 1º × 2º (abstenção, totais). |

Sugestão de escala: comece com UFs pequenas (`AC` → `RR AP ZZ`), confira se RDV ≡ BU, depois amplie para outras UFs / `ALL`.

## Plano

Prioridade: as **duas análises principais** abaixo. Curto prazo / infra só desbloqueiam ou enriquecem essas leituras.

### 1. Comparativo 1º × 2º turno (seção a seção) — análise principal
Chave de junção: `join_key` = `UF:municipio:zona:secao` (sem o local — ele pode mudar em contingência).

**Objetivo:** analisar **seção a seção** o comportamento dos votos — o que mudou entre turnos, de onde veio a diferença (abstenção, finalistas, eliminados, brancos/nulos, seções novas/sumidas) e cruzar com indicadores de risco (% sem digital, pós-17h). Não é “quem migrou”, e sim **reconstruir o saldo agregado da seção** para explicar o Δ.

**Dá para medir (só no total da seção — não eleitor a eleitor):**
- [x] Esqueleto `comparar-turnos` (Parquet/MD com status `pendente_2t`)
- [ ] Aptos, comparecimento e **abstenção** 1º vs 2º (diferença e %) — quando 2º existir
- [ ] Votos nos finalistas no 2º vs o que a seção tinha no 1º
- [ ] Mudança da margem na seção entre os dois finalistas
- [ ] Saldo aparente dos votos de quem ficou de fora no 1º (só como total da seção)
- [ ] Brancos/nulos 1º→2º; seções que aparecem ou somem (contingência, ZZ, etc.)
- [ ] Relatório/painel por seção: decomposição do Δ (abstenção × transferência aparente × brancos/nulos) + ranking das seções que mais explicam a mudança na UF

**Não dá (sigilo do voto):** saber *quem* mudou de um candidato para outro. O RDV não identifica eleitor entre turnos. Qualquer “migração” é só estimativa pelo total da seção.

Antes disso: Parquet de seção nos dois turnos + 2º turno publicado.

### 2. Horário da votação e impacto pós-17h — análise principal
Fonte: log da urna (horário de cada `Eleitor foi habilitado`). O BU só traz abertura/encerramento da seção; o RDV não tem hora por voto. Critério: ≥17h em **Brasília** (ZZ = horário local do posto).

**Objetivo:** medir **quanto o fluxo depois das 17h** (fila / eventual ampliação) pesou no comparecimento — por UF, município e seção — se há padrões atípicos, e como isso se relaciona com o Δ 1º×2º na mesma seção.

- [x] Gerar Parquet de habilitações com `dt` + hora + `join_key` (`urna-logs horario`)
- [x] Distribuição **hora a hora por UF** + página Quarto
- [x] Indicadores: % ≥17h; faixas 17–18h, 18–19h, 19h+
- [ ] Cruzar seções com alto % pós-17h × resultado presidente / abstenção (só agregado)
- [x] Esqueleto `comparar-turnos` (preenche Δ horário quando o 2º existir)
- [ ] Comparar 1º × 2º no mesmo recorte horário (dados do 2º)

**Limite:** horário = momento da **habilitação**, não do voto em cada cargo; não dá para saber em quem votou quem chegou depois das 17h.

### Infra / curto prazo (desbloqueio)
- [x] Gravar `audit` em **Parquet** (seções + votos + várias UFs juntas)
- [ ] Fechar `audit` nacional 1º turno (todas as UFs)
- [x] Cruzamento com o **resultado oficial** (`cruzar-oficial`, presidente × seção)
- [x] Curva horária nacional 1º turno (`horario`, BRT)
- [ ] Testar 2º turno assim que existir `…_2t_*.zip` — [monitorar dados abertos](https://dadosabertos.tse.jus.br/dataset/resultados-2026-arquivos-transmitidos-para-totalizacao)

### Médio prazo (painel e cruzamentos)
- [x] Site Quarto consolidado (Painel 1º×2º + Método)
- [ ] Preencher no painel as duas análises principais quando o 2º existir (Δ seção + horário)
- [ ] Scatter seção a seção (% sem digital × Δ; pós-17h × Δ)
- [ ] Alertas de anomalia: seções fora do padrão (% sem digital, pós-17h, comparecimento, mudança extrema 1º→2º)
- [ ] Cruzar log × BU (habilitações do log vs comparecimento)
- [ ] Validar assinaturas / hashes (`.vsc`) — integridade do pacote

### Fora de escopo (por enquanto)
- Recontagem de outros cargos (deputado, governador, …) — o schema já permite; o foco agora é presidente
- Seguir eleitor individual entre turnos (impossível com os arquivos públicos)
- Provar que o hardware da urna está correto
- Afirmar “eleição íntegra” só porque RDV, BU e CSV oficial coincidem

## Site (Quarto → GitHub Pages)

**Duas páginas:** Painel (foco nas duas análises principais + sem digital como risco) e Método/glossário.

```bash
python scripts/build_site_data.py   # painel_uf.csv, curva_horaria.csv, outliers_…
quarto render site                  # requer Quarto: https://quarto.org
quarto preview site
```

- Fonte: `site/index.qmd` (painel), `site/metodo.qmd`, `site/data/`
- CI: `.github/workflows/quarto-publish.yml` → branch `gh-pages`
- URL: `https://mclaguiar.github.io/urna-logs-2026/`

No GitHub: **Settings → Pages** com source = branch `gh-pages` (após o primeiro publish). Em **Settings → Actions → General**, permitir write para o workflow (`GITHUB_TOKEN`).

## Fontes

- **Monitorar 2º turno:** [Resultados 2026 — Arquivos transmitidos para totalização](https://dadosabertos.tse.jus.br/dataset/resultados-2026-arquivos-transmitidos-para-totalizacao) — BU, RDV, log, assinatura por UF (1º e 2º; só situação “Totalizado”). Quando aparecerem pacotes do 2º, rodar `download` / `audit --turno 2`.
- [Resultados 2026](https://dadosabertos.tse.jus.br/dataset/resultados-2026) — votação oficial por seção / município-zona (para cruzar com a `audit`)
- Schemas ASN.1 BU/RDV 2026 (em `src/urna_logs/spec/`)
