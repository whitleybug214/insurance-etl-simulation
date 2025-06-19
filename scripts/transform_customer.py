import pandas as pd
import logging
from pathlib import Path
from etl.schema_definition import customers_schema
from etl.utils.load import load_raw_table
from etl.utils.paths import ensure_dir

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

processed_dir = ensure_dir("data/processed")

def load_data() -> pd.DataFrame:
    """Load clean and messy raw customer data"""
    return load_raw_table("customers")

