"""Generate fictional CRM and ERP data with stable keys and known edge cases."""

import argparse
import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 20260927
AS_OF = date(2026, 9, 1)
ACCOUNTS = [
    ("A001", "Aster Medical", "Healthcare"),
    ("A002", "Blue Peak Retail", "Retail"),
    ("A003", "Cedar Industrial", "Manufacturing"),
    ("A004", "Delta Foods", "Food"),
    ("A005", "Evergreen Transit", "Transport"),
    ("A006", "Fable Energy", "Energy"),
]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def generate(output: Path, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    accounts = [
        {"account_id": key, "account_name": name, "industry": industry,
         "sales_rep_id": f"R{(i % 3) + 1:03d}"}
        for i, (key, name, industry) in enumerate(ACCOUNTS)
    ]
    reps = [
        {"sales_rep_id": "R001", "sales_rep_name": "Maya Chen"},
        {"sales_rep_id": "R002", "sales_rep_name": "Noah Patel"},
        {"sales_rep_id": "R003", "sales_rep_name": "Amira Diallo"},
    ]
    opportunities, invoices, shipments = [], [], []
    for i, account in enumerate(accounts):
        aid = account["account_id"]
        for j in range(2):
            opportunities.append({
                "opportunity_id": f"O{i * 2 + j + 1:03d}", "account_id": aid,
                "opportunity_name": f"{account['account_name']} expansion {j + 1}",
                "stage": ["Discovery", "Proposal", "Negotiation", "Closed Won"][((i + j) % 4)],
                "amount_usd": 10000 + rng.randrange(5, 45) * 1000,
                "close_date": (AS_OF + timedelta(days=15 + i * 9 + j * 12)).isoformat(),
            })
        for j in range(2):
            amount = 4000 + rng.randrange(2, 20) * 500
            due = AS_OF + timedelta(days=i * 5 + j * 15 - 20)
            paid = (i + j) % 3 != 0
            invoices.append({
                "invoice_id": f"I{i * 2 + j + 1:03d}", "account_id": aid,
                "invoice_date": (due - timedelta(days=30)).isoformat(),
                "due_date": due.isoformat(), "amount_usd": amount,
                "paid_amount_usd": amount if paid else 0,
            })
            shipments.append({
                "shipment_id": f"S{i * 2 + j + 1:03d}", "account_id": aid,
                "promised_date": (AS_OF + timedelta(days=i * 3 + j * 7)).isoformat(),
                "delivered_date": (AS_OF + timedelta(days=i * 3 + j * 7 + (5 if i == 2 else -1))).isoformat(),
                "status": "Late" if i == 2 else "On Time",
            })
    tables = {"accounts": accounts, "sales_reps": reps, "opportunities": opportunities,
              "invoices": invoices, "shipments": shipments}
    for name, rows in tables.items():
        write_csv(output / f"{name}.csv", rows)
    expected = {
        "seed": seed, "as_of_date": AS_OF.isoformat(),
        "row_counts": {name: len(rows) for name, rows in tables.items()},
        "open_pipeline_usd": sum(o["amount_usd"] for o in opportunities if o["stage"] != "Closed Won"),
        "outstanding_ar_usd": sum(i["amount_usd"] - i["paid_amount_usd"] for i in invoices),
        "late_shipments": sum(s["status"] == "Late" for s in shipments),
    }
    (output / "expected_results.json").write_text(json.dumps(expected, indent=2) + "\n")
    return expected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/generated"))
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    print(json.dumps(generate(args.output, args.seed), indent=2))


if __name__ == "__main__":
    main()
