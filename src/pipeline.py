import logging

from extract import extract_data, save_raw_data
from transform import transform_data
from load import load_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_pipeline() -> None:
    raw_data = extract_data()
    logger.info("Data extracted")
    save_raw_data(raw_data)
    logger.info("Raw data saved")
    processed_data = transform_data(raw_data)
    logger.info("Data transformed")
    load_data(processed_data)
    logger.info("Processed data loaded")

if __name__ == "__main__":
    run_pipeline()