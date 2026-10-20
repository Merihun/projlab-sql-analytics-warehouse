-- Top 3 products per category per month, ties broken by product_id.
-- Columns: year_month, category_name, product_id, revenue, rank_in_category
-- Revenue excludes cancelled orders.
WITH monthly AS (
  SELECT d.year_month, p.category_name, p.product_id, SUM(f.net_amount) AS revenue
  FROM wh.fact_order_line f
  JOIN wh.dim_date d ON d.date_key = f.order_date_key
  JOIN wh.dim_product p ON p.product_key = f.product_key
  WHERE f.order_status <> 'cancelled' AND f.product_key <> -1
  GROUP BY 1, 2, 3
)
-- TODO: rank products inside each month and category, keep the top three
SELECT * FROM monthly;
