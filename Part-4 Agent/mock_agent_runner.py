import csv
import json
import os
import sys

# Allow importing Part 2 even though the folder name contains a hyphen.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PART2_DIR = os.path.join(PROJECT_ROOT, "part-2 engine")

if PART2_DIR not in sys.path:
    sys.path.insert(0, PART2_DIR)

from growth_engine import validate_feed, mom_growth, is_flagged


def load_feed(csv_path):
    """Load month/category/revenue/n_orders CSV into a dictionary."""
    data = {}

    with open(csv_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            category = row["category"].strip()
            revenue = float(row["revenue"])

            data[category] = {
                "revenue": revenue,
                "n_orders": int(row["n_orders"]) if row["n_orders"] else 0
            }

    return data


def build_message(category, previous_revenue, current_revenue, mom_pct,
                  month, previous_month):
    """Part 3-style Context -> Insight -> Implication draft."""

    return (
        f"Context: {category} revenue is being monitored for "
        f"{month} versus {previous_month}. "
        f"Insight: Fact — {category} recorded a MoM change of {mom_pct}%. "
        f"Implication: Hypothesis — review the category's recent sales movement, "
        f"pricing, promotions and availability before approving any action."
    )


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:

    # ---------------------------------------------------------
    # 1. Validate current feed
    # ---------------------------------------------------------
    valid, errors = validate_feed(current_month_csv)

    if not valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop"
        }

    # ---------------------------------------------------------
    # 2. Load valid feeds
    # ---------------------------------------------------------
    previous_data = load_feed(previous_month_csv)
    current_data = load_feed(current_month_csv)

    flagged = []
    suppressed = []
    escalated = []

    # ---------------------------------------------------------
    # 3. Calculate MoM for every category
    # 4. Run is_flagged()
    # ---------------------------------------------------------
    for category, current_info in current_data.items():

        if category not in previous_data:
            continue

        previous_revenue = previous_data[category]["revenue"]
        current_revenue = current_info["revenue"]

        mom_pct = mom_growth(previous_revenue, current_revenue)
        status = is_flagged(mom_pct)

        if status == "flagged":

            flagged.append({
                "category": category,
                "mom_pct": mom_pct,
                "previous_revenue": previous_revenue,
                "current_revenue": current_revenue,
                "drafted": False
            })

        elif status == "escalate_exact_boundary":

            escalated.append(category)

    # ---------------------------------------------------------
    # 5. Sort flagged categories by absolute growth
    # ---------------------------------------------------------
    flagged.sort(key=lambda item: abs(item["mom_pct"]), reverse=True)

    # ---------------------------------------------------------
    # 6. Draft messages for top 3
    # ---------------------------------------------------------
    for item in flagged[:3]:

        item["drafted"] = True

        item["message"] = build_message(
            item["category"],
            item["previous_revenue"],
            item["current_revenue"],
            item["mom_pct"],
            month,
            month_name_before(month)
        )

    # ---------------------------------------------------------
    # 7. Suppress remaining flagged categories
    # ---------------------------------------------------------
    for item in flagged[3:]:
        suppressed.append(item["category"])

    # Only drafted categories appear in flagged_categories output.
    drafted_categories = flagged[:3]

    # ---------------------------------------------------------
    # 8. Structured JSON output
    # ---------------------------------------------------------
    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": drafted_categories,
        "suppressed_categories": suppressed,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval"
    }


def month_name_before(month):
    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    if month not in months:
        return ""

    index = months.index(month)

    if index == 0:
        return "December"

    return months[index - 1]


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print(
            "Usage: python mock_agent_runner.py "
            "<month> <previous_month_csv> <current_month_csv>"
        )
        sys.exit(1)

    result = run(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3]
    )

    print(json.dumps(result, indent=2))