import logging
from etl.utils.load import load_raw_table
from etl.schema_definition import customers_schema
from etl.transform_base import (
    split_valid_invalid,
    save_transformed_data,
    save_rejected_data,
)
from etl.transform_base import clean_customers

logging.basicConfig(level=logging.INFO, format="%(asctime)s | [%(levelname)s] | %(message)s")

def main():
    """
    ETL transform script for customers data.
    Loads raw data, cleans it, validates against schema, and saves outputs.
    """
    table = "customers"
    raw_df = load_raw_table(table)
    logging.info(f"Loaded {len(raw_df)} raw rows from {table}")

    cleaned_df = clean_customers(raw_df)
    valid_df, invalid_df = split_valid_invalid(cleaned_df, customers_schema)
    logging.info(f"{len(valid_df)} valid rows, {len(invalid_df)} invalid rows after validation")

    save_transformed_data(valid_df, table)
    if not invalid_df.empty:
        save_rejected_data(invalid_df, table)


if __name__ == "__main__":
    main()