-- Step "Measure nulls, invalid emails and orphans".
-- Goal: profile.defects(check_name, failing_rows) with five checks. Two are done; add the other three.
-- An email is valid when, trimmed and lower-cased, it matches:  ^[^@\s]+@[^@\s]+\.[a-z]{2,}$
CREATE SCHEMA IF NOT EXISTS profile;
CREATE OR REPLACE TABLE profile.defects AS
SELECT 'null_email' AS check_name, COUNT(*) AS failing_rows
FROM raw.customers WHERE email IS NULL
UNION ALL
SELECT 'invalid_email', COUNT(*) FROM raw.customers
WHERE email IS NOT NULL
  AND NOT regexp_matches(lower(trim(email)), '^[^@\s]+@[^@\s]+\.[a-z]{2,}$')
-- TODO UNION ALL: orphan_line_product, orphan_line_order, unparseable_signup_date
;
