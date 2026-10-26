# urna-logs-2026

Validação dos arquivos transmitidos para totalização (TSE) nas Eleições 2026.

## Análises

- Conferência de totais (habilitações no log × BU)
- % de habilitações sem biometria (1º e 2º turno)
- Impacto de votos/habilitações após 17h

## Requisitos

- Python 3.12+
- Disco livre recomendado: ~250 GB (1º turno nacional ≈ 95 GB de ZIPs + folga para Parquet)

## Setup (macOS / Linux)

```bash
git clone https://github.com/mclaguiar/urna-logs-2026.git
cd urna-logs-2026
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Setup (Windows)

No PowerShell ou cmd (com Python 3.12+ no PATH):

```bat
git clone https://github.com/mclaguiar/urna-logs-2026.git
cd urna-logs-2026
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Uso

```bash
# Download retomável (AC, 1º turno) — se interromper, rode de novo
urna-logs download --ufs AC --turno 1

# Várias UFs
urna-logs download --ufs "AC RR AP" --turno 1

# País (1º turno ≈ 95 GB)
urna-logs download --ufs ALL --turno 1

# Catálogo de mensagens (fase 0 / viabilidade)
urna-logs catalog --ufs AC --turno 1

# Métricas (biometria, pós-17h, totais)
urna-logs metrics --ufs AC --turno 1

# Relatório de viabilidade (catálogo + métricas)
urna-logs viability --ufs AC --turno 1
```

## Arquivos gerados

| Caminho | Conteúdo |
|---|---|
| `data/raw/*.zip` | ZIPs do TSE (não versionados) |
| `data/raw/download_state.json` | Estado do download (retomada) |
| `reports/catalog_*_Nt.json` | Catálogo de mensagens |
| `reports/metrics_*_Nt.parquet` | Uma linha por habilitação |
| `reports/metrics_summary_*_Nt.csv` | Resumo (% sem digital, % pós-17h) |
| `reports/viability_*_Nt.md` | Parecer go/no-go |

## Ordem sugerida

1. `download` de uma UF pequena (ex.: AC)
2. `viability` nessa UF
3. Se ok, escalar outras UFs / `ALL`
4. Agregar os `metrics_summary_*.csv` ou Parquets para consolidado nacional

## Fonte

[Arquivos transmitidos para totalização 2026](https://dadosabertos.tse.jus.br/dataset/resultados-2026-arquivos-transmitidos-para-totalizacao)
