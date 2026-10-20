"""Load the export into DuckDB and run SQL files against it."""

from __future__ import annotations

import time
from pathlib import Path

import duckdb

from fernhill_shop import data

DATABASE = "fernhill.db"
RAW_DIR = "data/raw"
# The column types of the export, as the shop database declares them. signup_date is text on purpose.
TYPES = {
    "customers": {"customer_id": "INTEGER", "email": "VARCHAR", "first_name": "VARCHAR", "last_name": "VARCHAR",
                  "country_code": "VARCHAR", "signup_date": "VARCHAR"},
    "categories": {"category_id": "INTEGER", "category_name": "VARCHAR"},
    "products": {"product_id": "INTEGER", "sku": "VARCHAR", "product_name": "VARCHAR", "category_id": "INTEGER",
                 "list_price": "DECIMAL(10,2)"},
    "orders": {"order_id": "INTEGER", "customer_id": "INTEGER", "order_ts": "TIMESTAMP", "status": "VARCHAR",
               "channel": "VARCHAR"},
    "order_lines": {"order_line_id": "INTEGER", "order_id": "INTEGER", "product_id": "INTEGER",
                    "quantity": "INTEGER", "unit_price": "DECIMAL(10,2)", "discount_amount": "DECIMAL(10,2)"},
    "payments": {"payment_id": "INTEGER", "order_id": "INTEGER", "method": "VARCHAR", "amount": "DECIMAL(10,2)",
                 "paid_at": "TIMESTAMP"},
}  # fmt: skip
# The order `build` runs your files in. A file that is still only comments is skipped.
BUILD_ORDER = (
    "profiling/01_tables.sql",
    "profiling/02_defects.sql",
    "models/stg/customers.sql",
    "models/stg/orders.sql",
    "models/wh/ddl.sql",
    "models/wh/dim_date.sql",
    "models/wh/load_dimensions.sql",
    "models/wh/load_fact.sql",
)


def connect(database: str = DATABASE) -> duckdb.DuckDBPyConnection:
    # One thread: the data is small, and DuckDB 1.4-1.5 can hang running several window functions over
    # aggregates (as the RFM query does) in parallel.
    return duckdb.connect(database, config={"threads": 1})


def load(con: duckdb.DuckDBPyConnection, raw_dir: str = RAW_DIR) -> dict[str, int]:
    """(Re)create the ``raw`` schema from the CSV export. Returns the row count of each table."""
    folder = data.write_csvs(raw_dir)
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")
    counts = {}
    for table, columns in TYPES.items():
        spec = ", ".join(f"'{name}': '{kind}'" for name, kind in columns.items())
        path = (folder / f"{table}.csv").as_posix().replace("'", "''")
        con.execute(
            f"CREATE OR REPLACE TABLE raw.{table} AS "  # noqa: S608 - table names and types come from TYPES above
            f"SELECT * FROM read_csv('{path}', header = true, columns = {{{spec}}}, nullstr = '')"
        )
        counts[table] = con.execute(f"SELECT COUNT(*) FROM raw.{table}").fetchone()[0]  # noqa: S608
    return counts


def has_sql(text: str) -> bool:
    """Whether a file holds a statement, not only comments and blank lines."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("--"):
            return True
    return False


def run_file(con: duckdb.DuckDBPyConnection, path: str | Path, show: bool = True, timer: bool = False) -> bool:
    """Run every statement in a file. Prints the last statement's result when it returns rows."""
    text = Path(path).read_text(encoding="utf-8")
    if not has_sql(text):
        print(f"-- {path}: nothing to run yet (only comments)")
        return True
    started = time.perf_counter()
    try:
        result = con.sql(text)
        if result is not None and show:
            result.show(max_rows=40)
    except duckdb.Error as error:
        print(f"-- {path}: FAILED\n{error}")
        return False
    if timer:
        print(f"-- {path}: {time.perf_counter() - started:.2f} s")
    return True


def build(con: duckdb.DuckDBPyConnection, root: str | Path = ".") -> list[str]:
    """Load the export, then run the profiling and model files in order. Returns the files that failed; the
    rest still run, so one unfinished file does not hide the state of the others."""
    load(con)
    failed = []
    for name in BUILD_ORDER:
        path = Path(root) / name
        if not path.is_file():
            continue
        if not run_file(con, path, show=False):
            failed.append(name)
    return failed
