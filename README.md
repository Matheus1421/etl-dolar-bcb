# etl-dolar-bcb

## About

ETL pipeline extracting, cleaning, and classifying USD/BRL exchange rate data from the Brazilian Central Bank (BCB) PTAX/Olinda API, covering the full historical series from 1985 to the present — including three distinct exchange-rate regimes and the currency redenominations Brazil went through along the way. Built to practice end-to-end data engineering fundamentals: pure functions, type hints, automated tests, and logging.

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

### Extract — done

- **Source:** BCB PTAX/Olinda API (OData), `CotacaoDolarPeriodo` endpoint. No authentication required.
- **Date range:** 1985-01-01 through today (dynamic). No date-range cap and no need for `$top`/pagination — verified empirically against the full history (10,450 records, no truncation). 1984 excluded (only 22 irregular records).
- `extract_data()` fetches and returns the raw records; `save_raw_data()` writes them to `data/raw/raw.json`. Covered by `tests/test_extract.py` (3/3 passing).

### Transform — done

- Type conversion: `dataHoraCotacao` string → `datetime`. `cotacaoCompra`/`cotacaoVenda` arrive as floats already.
- Filters out records before 1985-01-01.
- Adds two classifications, both resolved from the record's date via lookup tables (a list of dicts per range, one axis for regime, one for currency):
  - **`regime`** — how the rate was calculated/published: administered, interbank average, or PTAX.
  - **`currency`** — which of Brazil's currencies since 1985 the raw value is denominated in (raw values are confirmed, empirically, to reflect the currency of the time rather than being retroactively normalized).
- Adds `value_brl_compra`/`value_brl_venda`: the original values converted to BRL terms using each currency's conversion factor. Always populated (post-1994 rows simply equal the original value, since it's already in Real) — the original `cotacaoCompra`/`cotacaoVenda` are kept unchanged alongside them for traceability.
- Output: a single DataFrame (not split per regime), one row per original record.
- Covered by `tests/test_transform.py` (12/12 passing).

### Load — done

- Writes the final DataFrame to Parquet at `data/processed/processed.parquet`, using `pandas.DataFrame.to_parquet` (with `pyarrow` as the underlying engine).
- Drops the pandas row index (`index=False`) before writing — it becomes fragmented by the 1985 filter applied in Transform and carries no useful information.
- Covered by `tests/test_load.py` (3/3 passing).

## Decisions

_This section is updated as choices are made during development._

- **Data source:** PTAX/Olinda API, not the SGS series `1` originally planned — richer typed fields and documented exchange-rate regimes.
- **Date range:** 1985-01-01 to today, verified empirically (no chunking or pagination needed). 1984 excluded for data quality reasons.
- **Currency handling:** raw values are denominated in whatever currency was legal tender at the time, confirmed by empirical testing around each redenomination date — hence the `currency`/`value_brl_*` columns in Transform.
- **Output shape:** a single DataFrame with `regime` and `currency` columns, rather than one DataFrame per regime — chosen to make cross-regime comparison easier in a future project.
- **Storage format:** Parquet over CSV/JSON for the processed output — columnar, preserves dtypes, and cheaper to read back for analysis.
- **Pipeline entry point:** `run_pipeline()` implemented as a function (not a bare script), guarded by `if __name__ == "__main__":` — runnable directly and reusable/importable later (tests, future projects).

## How to run

```bash
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python src/pipeline.py
```

Running `pipeline.py` executes the full chain — extract, save raw data, transform, load — producing `data/raw/raw.json` and `data/processed/processed.parquet`.
