# etl-dolar-bcb

## Status

🚧 In development — Fase 1 capstone project (Data Journey)

## About

ETL pipeline extracting, cleaning, and aggregating USD/BRL exchange rate data from the Brazilian Central Bank (BCB) SGS API, series 1. Built to practice end-to-end data engineering fundamentals: pure functions, type hints, automated tests, and logging.

## Stack

- Python 3.x
- pandas
- requests
- pytest
- pyarrow (Parquet)

## Structure

```
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
```

## Pipeline

### Extract

- **Source:** BCB SGS API, series `1` (USD/BRL commercial rate, sell, daily). No authentication required.
- **Date range:** TBD

### Transform

- Type conversion: date string → `datetime`, value string → `float`
- Handling of missing values (non-trading days)
- At least one `groupby` aggregation — granularity TBD (likely monthly summary: mean/min/max/std)
- Optional: daily percentage change as a derived column

### Load

- Output format: Parquet
- Location and file structure in `data/processed/`: TBD

## Decisions

_This section is updated as choices are made during development._

- Date range chosen and why: —
- Aggregation granularity chosen and why: —
- Output structure chosen and why: —

## How to run

_To be added once `pipeline.py` is implemented._
