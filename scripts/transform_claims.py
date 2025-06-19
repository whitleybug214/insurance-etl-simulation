import logging
from etl.schema_definition import claims_fact_schema
from etl.utils.load import load_raw_table
from etl.transform_base import (
    clean_dataframe,
    split_valid_invalid,
    save_transformed_data,
    save_rejected_data,
)

def main() -> None:
    table = "claims"
    schema = claims_fact_schema

    raw_df = load_raw_table(table)
    cleaned_df = clean_dataframe(raw_df)
    valid_df, invalid_df = split_valid_invalid(cleaned_df, schema)

    save_transformed_data(valid_df, f"{table}_fact")
    logging.info(f"{len(valid_df)} valid rows processed from {table}_fact")

    if not invalid_df.empty:
        save_rejected_data(invalid_df, f"{table}_fact")
        logging.warning(f"{len(invalid_df)} rows rejected from {table}_fact")


if __name__ == "__main__":
    main()