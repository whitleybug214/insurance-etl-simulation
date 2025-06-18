import pandas as pd
import logging
from pathlib import Path
from etl.schema_definition import customers_schema

"""
Transforms raw customer data (clean + messy) into a cleaned, validated dataset.
- Reads raw data from data/raw/
- Cleans and standardizes values
- Drops or flags invalid records
- Writes output to data/processed/customers.csv

Run from the project root using:
    python -m scripts.transform_customers
"""

logging.basicConfig(level=logging.INFO, format="%(asctime)s | [%(levelname)s] | %(message)s")

raw_dir = Path("data/raw")
processed_dir = Path("data/processed")
processed_dir.mkdir(exist_ok=True)

def load_data() -> pd.DataFrame:
    """Load clean and messy raw customer data"""
    clean_df = pd.read_csv(raw_dir / "customers_clean.csv")
    messy_df = pd.read_csv(raw_dir / "customers_messy.csv")
    combined = pd.concat([clean_df, messy_df], ignore_index=True)
    logging.info(f"Loaded {len(combined)} rows from clean and messy sources")
    return combined

