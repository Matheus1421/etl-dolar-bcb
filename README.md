# ETL - Dollar Historical in Brazil

## Status

🚧 In development — Fase 1 capstone project (Data Journey). Extract complete and tested; Transform in design.

## About

ETL pipeline extracting, cleaning, and classifying USD/BRL exchange rate data from the Brazilian Central Bank (BCB) PTAX/Olinda API, covering the full historical series from 1985 to the present — including three distinct exchange-rate regimes and Brazil's currency redenominations along the way. Built to practice end-to-end data engineering fundamentals: pure functions, type hints, automated tests, and logging.

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

### Extract - Complete ✅

- **Source:** BCB API - https://dadosabertos.bcb.gov.br/dataset/dolar-americano-usd-todos-os-boletins-diarios
- **Date range:** 1985-01-01 through today (dynamic). 
- **Excluded:** 1984 data, there are only 22 irregular records, multiple quotes per day — insufficient granularity.
- `extract.py` exposes `extract_data()` (fetches and returns the raw records) and `save_raw_data()` (writes them to `data/raw/raw.json`). Fully covered by `tests/test_extract.py` (3/3 passing), using `unittest.mock` and the `tmp_path` fixture.

### Transform — in design 🏗️


### Load - to be done 🔜

## How to run

_To be added once `pipeline.py` is implemented._
