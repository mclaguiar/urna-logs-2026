# urna-logs-2026

Auditoria independente dos **arquivos públicos** do TSE (Eleições 2026, cargo **presidente**).

Trabalhamos só com o que foi **transmitido e publicado**. Objetivo: achar inconsistências e anomalias **justificáveis** seção a seção — não “provar fraude” a partir de padrão eleitoral agregado, nem afirmar que a eleição é íntegra só porque os arquivos batem.

```text
RDV (recontar)  →  BU da urna  →  CSV oficial divulgado
```

Divergência entre camadas é achado forte. Concordância total = os arquivos públicos são **consistentes entre si**; não prova hardware intacto nem ausência de problema antes da publicação.

## Postura: hierarquia A / B / C

| Nível | O quê | O que se pode dizer |
|---|---|---|
| **A** | Inconsistência **documental** (RDV≠BU, BU≠oficial, seção só num turno) | Indício documental — checar a cadeia |
| **B** | Anomalia **operacional** (confluência de flags na mesma seção) | Priorizar revisão; **≠** fraude comprovada |
| **C** | Padrão ecológico / flag isolada / taxas médias da UF | Contexto de saldos; **não** sustenta fraude sozinho |

Caminho principal (**auditoria séria**): A → B, sempre no nível da **seção** (`join_key` = `UF:municipio:zona:secao`).  
Nível C (`fluxo-ecologico`) é anexo opcional — médias de UF, não “o que aconteceu nesta urna”.

Limiares pré-registrados: `urna_logs.thresholds` (versão no relatório de `achados`). Detalhe do método: [site/metodo.qmd](site/metodo.qmd).

## Como o programa funciona

Cada comando lê o que o anterior gravou em `data/` / `reports/` e escreve Parquet (análise) + Markdown/CSV (leitura).

| # | Comando | Papel |
|---|---|---|
| 1 | `download` | Baixa ZIP da UF (retomável). `--ufs ALL` ≈ 95 GB no 1º. |
| 2 | `audit` | Por urna: reconta presidente no RDV e compara com o BU. |
| 3 | `by-municipio` | Agrega a audit por município (mapa / % sem digital). |
| 4 | `cruzar-oficial` | BU × CSV oficial por seção (baixa o ZIP nacional uma vez em `data/ref/`). |
| 5 | `horario` | Curva de habilitações no log + % ≥17h (BRT; ZZ = local). `--por-secao` grava pós-17h por `join_key`. |
| 6 | `comparar-turnos` | Junta 1º×2º na mesma seção: Δ votos/abstenção/margem + flags. |
| 7 | `achados` | Empacota A/B/C em fichas reproduzíveis. |

**Opcionais:** `viability` / `catalog` / `metrics` (exploração do log); `fluxo-ecologico` + `validar-fluxo` (Nível C — limites Duncan–Davis por seção + taxas médias UF; validar = sanidade do algoritmo, não da eleição); `inspect` (olhar dentro do ZIP).

Repita `download` → `audit` → `cruzar` → `horario` para o **2º turno** (`--turno 2`) antes de `comparar-turnos` / `achados`.

### O que medimos (e o que não)

| Conseguimos | Não conseguimos |
|---|---|
| RDV ≡ BU e BU ≡ oficial por seção | Saber *quem* votou em quem / migrou entre turnos |
| Δ 1º×2º (abstenção, finalistas, margem, seções só num turno) | Provar integridade do **hardware** da urna |
| % sem digital no BU; % habilitações ≥17h no log | Afirmar “eleição limpa” só porque as três camadas batem |
| Ranking de seções com confluência operacional (B) | Auditar outros cargos neste pipeline (ainda) |

“Nenhuma divergência” em `audit` / `cruzar-oficial` = só **integridade entre os arquivos públicos comparados**.

## Setup

```bash
git clone https://github.com/mclaguiar/urna-logs-2026.git
cd urna-logs-2026
python3 -m venv .venv          # macOS / Linux
# Windows: py -3.12 -m venv .venv   (ou py -3.15)
source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"
urna-logs --help
```

Requisitos: Python **3.12+**; ~250 GB livres se for baixar o país no 1º turno.

**Windows — NumPy / `cp315` vs Python 3.10:** o venv misturou interpretadores. Recrie com o launcher explícito:

```powershell
Remove-Item -Recurse -Force .venv
py -3.15 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Uso (auditoria séria)

```bash
# 1º turno (base documental)
urna-logs download --ufs "AC RR AP ZZ" --turno 1
urna-logs audit --ufs "AC RR AP ZZ" --turno 1
urna-logs by-municipio --ufs "AC RR AP ZZ" --turno 1
urna-logs cruzar-oficial --ufs "AC RR AP ZZ" --turno 1
urna-logs horario --ufs "AC RR AP ZZ" --turno 1 --por-secao

# 2º turno (quando o CDN publicar)
urna-logs download --ufs "AC RR AP ZZ" --turno 2
urna-logs audit --ufs "AC RR AP ZZ" --turno 2
urna-logs cruzar-oficial --ufs "AC RR AP ZZ" --turno 2
urna-logs horario --ufs "AC RR AP ZZ" --turno 2 --por-secao

# Comparativo seção a seção + fichas A/B/C
urna-logs comparar-turnos --ufs "AC RR AP ZZ"
urna-logs achados --ufs "AC RR AP ZZ"

# Anexo C (opcional — não é o caminho sério)
# urna-logs fluxo-ecologico --ufs "AC RR AP ZZ"
# urna-logs validar-fluxo --ufs "AC RR AP ZZ"
```

Escala sugerida: UFs pequenas (`AC` → `RR AP ZZ` → …) → `ALL`.  
`-v` no `audit` lista divergências na hora. `horario` sem `--por-secao` só gera curva UF (rápido); com `--por-secao` alimenta flags de pós-17h no comparativo.

## Dados gerados

| Onde | O quê |
|---|---|
| `data/raw/*.zip` | Pacotes TSE (não versionados); `download_state.json` para retomar |
| `data/ref/` | Oficial (`votacao_secao_*`), Parquets por UF, `municipios_tse.csv` |
| `reports/audit_presidente_*` | RDV×BU (`.parquet` seções + votos, `.md`/`.csv`) |
| `reports/cruzar_oficial_*` | BU × oficial |
| `reports/horario_*` / `horario_secao_*` / `curva_horaria_*` | Log: curva e pós-17h |
| `reports/comparar_turnos_*` | 1º×2º por seção + flags |
| `reports/achados_*` | Fichas A/B/C |
| `reports/fluxo_*` | Anexo ecológico (C), se rodado |
| `src/urna_logs/spec/*.asn1` | Schemas oficiais BU/RDV 2026 |

Parquet = base de análise; Markdown/CSV = leitura rápida. Várias UFs: arquivos `*_MULTI_*`.

## Glossário (curto)

| Termo | Significado |
|---|---|
| **BU / RDV** | Totais da urna / sequência de votos sem identificar eleitor |
| **Log** | Eventos da urna; fonte do horário de habilitação |
| **Sem digital (BU)** | Biografia + sem biometria (canônico no painel) |
| **Pós-17h** | Habilitação ≥17h em Brasília (ZZ = horário local) |
| **`join_key`** | `UF:municipio:zona:secao` — cruzar turnos e BU×oficial |
| **Parquet** | Detalhe colunar local (não sobe ao GitHub Pages) |

Glossário completo e inferência ecológica: [site/metodo.qmd](site/metodo.qmd).

## Status e próximos passos

- **1º e 2º turno:** download/audit/cruzar em escala nacional conforme CDN ([arquivos transmitidos](https://dadosabertos.tse.jus.br/dataset/resultados-2026-arquivos-transmitidos-para-totalizacao)).
- **Comparativo + achados:** piloto AC/RR/AP/ZZ/RO/SE; restante do país em andamento (`horario --por-secao` → `comparar-turnos` → `achados`).
- **Painel Quarto:** KPIs, scatter, fichas A/B.
- **Ainda não:** validação `.vsc`; cruzar contagem do log × comparecimento do BU; outros cargos.

## Site (Quarto → GitHub Pages)

```bash
python scripts/build_site_data.py
quarto render site                  # https://quarto.org
quarto preview site
```

- Páginas: `site/index.qmd` (painel), `site/metodo.qmd`
- CI: `.github/workflows/quarto-publish.yml` → `gh-pages`
- URL: https://mclaguiar.github.io/urna-logs-2026/

## Fontes

- [Arquivos transmitidos para totalização 2026](https://dadosabertos.tse.jus.br/dataset/resultados-2026-arquivos-transmitidos-para-totalizacao) — BU, RDV, log por UF (1º/2º)
- [Resultados 2026](https://dadosabertos.tse.jus.br/dataset/resultados-2026) — votação oficial (cruzar com a audit)
- Schemas ASN.1 em `src/urna_logs/spec/`
