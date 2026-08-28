import requests
import datetime
import logging
import os
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

final_date = datetime.date.today().strftime("%m-%d-%Y")
start_date = "01-01-1985"
url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='{start_date}'&@dataFinalCotacao='{final_date}'&$format=json"

def extract_data() -> list[dict]:
    logger.info("Starting data extraction via PTAX API")
    response = requests.get(url)

    logger.info("Checking the data extraction status")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as erro:
        logger.error(f"Error in API request: {erro}")
        raise

    data = response.json()
    logger.info(f"Successfully completed data extraction: {len(data['value'])} records retrieved")
    return data['value']

def save_raw_data(dados: list[dict], path: str = "data/raw/raw.json") -> None:
    logger.info("Ensuring raw data folder exists")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    logger.info(f"Saving raw data to {path}")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    logger.info(f"Raw data saved: {len(dados)} records written to {path}")
