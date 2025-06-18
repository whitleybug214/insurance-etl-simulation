# claims_fact Star Schema

This star schema models insurance claim submissions. The central `claims_fact` table captures each claim event, and is joined to supporting dimension tables for customers, policies, dates, and adjusters.

_Star schema diagram will be added here in future iterations._

## Fact Table: `claims_fact`

| Column         | Type     | Description                          |
|----------------|----------|--------------------------------------|
| `claim_id`     | INT (PK) | Unique ID for the claim              |
| `customer_id`  | INT (FK) | Foreign key to `customers_dim`       |
| `policy_id`    | INT (FK) | Foreign key to `policies_dim`        |
| `date_id`      | INT (FK) | Foreign key to `dates_dim`           |
| `adjuster_id`  | INT (FK) | Foreign key to `adjusters_dim`       |
| `amount`       | FLOAT    | Dollar amount of the claim           |
| `status`       | TEXT     | Claim status (Approved / Denied etc) |

## Dimension Table: `customers_dim`

| Column         | Type     | Description               |
|----------------|----------|---------------------------|
| `customer_id`  | INT (PK) | Unique customer identifier         |
| `first_name`   | TEXT     | Customer’s first name              |
| `last_name`    | TEXT     | Customer’s last name               |
| `birth_date`   | DATE     | Date of birth                      |
| `gender`       | TEXT     | M / F / Other                      |
| `email`        | TEXT     | Email address                      |
| `phone_number` | TEXT     | Contact number                     |
| `region`       | TEXT     | Geographic region (e.g. Northeast) |
| `risk_score`   | FLOAT    | Internal score for insurance risk  |

## Dimension Table: `policies_dim`

| Column        | Type     | Description          |
|---------------|----------|----------------------|
| `policy_id`   | INT (PK) | Unique policy ID     |
| `policy_type` | TEXT     | Auto/Home/Life/etc.  |
| `start_date`  | DATE     | Start of policy term |
| `end_date`    | DATE     | End of policy term   |
| `premium`     | FLOAT    | Monthly or annual premium paid |

## Dimension Table: `dates_dim`

| Column    | Type     | Description        |
|-----------|----------|--------------------|
| `date_id` | INT (PK) | Unique date ID     |
| `day`     | INT      | 1-31               |
| `month`   | TEXT     | January-December   |
| `year`    | INT      | 2025, etc.         |
| `quarter` | TEXT     | Q1-Q4              |
| `weekday` | TEXT     | Monday, Tuesday... |

## Dimension Table: `adjusters_dim`

| Column        | Type     | Description          |
|---------------|----------|----------------------|
| `adjuster_id` | INT (PK) | Unique adjuster ID   |
| `name`        | TEXT     | Adjuster's full name |
| `region`      | TEXT     | Their service area   |
| `team_lead`   | TEXT     | Supervisor name or ID |

### Notes:
- All foreign key IDs in the fact table must match existing rows in their dimension tables.
- `risk_score` is simulated and not derived from real models.
- Future versions may include claim types, payout timelines, or fraud risk indicators.