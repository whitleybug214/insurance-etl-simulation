import csv
from datetime import datetime, timedelta
from pathlib import Path
from etl.schema_definition import dates_schema

"""
Generates clean and messy date dimension records for the ETL pipeline simulation.

Outputs:
- dates_clean.csv: valid date records
- dates_messy.csv: includes intentional corruptions for testing

Run from the project root using:
    python -m scripts.generate_dates
"""

output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

columns = list(dates_schema.keys())


def generate_clean_dates(start_date: datetime, num_days: int) -> list[dict]:
    """
    Generate a list of valid date dimension records.
    Args:
        start_date (datetime): Starting date.
        num_days (int): Number of sequential days to generate.
    Returns:
        list[dict]: Clean date records.
    """
    records = []
    for i in range(num_days):
        current_date = start_date + timedelta(days=i)
        records.append({
            "date_id": i + 1,
            "day": current_date.day,
            "month": current_date.strftime("%B"),
            "year": current_date.year,
            "quarter": f"Q{((current_date.month - 1) // 3) + 1}",
            "weekday": current_date.strftime("%A"),
        })
    return records


def write_clean_dates() -> None:
    """
    Writes a clean CSV file of 365 valid date records.
    """
    file_path = output_dir / "dates_clean.csv"
    records = generate_clean_dates(datetime(2023, 1, 1), 365)
    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in records:
            writer.writerow(row)


def generate_messy_date(date_id: int, base_date: datetime) -> dict:
    """
    Generate a date record with an intentional corruption.
    Args:
        date_id (int): Unique ID.
        base_date (datetime): Reference date to manipulate.
    Returns:
        dict: Corrupted date record.
    """
    row = {
        "date_id": date_id,
        "day": base_date.day,
        "month": base_date.strftime("%B"),
        "year": base_date.year,
        "quarter": f"Q{((base_date.month - 1) // 3) + 1}",
        "weekday": base_date.strftime("%A"),
    }

    corruption_type = date_id % 6  # Rotate between types

    if corruption_type == 0:
        row["month"] = "07"  # numeric instead of full name
    elif corruption_type == 1:
        row["quarter"] = "Q5"  # invalid quarter
    elif corruption_type == 2:
        row["weekday"] = "Fridday"  # typo
    elif corruption_type == 3:
        row["day"] = ""  # missing value
    elif corruption_type == 4:
        row["extra_column"] = "calendar glitch"  # extra column
    elif corruption_type == 5:
        row["month"] = row["month"].lower()  # case sensitivity issue

    return row


def write_messy_dates() -> None:
    """
    Writes a messy CSV file with 100 intentionally corrupted date records.
    """
    file_path = output_dir / "dates_messy.csv"
    all_columns = columns + ["extra_column"]
    start_date = datetime(2023, 1, 1)

    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_columns, extrasaction="ignore")
        writer.writeheader()
        for i in range(1, 101):
            base_date = start_date + timedelta(days=i)
            writer.writerow(generate_messy_date(i, base_date))


if __name__ == "__main__":
    write_clean_dates()
    write_messy_dates()