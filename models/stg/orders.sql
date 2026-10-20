-- Step "Build orders, order lines and products staging".
-- stg.orders is provided. Add stg.order_lines and stg.products below it.
CREATE SCHEMA IF NOT EXISTS stg;
CREATE OR REPLACE VIEW stg.orders AS
SELECT order_id, customer_id, CAST(order_ts AS TIMESTAMP) AS order_ts,
       lower(status) AS status, lower(channel) AS channel
FROM raw.orders;

-- TODO stg.order_lines: every raw line, plus net_amount and is_orphan_product (LEFT JOIN raw.products)

-- TODO stg.products: every raw product with its category_name (LEFT JOIN raw.categories)
