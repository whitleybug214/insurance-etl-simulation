"""
Defines the expected schema for each table in the simulated insurance data pipeline.
Each schema is represented as a dictionary mapping column names to expected Python types.

These schemas can be reused for:
- Validating raw and transformed data
- Guiding data generation logic
- Maintaining consistent structure across ETL steps
"""

SchemaType = dict[str, type]

claims_fact_schema = {
    "claim_id": int,
    "customer_id": int,
    "policy_id": int,
    "date_id": int,
    "adjuster_id": int,
    "amount": float,
    "status": str,
}

customers_schema = {
    "customer_id": int,
    "first_name": str,
    "last_name": str,
    "birth_date": str,
    "gender": str,
    "email": str,
    "phone_number": str,
    "region": str,
    "risk_score": float
}

policies_schema = {
    "policy_id": int,
    "policy_type": str,
    "start_date": str,
    "end_date": str,
    "premium": float,
}

dates_schema = {
    "date_id": int,
    "day": int,
    "month": str,
    "year": int,
    "quarter": str,
    "weekday": str,
}

adjusters_schema = {
    "adjuster_id": int,
    "name": str,
    "region": str,
    "team_lead_id": int,
}

schemas = {
    "claims_fact": claims_fact_schema,
    "customers_dim": customers_schema,
    "policies_dim": policies_schema,
    "dates_dim": dates_schema,
    "adjusters_dim": adjusters_schema,
}
