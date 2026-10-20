"""Verify your lab. Run inside the workspace: python -m pytest -q tests/test_environment.py"""

import sys

import pytest


def test_python_version():
    assert sys.version_info[:2] == (3, 12), sys.version


def test_packages_import():
    import jupyterlab  # noqa: F401
    import pandas  # noqa: F401
    import psycopg  # noqa: F401


@pytest.mark.service
def test_postgres_is_reachable(pg_conninfo):
    import psycopg

    with psycopg.connect(**pg_conninfo) as conn:
        version = conn.execute("SHOW server_version").fetchone()[0]
    assert version.startswith("16."), version


@pytest.mark.service
def test_sample_database_is_loaded(pg_conninfo):
    import psycopg

    with psycopg.connect(**pg_conninfo) as conn:
        customers = conn.execute("SELECT count(*) FROM sample.customers").fetchone()[0]
        orders = conn.execute("SELECT count(*) FROM sample.orders").fetchone()[0]
    assert customers == 5 and orders == 7, "Sample data missing; reset with: docker compose down -v"
