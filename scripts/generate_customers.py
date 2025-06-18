import csv
import random
from faker import Faker
from pathlib import Path
from etl.schema_definition import customers_schema

"""
Generates both clean and intentionally messy synthetic customer records for use in the insurance ETL simulation project.

Outputs:
- customers_clean.csv: realistic, valid customer data
- customers_messy.csv: includes corruptions for testing data cleaning and validation

Run from the project root using:
    python -m scripts.generate_customers
"""

fake = Faker()
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

columns = [
    "customer_id",
    "first_name",
    "last_name",
    "birth_date",
    "gender",
    "email",
    "phone_number",
    "region",
    "risk_score"
]


def generate_clean_customer(customer_id: int) -> dict:
    """
    Generates a single valid customer record using Faker.
    Args:
        customer_id (int): Unique ID for the customer.
    Returns:
        dict: A clean customer record.
    """
    return {
        "customer_id": customer_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
        "gender": random.choice(["M", "F", "Other"]),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "region": random.choice(["Northeast", "Southeast", "Midwest", "Southwest", "West"]),
        "risk_score": round(random.uniform(1.0, 5.0), 2),
    }


def write_clean_customers(num_rows: int) -> None:
    """
    Writes a CSV of clean customer records to data/raw/customers_clean.csv.
    Args:
        num_rows (int): Number of rows to generate.
    """
    filepath = output_dir / "customers_clean.csv"
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for i in range(1, num_rows + 1):
            writer.writerow(generate_clean_customer(i))


def generate_messy_customer(customer_id: int) -> dict:
    """
    Generates a customer record with a random intentional corruption.
    Corruption types include missing values, formatting errors, invalid categories,
    duplicate IDs, and added extra columns.
    Args:
        customer_id (int): Nominal ID to assign to the customer.
    Returns:
        dict: A corrupted customer record.
    """
    row = generate_clean_customer(customer_id)
    corruption_type = random.choice([
        "missing_value",
        "invalid_format",
        "extra_column",
        "wrong_gender",
        "duplicate_id",
        "null_risk_score",
    ])

    if corruption_type == "missing_value":
        row["email"] = ""  # remove email

    elif corruption_type == "invalid_format":
        row["birth_date"] = "April 18th, 1992"  # wrong format

    elif corruption_type == "extra_column":
        row["notes"] = "Preferred customer"  # will become an extra column

    elif corruption_type == "wrong_gender":
        row["gender"] = "X"  # not a valid option

    elif corruption_type == "duplicate_id":
        row["customer_id"] = 1  # intentionally duplicate

    elif corruption_type == "null_risk_score":
        row["risk_score"] = ""  # missing numeric value

    return row


def write_messy_customers(num_rows: int) -> None:
    """
    Writes a CSV of intentionally corrupted customer records to data/raw/customers_messy.csv.
    Args:
        num_rows (int): Number of rows to generate.
    """
    filepath = output_dir / "customers_messy.csv"
    all_columns = list(customers_schema.keys()) + ["notes"]  # handles extra column
    with open(filepath, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_columns, extrasaction="ignore")
        writer.writeheader()
        for i in range(1, num_rows + 1):
            writer.writerow(generate_messy_customer(i))


if __name__ == "__main__":
    write_clean_customers(800)
    write_messy_customers(200)
