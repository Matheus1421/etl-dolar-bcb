import datetime
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

regimes = [
        {"start":datetime.date(1985, 1, 1), "end":datetime.date(1990, 3, 18), "regime":"administrado"},
        {"start":datetime.date(1990, 3, 19), "end":datetime.date(2011, 6, 30), "regime":"interbancário"},
        {"start":datetime.date(2011, 7, 1), "end": datetime.date.today(), "regime":"PTAX"}
]

currencies = [
    {"start": datetime.date(1985, 1, 1), "end": datetime.date(1986, 2, 27), "currency": "cruzeiro", "factor": 2_750_000_000_000},
    {"start": datetime.date(1986, 2, 28), "end": datetime.date(1989, 1, 15), "currency": "cruzado", "factor": 2_750_000_000},
    {"start": datetime.date(1989, 1, 16), "end": datetime.date(1990, 3, 15), "currency": "cruzado novo", "factor": 2_750_000},
    {"start": datetime.date(1990, 3, 16), "end": datetime.date(1993, 7, 31), "currency": "cruzeiro", "factor": 2_750_000},
    {"start": datetime.date(1993, 8, 1), "end": datetime.date(1994, 6, 30), "currency": "cruzeiro real", "factor": 2750},
    {"start": datetime.date(1994, 7, 1), "end": datetime.date.today(), "currency": "real", "factor": 1},
]

def define_regime(data_raw: datetime.datetime) -> str: 
    data = data_raw.date()

    for period in regimes:
        if period["start"] <= data <= period["end"]:
            return period["regime"]

    raise ValueError(f"No regime found for the date {data}")


def define_currency(data_raw: datetime.datetime) -> tuple[str, float]:
    data = data_raw.date()

    for period in currencies:
        if period["start"] <= data <= period["end"]:
            return period["currency"], period["factor"]

    raise ValueError(f"No currency found for the date {data}")



def convert_to_brl(value_raw: float,  factor:float) -> float:
    return value_raw / factor

def transform_data(data: list[dict]) -> pd.DataFrame:
    logger.info("Starting data transformation")

    df = pd.DataFrame(data)
    df["dataHoraCotacao"] = pd.to_datetime(df["dataHoraCotacao"])
    df = df[df["dataHoraCotacao"] > "1984-12-31"]
    logger.info("Initial changes applied")

    df["regime"] = df["dataHoraCotacao"].apply(define_regime)
    logger.info("Regime added")
    df[["currency", "factor"]] = df["dataHoraCotacao"].apply(define_currency).apply(pd.Series)
    logger.info("Currency and factor added")
    df["value_brl_compra"] = df.apply(lambda line: convert_to_brl(line["cotacaoCompra"], line["factor"]), axis=1)
    df["value_brl_venda"] = df.apply(lambda line: convert_to_brl(line["cotacaoVenda"], line["factor"]), axis=1)
    logger.info("Value in BRL added")

    df = df.drop(columns=["factor"])

    logger.info(f"Data transformation completed: {len(df)} records processed")

    return df