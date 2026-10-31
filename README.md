# urna-logs-2026

Auditoria dos **arquivos públicos** do TSE (Eleições 2026, cargo **presidente**): inconsistências, saldos 1º×2º e taxas agregadas, seção a seção.

```text
RDV (recontar)  →  BU da urna  →  CSV oficial divulgado
```

Divergência entre camadas = achado documental. Concordância = os arquivos publicados são **consistentes entre si** na chave. Relatórios descrevem números e razoabilidade sob o modelo; interpretação causal ou jurídica fica com o leitor.

## Hierarquia A / B / C

| Nível | O quê | Uso |
|---|---|---|
| **A** | Inconsistência **documental** (RDV≠BU, BU≠oficial, seção só num turno) | Abrir a cadeia da seção |
| **B** | Anomalia **operacional** (confluência de flags na mesma seção) | Priorizar revisão |
| **C** | Padrão ecológico / flag isolada / taxas médias da UF | Contexto de saldos |

Caminho principal: A → B, no nível da **seção** (`join_key` = `UF:municipio:zona:secao`).  
Nível C (`fluxo-ecologico`) — médias de UF e bounds por seção.

Limiares: `urna_logs.thresholds`. Método: [site/metodo.qmd](site/metodo.qmd).

## Pipeline

Cada comando lê o que o anterior gravou em `data/` / `reports/` e escreve Parquet + Markdown/CSV.

| # | Comando | Papel |
|---|---|---|
| 1 | `download` | Baixa ZIP da UF (retomável). `--ufs ALL` ≈ 95 GB no 1º. |
| 2 | `audit` | Reconta presidente no RDV × totais do BU. |
| 3 | `by-municipio` | Agrega audit por município. |
| 4 | `cruzar-oficial` | BU × CSV oficial por seção. |
| 5 | `horario` | Dia oficial ± tolerância: janelas 8h–17h / pós / fora; histórico = outras datas no `.jez`. `--por-secao`. |
| 6 | `comparar-turnos` | 1º×2º na mesma seção: Δ + flags. |
| 7 | `achados` | Fichas A/B/C. |
| 8 | `verificar-vsc` | `-vota.vsc`: hashes do ZIP e Ed521. `--nivel 1` só hashes; `--nivel 2` só Ed521. |
| 9 | `fluxo-ecologico` | Duncan–Davis + taxas IPF com IC (Nível C). |
| 10 | `transferencia` | Matriz 1º→2º por cidade. Brown e Payne em cada seção, com intervalo de 95%. lphom na seção até 2.500 linhas; acima disso, por zona. No fim, leitura de cada estado e o consolidado do país. |

**Opcionais:** `viability` / `catalog` / `metrics`; `validar-fluxo`; `inspect`.

Repita `download` → `audit` → `cruzar` → `horario` para o **2º turno** (`--turno 2`) antes de `comparar-turnos` / `achados`.

### Escopo

| No pipeline | Fora (por desenho / ainda) |
|---|---|
| RDV ≡ BU e BU ≡ oficial por seção | Microdado de eleitor / migração pessoa a pessoa |
| Δ 1º×2º; % sem digital; pós-17h; flags B | Outros cargos |
| Fluxo ecológico (taxas + bounds) | Chave SW da cerimônia (`.vsc`) |
| Hashes `.vsc` nível 1 (arquivos no ZIP) | |
| Ed521 `.vsc` (padrão do `verificar-vsc`; extra `hw`) | |

### Prefixos em `reports/`

| Prefixo | Conteúdo |
|---|---|
| `audit_presidente_*` | RDV×BU |
| `cruzar_oficial_*` | BU×oficial |
| `horario_*` / `horario_secao_*` / `curva_horaria_*` | Log horário |
| `comparar_turnos_*` | 1º×2º + flags |
| `achados_*` | Fichas A/B/C |
| `fluxo_*` | Bounds / taxas / MD ecológico |
| `verificar_vsc_*` | Integridade `.vsc` |
| `hipoteses_fluxo_*` / `evidencia_nacional_*` | Consolidados nacionais (scripts) |

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

## Uso

```bash
# Exemplo piloto → escalar com ALL
urna-logs download --ufs "AC RR AP ZZ" --turno 1
urna-logs audit --ufs "AC RR AP ZZ" --turno 1
urna-logs by-municipio --ufs "AC RR AP ZZ" --turno 1
urna-logs cruzar-oficial --ufs "AC RR AP ZZ" --turno 1
urna-logs horario --ufs "AC RR AP ZZ" --turno 1 --por-secao

urna-logs download --ufs "AC RR AP ZZ" --turno 2
urna-logs audit --ufs "AC RR AP ZZ" --turno 2
urna-logs cruzar-oficial --ufs "AC RR AP ZZ" --turno 2
urna-logs horario --ufs "AC RR AP ZZ" --turno 2 --por-secao

urna-logs comparar-turnos --ufs "AC RR AP ZZ"
urna-logs achados --ufs "AC RR AP ZZ"
urna-logs fluxo-ecologico --ufs "AC RR AP ZZ"
urna-logs verificar-vsc --ufs "AC RR AP ZZ" --turno 1
urna-logs verificar-vsc --ufs "AC RR AP ZZ" --turno 2
```

## Pós-pipeline (sem baixar ZIP de novo)

```bash
python scripts/relatorio_evidencia_nacional.py          # A/B/C + log×BU + .vsc resumo
python scripts/relatorio_evidencia_nacional.py --all     # + hipóteses IPF + painel
python scripts/relatorio_hipoteses_fluxo.py              # só fluxo didático UF+Brasil
python scripts/build_site_data.py                       # site/data/*.csv
```

Se `outliers_sem_digital.csv` estiver bloqueado no Windows, o build grava `outliers_sem_digital.new.csv` (fallback).

## Status

- Pipeline 1º/2º e comparativo/achados/fluxo em escala **nacional** (28 UFs), conforme CDN.
- Consolidados: `reports/evidencia_nacional_1t_2t.md`, `reports/hipoteses_fluxo_1t_2t.md`.
- `.vsc`: `verificar-vsc` confere hashes e Ed521. `--nivel 1` fica só nos hashes; `--nivel 2` fica só no Ed521. O Ed521 precisa do extra `hw` (ECPy). Piloto de hashes no AC: 100%; demais UFs conforme job.
- Ainda: outros cargos.

## Site (Quarto → GitHub Pages)

```bash
python scripts/build_site_data.py
quarto render site
quarto preview site
```

- Páginas: `site/index.qmd`, `site/metodo.qmd`, `site/secao.qmd` (consulta UF → cidade → zona → seção)
- CI: `.github/workflows/quarto-publish.yml` → `gh-pages`
- URL: https://mclaguiar.github.io/urna-logs-2026/

## Fontes

- [Arquivos transmitidos 2026](https://dadosabertos.tse.jus.br/dataset/resultados-2026-arquivos-transmitidos-para-totalizacao) — BU, RDV, log, `.vsc`
- [Resultados 2026](https://dadosabertos.tse.jus.br/dataset/resultados-2026) — votação oficial
- Schemas ASN.1 em `src/urna_logs/spec/` (`bu`, `rdv`, `assinatura`)
