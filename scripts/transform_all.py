from scripts import (
    transform_customers,
    transform_policies,
    transform_dates,
    transform_adjusters,
    transform_claims
)

def main():
    transform_customers.main()
    transform_policies.main()
    transform_dates.main()
    transform_adjusters.main()
    transform_claims.main()

if __name__ == "__main__":
    main()