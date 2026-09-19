import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(df: pd.DataFrame, path: str = "data/processed/processed.parquet") -> None:
    logger.info("Ensuring processed data folder exists")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    logger.info(f"Saving processed data to {path}")
    df.to_parquet(path, index=False)

    logger.info(f"Processed data saved: {len(df)} records written to {path}")
