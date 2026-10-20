# SQL Analytics Warehouse: what this starter gives you

This folder is your ProjLabs lab with the Fernhill project's starter files added. Everything runs on your
own computer and needs no account anywhere.

| Provided | What it is |
|----------|------------|
| `fernhill_shop/` | The shop database export (six tables, generated) and a small runner for SQL files. You do not change it. |
| `profiling/`, `models/`, `queries/` | One SQL file per step, with the worked examples the steps mention and a TODO for the rest. |
| `.sqlfluff` | The style settings for `sqlfluff lint models queries`. |

## Create the database

Once, in a terminal in this folder (in the Docker lab: `docker compose exec workspace bash` first):

    python -m fernhill_shop load

It writes the export to `data/raw/` and creates `fernhill.db` with the schema `raw`: customers (20,000),
products (1,200), categories (40), orders (90,000), order_lines (250,000) and payments (90,000). Both are
git-ignored: you commit the SQL that builds the warehouse, not the data.

## Run your SQL

    python -m fernhill_shop run profiling/01_tables.sql        run a file; prints the last result
    python -m fernhill_shop query "SELECT * FROM profile.tables ORDER BY table_name"
    python -m fernhill_shop run queries/q06_top_products.sql --timer
    python -m fernhill_shop build                               load, then run profiling/ and models/ in order

`build` runs these files in this order, which is also the order of the steps:
`profiling/01_tables.sql`, `profiling/02_defects.sql`, `models/stg/customers.sql`, `models/stg/orders.sql`,
`models/wh/ddl.sql`, `models/wh/dim_date.sql`, `models/wh/load_dimensions.sql`, `models/wh/load_fact.sql`.
Keep those file names. Each file in `queries/` holds one `SELECT` statement.

If you have the DuckDB command line installed, `duckdb fernhill.db` opens the same database.
