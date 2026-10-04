import sqlite3
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "Data", "meesho_reseller.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 1. Monthly revenue by category
query1 = """
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY
    CASE month
        WHEN 'April' THEN 1
        WHEN 'May' THEN 2
        WHEN 'June' THEN 3
    END,
    CASE category
        WHEN 'Ethnic Wear' THEN 1
        WHEN 'Western Wear' THEN 2
        WHEN 'Kids Wear' THEN 3
        WHEN 'Home & Kitchen' THEN 4
        WHEN 'Beauty & Personal Care' THEN 5
    END;
"""

# 2. Region-wise revenue and order count
query2 = """
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
    COUNT(o.order_id) AS n_orders
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY revenue DESC;
"""

# 3. Top resellers by total spend
query3 = """
SELECT
    r.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;
"""

# 4. Resellers who have never placed an order
query4 = """
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
GROUP BY r.reseller_id, r.reseller_name, r.region
HAVING COUNT(o.order_id) = 0;
"""

# 5. AOV for June, Delivered orders only
query5 = """
SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
"""


def save_csv(filename, query):
    cur.execute(query)
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]

    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)

    print(f"Created: {filename} ({len(rows)} rows)")


save_csv("monthly_category_revenue.csv", query1)
save_csv("region_revenue.csv", query2)
save_csv("top_resellers.csv", query3)
save_csv("zero_order_resellers.csv", query4)
save_csv("june_aov.csv", query5)

# Extra check for COUNT(*) vs COUNT(order_id)
check_query = """
SELECT
    r.reseller_id,
    r.reseller_name,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id, r.reseller_name;
"""

cur.execute(check_query)
print("\nCOUNT(*) vs COUNT(order_id) for RS024:")
print(cur.fetchone())

conn.close()

print("\nAll 5 queries completed successfully!")