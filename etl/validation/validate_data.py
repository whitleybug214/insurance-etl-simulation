import pandas as pd
from pathlib import Path
import logging
from etl.utils.helpers import is_valid_type

REJECTED_DATA_DIR = Path("data/rejected")
REJECTED_DATA_DIR.mkdir(parents=True, exist_ok=True)

def validate_data(df: pd.DataFrame, schema: dict, table_name: str) -> pd.Series:
    """
    Validates the input DataFrame against the provided schema.
    Invalid rows are written to a rejected file with a rejection reason.
    Args:
        df (pd.DataFrame): Input DataFrame to validate.
        table_name (str): Name of the table (used for file naming).
        schema (dict): Expected schema definition {column: dtype}.
    Returns:
        pd.Series: Boolean Series indicating which rows are valid.
    """
    valid_rows = []
    rejected_rows = []
    is_valid_list = []

    for _, row in df.iterrows():
        reasons = []

        for column, expected_type in schema.items():
            value = row.get(column, None)

            if not is_valid_type(value, expected_type):
                reasons.append(f"Invalid type in '{column}': expected {expected_type}, got {type(value).__name__}")

        if reasons:
            row_with_reason = row.to_dict()
            row_with_reason["rejection_reason"] = "; ".join(reasons)
            rejected_rows.append(row_with_reason)
            is_valid_list.append(False)
        else:
            valid_rows.append(row)
            is_valid_list.append(True)

    # Save rejected rows
    if rejected_rows:
        rejected_df = pd.DataFrame(rejected_rows)
        rejected_path = REJECTED_DATA_DIR / f"{table_name}.csv"
        rejected_df.to_csv(rejected_path, index=False)
        logging.warning(f"{len(rejected_df)} rows rejected from {table_name} — written to {rejected_path}")

    logging.info(f"{len(valid_rows)} valid rows retained from {table_name}")
    return pd.Series(is_valid_list, index=df.index).fillna(False)