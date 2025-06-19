import pandas as pd
import logging
from etl.schema_definition import SchemaType
from etl.utils.paths import TRANSFORMED_DATA_DIR, REJECTED_DATA_DIR, ensure_dir
from etl.validation.validate_data import validate_data


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs basic data cleaning operations such as:
    - Removing duplicate rows
    - Stripping whitespace from string fields
    Args:
        df (pd.DataFrame): Raw input DataFrame

    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    df = df.drop_duplicates()
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return df


def split_valid_invalid(df: pd.DataFrame, schema: SchemaType) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Validates the dataframe and splits it into valid and invalid rows.
    Args:
        df (pd.DataFrame): Input DataFrame
        schema (SchemaType): Table schema
    Returns:
        Tuple of valid and invalid DataFrames
    """
    is_valid = validate_data(df, schema)
    return df[is_valid], df[~is_valid]


def save_transformed_data(df: pd.DataFrame, table: str) -> None:
    """
    Saves the valid (cleaned + validated) DataFrame to transformed/ as a CSV.
    Args:
        df (pd.DataFrame): Clean and validated DataFrame
        table (str): Table name (used for filename)
    """
    ensure_dir(TRANSFORMED_DATA_DIR)
    path = TRANSFORMED_DATA_DIR / f"{table}.csv"
    df.to_csv(path, index=False)
    logging.info(f"Saved {len(df)} rows to {path}")


def save_rejected_data(df: pd.DataFrame, table: str) -> None:
    """
    Saves the invalid DataFrame to rejected/ as a CSV.
    Args:
        df (pd.DataFrame): Invalid rows
        table (str): Table name (used for filename)
    """
    ensure_dir(REJECTED_DATA_DIR)
    path = REJECTED_DATA_DIR / f"{table}.csv"
    df.to_csv(path, index=False)
    logging.warning(f"Rejected {len(df)} rows saved to {path}")