import pandas as pd
import logging
from etl.schema_definition import SchemaType
from etl.utils.paths import TRANSFORMED_DATA_DIR, REJECTED_DATA_DIR, ensure_dir
from etl.validation.validate_data import validate_data
from etl.utils.helpers import parse_date, normalize_gender, normalize_region


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

def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the customers table with additional field-specific logic:
    - Normalize gender values to 'M' or 'F'
    - Standardize phone number format
    - Format names and emails
    - Ensure risk score is numeric
    """
    df = clean_dataframe(df)

    # Standardize names and email
    df["email"] = df["email"].str.lower()
    df["first_name"] = df["first_name"].str.title()
    df["last_name"] = df["last_name"].str.title()

    # Standardize date
    df["birth_date"] = df["birth_date"].apply(parse_date)

    # Normalize gender
    gender_map = {
        "m": "M", "male": "M", "man": "M",
        "f": "F", "female": "F", "woman": "F",
        "other": "Other", "nonbinary": "Other", "nb": "Other",
    }
    df["gender"] = df["gender"].str.strip().str.lower().map(gender_map).fillna(df["gender"])

    # Standardize phone numbers to format: 10-digit only (e.g., '5551234567')
    df["phone_number"] = df["phone_number"].str.replace(r"\D", "", regex=True)
    df["phone_number"] = df["phone_number"].str.slice(-10)  # Keep only last 10 digits

    # Normalize region
    df["region"] = df["region"].apply(normalize_region)

    # Ensure risk_score is numeric
    df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce")

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