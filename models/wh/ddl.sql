-- Step "Write the star schema DDL".
CREATE SCHEMA IF NOT EXISTS wh;

CREATE OR REPLACE TABLE wh.dim_customer (
  customer_key BIGINT PRIMARY KEY, customer_id INTEGER, full_name VARCHAR,
  email VARCHAR, is_valid_email BOOLEAN, country_code VARCHAR, signup_date DATE);

-- TODO wh.dim_product: product_key BIGINT PRIMARY KEY, product_id INTEGER,
--      sku, product_name and category_name as VARCHAR

-- Grain: ...
-- TODO wh.fact_order_line: order_line_id and order_id INTEGER; customer_key and product_key BIGINT NOT NULL;
--      order_date_key INTEGER NOT NULL; order_status and channel VARCHAR; quantity INTEGER;
--      net_amount DECIMAL(18,2)
