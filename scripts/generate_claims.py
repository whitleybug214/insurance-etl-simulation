import csv
import random
from faker import Faker
from pathlib import Path
from etl.schema_definition import claims_fact_schema
import time
import logging

"""
Generates clean and messy insurance claims for the ETL pipeline simulation.
Outputs:
- claims_clean.csv
- claims_messy.csv
Run from the project root using:
    python -m scripts.generate_claims
"""

random.seed(42)
fake=Faker()

customer_ids = list(range(1, 801))
policy_ids = list(range(1, 551))
adjuster_ids = list(range(1, 101))
date_ids = list(range(1, 366))
statuses = ["Approved", "Denied", "Pending"]

output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

columns = list(claims_fact_schema.keys())

def generate_clean_claim(claim_id: int) -> dict:
    """
    Generate a clean insurance claim record.
    Args:
        claim_id (int): Unique claim ID
    Returns:
        dict: Clean claim data
    """
    return {
        "claim_id": claim_id,
        "customer_id": random.choice(customer_ids),
        "policy_id": random.choice(policy_ids),
        "adjuster_id": random.choice(adjuster_ids),
        "date_id": random.choice(date_ids),
        "amount": round(random.uniform(100.0, 10000.0), 2),
        "status": random.choice(statuses),
    }

def write_clean_claims(num_rows: int) -> None:
    """
    Write clean claims to CSV.
    Args:
        num_rows (int): Number of rows to generate
    """
    filepath = output_dir / "claims_clean.csv"
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for i in range(1, num_rows + 1):
            writer.writerow(generate_clean_claim(i))

def generate_messy_claim(claim_id: int) -> dict:
    """
        Generate a corrupted insurance claim for testing.
        Args:
            claim_id (int): Nominal claim ID
        Returns:
            dict: Messy claim row with injected error
        """
    row = generate_clean_claim(claim_id)
    corruption_type = random.choice([
        "missing_amount",
        "negative_amount",
        "invalid_status",
        "foreign_key_violation_customer",
        "foreign_key_violation_policy",
        "foreign_key_violation_date",
        "foreign_key_violation_adjuster",
        "extra_column"
    ])

    if corruption_type == "missing_amount":
        row["amount"] = ""

    elif corruption_type == "negative_amount":
        row["amount"] = -500.00

    elif corruption_type == "invalid_status":
        row["status"] = "In Progress"

    elif corruption_type == "foreign_key_violation_customer":
        row["customer_id"] = 999999  # unlikely to exist

    elif corruption_type == "foreign_key_violation_policy":
        row["policy_id"] = 888888

    elif corruption_type == "foreign_key_violation_date":
        row["date_id"] = 777777

    elif corruption_type == "foreign_key_violation_adjuster":
        row["adjuster_id"] = 666666

    elif corruption_type == "extra_column":
        row["notes"] = "Urgent payout requested"

    return row

def write_messy_claims(num_rows: int) -> None:
    """
        Write messy claims to CSV with intentional errors.
        Args:
            num_rows (int): Number of rows to generate
        """
    all_columns = columns + ["notes"]
    filepath = output_dir / "claims_messy.csv"
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_columns, extrasaction="ignore")
        writer.writeheader()
        for i in range(1, num_rows + 1):
            writer.writerow(generate_messy_claim(i))

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

if __name__ == "__main__":
    t0 = time.perf_counter()
    write_clean_claims(50000)
    t1 = time.perf_counter()
    logging.info(f"Clean claims generated in {t1 - t0:.2f} seconds")

    t2 = time.perf_counter()
    write_messy_claims(250)
    t3 = time.perf_counter()
    logging.info(f"Messy claims generated in {t3 - t2:.2f} seconds")