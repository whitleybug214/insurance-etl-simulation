import logging
from etl.utils.load import load_raw_table
from etl.schema_definition import adjusters_schema
from etl.transform_base import (
    clean_dataframe,
    split_valid_invalid,
    save_transformed_data,
    save_rejected_data,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    """
    ETL transform script for adjusters data.
    Loads raw data, cleans it, validates against schema, and saves outputs.
    """
    table = "adjusters"
    raw_df = load_raw_table(table)

    cleaned_df = clean_dataframe(raw_df)
    valid_df, invalid_df = split_valid_invalid(cleaned_df, adjusters_schema)

    save_transformed_data(valid_df, table)
    if not invalid_df.empty:
        save_rejected_data(invalid_df, table)

if __name__ == "__main__":
    main()
