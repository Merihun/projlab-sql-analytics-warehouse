-- Step "Build the customers staging view".
-- Worked example: the names are already trimmed. Finish the other columns.
CREATE SCHEMA IF NOT EXISTS stg;
CREATE OR REPLACE VIEW stg.customers AS
SELECT customer_id,
       email,                                   -- TODO trim and lower-case
       trim(first_name) AS first_name,
       trim(last_name)  AS last_name,
       country_code,                            -- TODO trim and upper-case
       signup_date                              -- TODO parse both formats into a DATE
       -- TODO is_valid_email (never null)
FROM raw.customers;
