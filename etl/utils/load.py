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
    print(f"Loading clean table: {clean_path}")
    messy_path = RAW_DATA_DIR / f"{table}_messy.csv"
    print(f"Loading messy: {messy_path}")

    dfs = []
    print("clean_path type:", type(clean_path))
    print("clean_path resolved:", clean_path.resolve())
    print("clean_path exists:", clean_path.exists())
    if clean_path.exists():
        dfs.append(pd.read_csv(clean_path))
    print("messy_path type:", type(messy_path))
    print("messy_path resolved:", messy_path.resolve())
    print("messy_path exists:", messy_path.exists())
    if messy_path.exists():
        print("Messy path exists")
        dfs.append(pd.read_csv(messy_path))

    if not dfs:
        raise FileNotFoundError(f"No data found for {table} in {RAW_DATA_DIR}")

    combined = pd.concat(dfs, ignore_index=True)
    logging.info(f"Loaded {len(combined)} rows from table {table}")
    return combined

load_raw_table("customers")