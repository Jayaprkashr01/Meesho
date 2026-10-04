import csv


def mom_growth(previous: float, current: float) -> float:
    """
    Calculate Month-on-Month growth percentage.
    """
    return round((current - previous) / previous * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    """
    Classify growth based on the threshold.
    """
    if abs(mom_pct) > threshold:
        return "flagged"
    elif abs(mom_pct) < threshold:
        return "not_flagged"
    else:
        return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    """
    Validate a month,category,revenue,n_orders CSV feed.
    """
    errors = []

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for line_number, row in enumerate(reader, start=2):
            month = row.get("month", "")
            category = row.get("category", "")
            revenue = row.get("revenue", "")

            # Missing category
            if not category.strip():
                errors.append(
                    f"line {line_number}: missing category (month={month})"
                )
                continue

            # Missing revenue
            if not revenue.strip():
                errors.append(
                    f"line {line_number}: missing revenue (category={category})"
                )
                continue

            # Revenue not numeric
            try:
                revenue_value = float(revenue)
            except ValueError:
                errors.append(
                    f"line {line_number}: revenue not numeric: {revenue!r}"
                )
                continue

            # Negative revenue
            if revenue_value < 0:
                errors.append(
                    f"line {line_number}: negative revenue ({revenue_value}) "
                    f"for category={category}"
                )

    return (len(errors) == 0, errors)