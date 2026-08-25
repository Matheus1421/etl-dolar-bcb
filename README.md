# etl-dolar-bcb

## Status

🚧 In development — Fase 1 capstone project (Data Journey)
🚧 Em desenvolvimento — projeto capstone da Fase 1 (Data Journey)

## About / Sobre

**EN:** ETL pipeline extracting, cleaning, and aggregating USD/BRL exchange rate data from the Brazilian Central Bank (BCB) SGS API, series 1. Built to practice end-to-end data engineering fundamentals: pure functions, type hints, automated tests, and logging.

**PT:** Pipeline de ETL que extrai, trata e agrega a cotação do dólar (USD/BRL) via API SGS do Banco Central, série 1. Construído para praticar os fundamentos de engenharia de dados ponta a ponta: funções puras, type hints, testes automatizados e logging.

## Stack

- Python 3.x
- pandas
- requests
- pytest
- pyarrow (Parquet)

## Structure / Estrutura

etl-dolar-bcb/
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── data/
│   ├── raw/
│   └── processed/
├── requirements.txt
└── README.md

## Pipeline

### Extract

- **Source / Fonte:** BCB SGS API, series `1` (USD/BRL commercial rate, sell / dólar comercial, venda, diário). No authentication required.
- **Date range / Período:** **TBD**

### Transform

- Type conversion: date string → `datetime`, value string → `float` / Conversão de tipos: data em string → `datetime`, valor em string → `float`
- Handling of missing values (non-trading days) / Tratamento de valores ausentes (dias sem pregão)
- At least one `groupby` aggregation / Pelo menos uma agregação com `groupby` — granularity **TBD** (likely monthly summary: mean/min/max/std)
- Optional: daily percentage change as a derived column / Opcional: variação percentual diária como coluna derivada

### Load

- Output format: Parquet / Formato de saída: Parquet
- Location and file structure in `data/processed/`: **TBD**

## Decisions / Decisões

_This section is updated as choices are made during development._
_Esta seção é atualizada conforme as decisões são tomadas ao longo do desenvolvimento._

- Date range chosen and why / Período escolhido e por quê: —
- Aggregation granularity chosen and why / Granularidade da agregação escolhida e por quê: —
- Output structure chosen and why / Estrutura de saída escolhida e por quê: —

## How to run / Como rodar

_To be added once `pipeline.py` is implemented._
_A ser adicionado assim que `pipeline.py` estiver implementado._
