-- 1. Monthly revenue by category
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


-- 2. Region-wise total revenue and order count
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
    COUNT(o.order_id) AS n_orders
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY revenue DESC;


-- 3. Top resellers by total spend
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


-- 4. Resellers who have never placed an order
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
GROUP BY r.reseller_id, r.reseller_name, r.region
HAVING COUNT(o.order_id) = 0;

-- For RS024, COUNT(*) = 1 because LEFT JOIN creates
-- one NULL unmatched row, while COUNT(order_id) = 0.
-- Therefore COUNT(order_id), not COUNT(*), should be
-- used to detect a reseller with zero orders.


-- 5. Average Order Value for June, Delivered orders only
SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';