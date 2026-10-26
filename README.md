# urna-logs-2026

Validação dos arquivos transmitidos para totalização (TSE) nas Eleições 2026.

## Análises

- Conferência de totais (habilitações no log × BU)
- % de habilitações sem biometria (1º e 2º turno)
- Impacto de votos/habilitações após 17h

## Requisitos

- Python 3.12+

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Uso

```bash
# Download retomável (AC, 1º turno)
urna-logs download --ufs AC --turno 1

# Catálogo de mensagens (fase 0 / viabilidade)
urna-logs catalog --ufs AC --turno 1

# Métricas (biometria, pós-17h, totais)
urna-logs metrics --ufs AC --turno 1

# Relatório de viabilidade
urna-logs viability --ufs AC --turno 1
```

## Fonte

[Arquivos transmitidos para totalização 2026](https://dadosabertos.tse.jus.br/dataset/resultados-2026-arquivos-transmitidos-para-totalizacao)
