import pandas as pd
from pathlib import Path
import logging
from etl.utils.paths import RAW_DATA_DIR

def load_raw_table(table:str) -> pd.DataFrame:
    """
    Loads and combines clean and messy versions of a table from data/raw/.
    Args:
        table (str): Table name without suffix, e.g. 'customers', 'claims'
    Returns:
        pd.DataFrame: Combined DataFrame from clean and messy CSVs.
    """

    clean_path = RAW_DATA_DIR / f"{table}_clean.csv"
    messy_path = RAW_DATA_DIR / f"{table}_messy.csv"

    dfs = []
    if clean_path.exists():
        dfs.append(pd.read_csv(clean_path))
    if messy_path.exists():
        dfs.append(pd.read_csv(messy_path))

    if not dfs:
        raise FileNotFoundError(f"No data found for {table} in {RAW_DATA_DIR}")

    combined = pd.concat(dfs, ignore_index=True)
    logging.info(f"Loaded {len(combined)} rows from table {table}")
    return combined