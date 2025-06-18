# claims_fact Star Schema

This star schema models insurance claim submissions. The central `claims_fact` table captures each claim event, and is joined to supporting dimension tables for customers, policies, dates, and adjusters.
