# urna-logs-2026

Auditoria independente dos arquivos transmitidos para totalização (TSE) — Eleições 2026.

Foco atual: **cargo presidente** (recontagem RDV × BU) e **habilitação sem digital** (detalhe do BU, agregado por UF/município).

## Status (piloto)

| Etapa | Situação |
|---|---|
| Download retomável (1º turno) | OK — URL `…_1t_{UF}.zip` |
| Download 2º turno | Aguardando publicação no CDN (`…_2t_…` → 404) |
| Parser ASN.1 BU/RDV (schemas TSE 2026) | OK |
| `audit` presidente urna a urna | OK — AC, RR, AP, ZZ: **7.013/7.013** RDV ≡ BU |
| `by-municipio` (votos + % sem digital) | OK — nomes via perfil eleitorado TSE |
| Métricas de log (biometria / pós-17h) | OK no AC (fase viabilidade) |
| Consolidado nacional / anomalias | Planejado |

## O que audita (e o que não)

**Cobre:** cadeia pós-urna nos pacotes abertos do TSE — recontar votos do RDV, confrontar com o BU, cruzar habilitação biométrica e geografia (UF/município/zona/seção).

**Não cobre:** o que ocorreu dentro do hardware antes de gravar o RDV (isso exigiria verificação de assinaturas HW/certificação).

## Formato de dados (várias visões)

**Parquet é o formato analítico canônico** para reprocessar e gerar visões depois (UF, município, zona, horário, candidato).

| Camada | Formato | Uso |
|---|---|---|
| Bruto TSE | ZIP (`data/raw/`) | Fonte imutável, retomável |
| Grão fino | **Parquet** | Uma linha por urna / habilitação / voto agregado — base para pivôs |
| Entrega humana | Markdown + CSV curto | Relatórios e planilha rápida |
| Referência | CSV em `data/ref/` | Nomes de município TSE |

Motivo do Parquet: colunar, tipado, compressão boa, leitura parcial, funciona bem com pandas/polars/DuckDB. CSV fica só para exportes leves.

`audit` grava **Parquet de seções** + **Parquet longo de votos** (e CSV leve). Consolidado multi-UF: `audit_presidente_MULTI_{t}t.parquet`. Chave entre turnos: `join_key = UF:municipio:zona:secao`.

## Análises

- Recontagem **presidente**: cada voto do RDV × totais do BU (por urna)
- Habilitação **sem digital** (BU): `bio` + `biografia` + `sem_biometria`  
  - *sem digital* = biografia + sem_biometria  
  - Exterior (ZZ) em geral **não traz** esse detalhe no BU
- Agregação por **município** (código TSE + nome)
- Viabilidade de log: catálogo de mensagens, biometria no log, eventos após 17h

## Requisitos

- Python 3.12+ (testado também com 3.15)
- Disco: ~250 GB livres se for baixar o 1º turno nacional (≈ **95 GB** de ZIPs + folga)

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
# Download retomável (UF pequena)
urna-logs download --ufs AC --turno 1

# Várias UFs / país (1º turno ≈ 95 GB)
urna-logs download --ufs "AC RR AP ZZ" --turno 1
urna-logs download --ufs ALL --turno 1

# Viabilidade (log): catálogo + métricas biometria/pós-17h
urna-logs viability --ufs AC --turno 1

# Auditoria presidente (RDV × BU) — use -v para listar divergências na hora
urna-logs audit --ufs "AC RR AP ZZ" --turno 1
urna-logs audit --ufs AC --turno 1 -v

# Visão por município (lê o CSV da audit + nomes TSE)
urna-logs by-municipio --ufs "AC RR AP ZZ" --turno 1
```

O download e o `audit` são verbosos por padrão (UF atual, tamanho, barra OK/fail).

## Arquivos gerados

| Caminho | Conteúdo |
|---|---|
| `data/raw/*.zip` | ZIPs do TSE (não versionados) |
| `data/raw/download_state.json` | Estado do download (retomada) |
| `data/ref/municipios_tse.csv` | Cache código → nome do município |
| `reports/catalog_*_Nt.json` | Catálogo de mensagens do log |
| `reports/metrics_*_Nt.parquet` | Uma linha por habilitação (log) |
| `reports/metrics_summary_*_Nt.csv` | Resumo log (% sem digital, % pós-17h) |
| `reports/viability_*_Nt.md` | Parecer go/no-go (log) |
| `reports/audit_presidente_*_Nt.md` | Recontagem presidente RDV × BU |
| `reports/audit_presidente_*_Nt.csv` | Seções (leve / Excel) |
| `reports/audit_presidente_*_Nt.parquet` | Seções: aptos, comparecimento, abstenção, bio, `join_key` |
| `reports/audit_presidente_votos_*_Nt.parquet` | Votos longos: seção × tipo × número |
| `reports/audit_presidente_MULTI_*t.parquet` | Consolidado multi-UF (seções + votos) |
| `reports/by_municipio_*_Nt.md` | Ranking municipal (% sem digital, votos) |
| `reports/by_municipio_*_Nt.csv` | Agregado municipal |
| `src/urna_logs/spec/*.asn1` | Schemas oficiais BU/RDV 2026 |

## Ordem sugerida

1. `download` de UFs pequenas (AC → RR AP ZZ)
2. `audit` nessas UFs (validar RDV ≡ BU)
3. `by-municipio` (visões geo + sem digital)
4. Escalar UFs / `ALL` no 1º turno
5. Quando o CDN publicar: `audit --turno 2` nas mesmas UFs
6. Painel **seção a seção 1º×2º** (migração agregada, abstenção, swing)
7. Camada Parquet unificada + detectores de anomalia

## Plano

### Curto prazo
- [x] Gravar `audit` em **Parquet** (seções + votos longos + consolidado multi-UF)
- [ ] Escalamento 1º turno (ondas: pequenas → médias → SP/MG/…)
- [ ] Smoke-test 2º turno assim que `…_2t_*.zip` existir
- [ ] Cruzar totais presidente com resultado oficial divulgado (sanity check)

### Comparativo 1º × 2º turno (seção a seção)
Chave de junção: `join_key` = `UF:municipio:zona:secao` (local omitido — pode mudar em contingência).

**Dá para medir (agregado da seção — não eleitor a eleitor):**
- [ ] Aptos, comparecimento e **abstenção** 1t vs 2t (Δ e %)
- [ ] Votos nos finalistas no 2t vs votos/“reservatório” no 1t na mesma seção
- [ ] Swing líquido na seção (ex.: variação da margem entre os dois finalistas)
- [ ] Destino aparente dos votos de candidatos eliminados (só como saldo de seção)
- [ ] Brancos/nulos 1t→2t; seções que surgem/somem (contingência, ZZ, etc.)

**Não dá (sigilo do voto):** saber *quem* migrou de A para B. O RDV embaralha/ordena votos; não há id de eleitor entre turnos. Qualquer “migração” é inferência ecológica na seção.

Pré-requisito: Parquet de urna/seção nos dois turnos + 2º turno publicado.

### Médio prazo
- [ ] Detector de anomalias: seções outliers (% sem digital, pós-17h, comparecimento, swing extremo 1t→2t)
- [ ] Cruzar log × BU (habilitações do log vs comparecimento)
- [ ] Validação de assinaturas / hashes (`.vsc`) — integridade do pacote
- [ ] Dashboard ou notebook sobre o Parquet unificado

### Fora de escopo (por enquanto)
- Recontagem de outros cargos (deputado, governador, …) — schemas já permitem; foco deliberado em presidente
- Rastreio individual de eleitor entre turnos (impossível com os arquivos públicos)
- Prova de corretude do hardware da urna

## Fonte

- [Arquivos transmitidos para totalização 2026](https://dadosabertos.tse.jus.br/dataset/resultados-2026-arquivos-transmitidos-para-totalizacao)
- Schemas ASN.1 BU/RDV 2026 (empacotados em `src/urna_logs/spec/`)
