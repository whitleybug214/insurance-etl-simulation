import csv
import random
from faker import Faker
from pathlib import Path
from datetime import datetime, timedelta
from etl.schema_definition import policies_schema

"""
Generates both clean and intentionally messy synthetic policy records for use in the insurance ETL simulation project.

Outputs:
- policies_clean.csv: realistic, valid customer data
- policies_messy.csv: includes corruptions for testing data cleaning and validation

Run from the project root using:
    python -m scripts.generate_policies
"""
random.seed(42)
Faker.seed(42)

fake = Faker()
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

columns = [
    "policy_id",
    "policy_type",
    "start_date",
    "end_date",
    "premium",
]

def generate_clean_policy(policy_id: int) -> dict:
    """
    Generates a single valid policy record using Faker.
    Args:
        policy_id (int): Unique ID for the policy.
    Returns:
        dict: A clean policy record.
    """
    start_date_obj = fake.date_between(start_date='-3y', end_date='today')
    end_date_obj = start_date_obj + timedelta(days=random.randint(90, 1095))

    return {
        "policy_id": policy_id,
        "policy_type": random.choice(["life", "auto", "house", "travel", "health", "pet"]),
        "start_date": start_date_obj.isoformat(),
        "end_date": end_date_obj.isoformat(),
        "premium": round(random.uniform(40.0, 300.0), 2),
    }

def write_clean_policies(num_rows: int) -> None:
    """
    Writes a CSV of clean policy records to data/raw/policies_clean.csv.
    Args:
        num_rows (int): Number of rows to generate.
    """

    file_path = output_dir / "policies_clean.csv"
    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for i in range(1, num_rows + 1):
            writer.writerow(generate_clean_policy(i))

def generate_messy_policy(policy_id: int) -> dict:
    """
    Generates a policy record with a random intentional corruption.
    Corruption types include missing values, invalid date format,
    end date before start date, non-numeric premiums, unknown policy types and added extra columns.
    Args:
        policy_id (int): Nominal ID to assign to the policy.
    Returns:
        dict: A corrupted policy record.
    """

    row = generate_clean_policy(policy_id)
    corruption_type = random.choice([
        "missing_value",
        "invalid_date_format",
        "extra_column",
        "end_before_start_date",
        "non_numeric_premium",
        "unknown_policy_type",
    ])

    start_date_obj = fake.date_between(start_date='-3y', end_date='today')
    end_date_obj = start_date_obj + timedelta(days=random.randint(90, 1095))

    if corruption_type == "missing_value":
        row["policy_type"] = ""

    elif corruption_type == "invalid_date_format":
        row["start_date"] = "March 15, 2022"

    elif corruption_type == "extra_column":
        row["agent_notes"] = "Loyal customer"

    elif corruption_type == "end_before_start_date":
        row["start_date"] = end_date_obj.isoformat()
        row["end_date"] = start_date_obj.isoformat()

    elif corruption_type == "non_numeric_premium":
        row["premium"] = "discount"

    elif corruption_type == "unknown_policy_type":
        row["policy_type"] = "magic"

    return row

def write_messy_policies(num_rows: int) -> None:
    """
    Writes a CSV of messy policy records to data/raw/policies_messy.csv.
    Args:
        num_rows (int): Number of rows to generate.
    """

    file_path = output_dir / "policies_messy.csv"
    all_columns = list(policies_schema.keys()) + ["notes"]  # handles extra column
    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_columns, extrasaction="ignore")
        writer.writeheader()
        for i in range(1, num_rows + 1):
            writer.writerow(generate_messy_policy(i))

if __name__ == "__main__":
    write_clean_policies(400)
    write_messy_policies(150)