# Solution 00 — Synthetic enterprise foundation

This solution runs locally without a Snowflake account. Every name and amount is fictional. The fixed seed and as-of date make the sample reproducible.

## Run

From the repository root:

```sh
uv sync --frozen
uv run generate-demo-data
uv run streamlit run app.py
```

Open the local URL shown by Streamlit. Select an account and inspect its opportunities, invoices, shipments, and business definitions.

## Check the result

The generator prints the expected row counts and three aggregate metrics. Compare them with `data/generated/expected_results.json`. The same CSVs are used by later solutions.

## Data contract

- Each key is unique within its table.
- Every `account_id` in a child table exists in `accounts.csv`.
- Invoice outstanding balance is `amount_usd - paid_amount_usd`.
- Opportunity stage `Closed Won` is excluded from open pipeline.
- The `as_of_date` is fixed at 2026-09-01; it does not depend on the reader's clock.

Next: load the CSVs into Snowflake and create governed business semantics. This repository does not claim the local UI is already connected to Snowflake.
