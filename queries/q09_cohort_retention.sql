-- Retention by first-order month (cohort) and months since the first order.
-- Columns: cohort_month, months_since, active_customers, retention
-- Revenue excludes cancelled orders.
WITH activity AS (
  SELECT DISTINCT f.customer_key, date_trunc('month', d.full_date) AS month_start
  FROM wh.fact_order_line f JOIN wh.dim_date d ON d.date_key = f.order_date_key
  WHERE f.order_status <> 'cancelled' AND f.customer_key <> -1)
-- TODO cohorts, counts, retention
SELECT * FROM activity;
