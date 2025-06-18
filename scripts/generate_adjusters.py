import csv
import random
from faker import Faker
from pathlib import Path
from etl.schema_definition import adjusters_schema

"""
Generates clean and messy adjuster records for the ETL pipeline simulation.

Outputs:
- adjusters_clean.csv
- adjusters_messy.csv

Run from the project root using:
    python -m scripts.generate_adjusters
"""

random.seed(42)
Faker.seed(42)

fake = Faker()
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

columns = list(adjusters_schema.keys())


def generate_clean_adjuster(adjuster_id: int) -> dict:
    return {
        "adjuster_id": adjuster_id,
        "name": fake.name(),
        "region": random.choice(["Northeast", "Southeast", "Midwest", "Southwest", "West"]),
        "team_lead_id": random.randint(1, 10),
    }


def write_clean_adjusters(num_rows: int) -> None:
    file_path = output_dir / "adjusters_clean.csv"
    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for i in range(1, num_rows + 1):
            writer.writerow(generate_clean_adjuster(i))


def generate_messy_adjuster(adjuster_id: int) -> dict:
    row = generate_clean_adjuster(adjuster_id)
    corruption_type = random.choice([
        "missing_name",
        "invalid_region",
        "non_numeric_id",
        "extra_column",
        "extra_whitespace",
        "region_case_sensitivity",
    ])

    if corruption_type == "missing_name":
        row["name"] = ""

    elif corruption_type == "invalid_region":
        row["region"] = "Atlantis"

    elif corruption_type == "non_numeric_id":
        row["adjuster_id"] = "A-XYZ"

    elif corruption_type == "extra_column":
        row["team_notes"] = "Temp contract"

    elif corruption_type == "extra_whitespace":
        row["name"] = fake.name() + "    "

    elif corruption_type == "region_case_sensitivity":
        row["region"] = "northeast"

    return row


def write_messy_adjusters(num_rows: int) -> None:
    all_columns = columns + ["team_notes"]  # for extra column
    file_path = output_dir / "adjusters_messy.csv"
    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_columns, extrasaction="ignore")
        writer.writeheader()
        for i in range(1, num_rows + 1):
            writer.writerow(generate_messy_adjuster(i))


if __name__ == "__main__":
    write_clean_adjusters(100)
    write_messy_adjusters(30)