# etl-dolar-bcb

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

### Extract — done

- **Source:** BCB PTAX/Olinda API (OData), `CotacaoDolarPeriodo` endpoint. No authentication required.
- **Date range:** 1985-01-01 through today (dynamic). No date-range limit on this API (unlike the SGS API's 10-year cap) and no need for `$top`/pagination — empirically verified against the full history (10,435 records, no truncation).
- **Excluded:** 1984 data (only 22 irregular records, multiple quotes per day — insufficient granularity).
- `extract.py` exposes `extract_data()` (fetches and returns the raw records) and `save_raw_data()` (writes them to `data/raw/raw.json`). Fully covered by `tests/test_extract.py` (3/3 passing), using `unittest.mock` and the `tmp_path` fixture.

### Transform — in design

- Type conversion: `dataHoraCotacao` string → `datetime`; `cotacaoCompra`/`cotacaoVenda` already arrive as floats.
- Filter out records before 1985-01-01.
- **Regime classification** (how the rate was calculated/published):
  - Administered rate — until 1990-03-18
  - Interbank average rate — 1990-03-19 to 2011-06-30
  - PTAX (average of 4 daily quotes, Circular 3506/2010) — since 2011-07-01
- **Currency classification** (which currency the raw value is denominated in): confirmed empirically — via a scratch test comparing values immediately before/after each currency-change date — that raw values reflect the currency in effect at the time, not a value retroactively normalized to Real. Six currencies apply across the period, each needing a conversion factor to express the value in Real:
  - Cruzeiro (until 1986-02-27): ÷ 1,000³ × 2,750
  - Cruzado (1986-02-28 to 1989-01-15): ÷ 1,000² × 2,750
  - Cruzado Novo (1989-01-16 to 1990-03-15): ÷ 1,000 × 2,750
  - Cruzeiro (1990-03-16 to 1993-07-31): ÷ 1,000 × 2,750
  - Cruzeiro Real (1993-08-01 to 1994-06-30): ÷ 2,750
  - Real (since 1994-07-01): no conversion needed
- **Output shape:** a single DataFrame (not split into separate DataFrames per regime), with added columns `regime`, `currency`, and derived `value_brl_compra` / `value_brl_venda` (converted to Real terms, filled for every row — for post-1994 rows this equals the original value, since it's already in Real). Original `cotacaoCompra`/`cotacaoVenda` are kept unchanged for traceability.
- Aggregation granularity for the `groupby` step: TBD.
- Optional: daily percentage change as a derived column: TBD.

### Load

- Output format: Parquet
- Location and file structure in `data/processed/`: TBD

## Decisions

_This section is updated as choices are made during development._

- **Data source:** BCB PTAX/Olinda API, not the SGS series `1` originally planned — richer fields (typed compra/venda, full datetime) and documented exchange-rate regimes that enable a more realistic classification exercise.
- **Date range:** 1985-01-01 to today. Empirically confirmed: no chunking needed (no date-range cap on this API, unlike SGS's 10-year limit) and no `$top` needed (full history returns without truncation). 1984 excluded due to sparse, irregular data.
- **Currency redenomination:** empirically confirmed that raw values are not retroactively normalized by the BCB — each reflects the currency in effect at the time it was recorded. Conversion to Real is therefore a real transformation requirement, not just a theoretical concern.
- **DataFrame structure:** a single DataFrame with `regime` and `currency` columns, rather than 3 separate DataFrames per regime — chosen to make cross-regime comparison easier later (planned reuse of this project's output in a Fase 3 statistics project).
- Aggregation granularity chosen and why: —
- Output structure chosen and why: —

## How to run

_To be added once `pipeline.py` is implemented._
