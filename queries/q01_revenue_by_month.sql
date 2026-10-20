-- Revenue by month.
-- Columns: year_month, revenue
-- Revenue excludes cancelled orders.
-- Worked example: run it, then use its shape for q02 to q05.
SELECT d.year_month, SUM(f.net_amount) AS revenue
FROM wh.fact_order_line f
JOIN wh.dim_date d ON d.date_key = f.order_date_key
WHERE f.order_status <> 'cancelled'
GROUP BY d.year_month
ORDER BY d.year_month;
