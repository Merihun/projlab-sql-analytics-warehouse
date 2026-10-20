"""Command line for the shop export and your SQL files. See ``python -m fernhill_shop --help``."""

from __future__ import annotations

import argparse

import duckdb

from fernhill_shop import warehouse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m fernhill_shop", description="Fernhill shop export and SQL runner.")
    parser.add_argument("--database", default=warehouse.DATABASE, help="The DuckDB file (default: fernhill.db).")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("load", help="Create the database with the six raw tables.")
    run = sub.add_parser("run", help="Run one or more SQL files and print the last result.")
    run.add_argument("files", nargs="+")
    run.add_argument("--timer", action="store_true", help="Print how long each file took.")
    query = sub.add_parser("query", help='Run one statement, e.g. query "SELECT COUNT(*) FROM raw.orders".')
    query.add_argument("sql")
    sub.add_parser("build", help="Load the export, then run profiling/ and models/ in order.")
    args = parser.parse_args(argv)

    con = warehouse.connect(args.database)
    try:
        if args.command == "load":
            for table, rows in warehouse.load(con).items():
                print(f"raw.{table:12} {rows:>8,} rows")
            print(f"Database: {args.database}")
            return 0
        if args.command == "build":
            failed = warehouse.build(con)
            print("Built." if not failed else f"Built, with errors in: {', '.join(failed)}")
            return 0  # the checks report what is missing, file by file
        if args.command == "query":
            try:
                result = con.sql(args.sql)
                if result is not None:
                    result.show(max_rows=60)
            except duckdb.Error as error:
                print(error)
                return 1
            return 0
        ok = all([warehouse.run_file(con, path, timer=args.timer) for path in args.files])
        return 0 if ok else 1
    finally:
        con.close()


if __name__ == "__main__":
    raise SystemExit(main())
