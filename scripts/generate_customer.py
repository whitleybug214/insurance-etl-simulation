import csv
import random
from faker import Faker
from pathlib import Path

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
    return {
        "customer_id": customer_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
        "gender": random.choice(["M", "F", "Other"]),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "region": random.choice("Northeast", "Southeast", "Midwest", "Southwest", "West"),
        "risk_score": round(random.uniform(1.0, 5.0), 2),
    }

def write_clean_customers(num_rows: int) -> None:
    filepath = output_dir / "customers_clean.csv"
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for i in range(1, num_rows+1):
            writer.writerow(generate_clean_customer(i))

if __name__ == "__main__":
    write_clean_customers(800)