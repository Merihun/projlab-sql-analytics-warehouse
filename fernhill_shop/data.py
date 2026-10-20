"""Deterministic sample data: the six tables of the Fernhill shop export, with its known defects.

Standard library only. The counts are exact; the defects are injected at fixed rates:
about 1% of customers have a malformed email and a few have none, signup dates come in two formats,
names and codes carry stray whitespace and mixed case, and about 0.5% of order lines point at a product
that does not exist.
"""

from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

SEED = 1101
VERSION = "fernhill-shop/1"
CUSTOMERS, PRODUCTS, CATEGORIES, ORDERS, ORDER_LINES = 20_000, 1_200, 40, 90_000, 250_000
START = datetime(2024, 9, 1)
SECONDS = 730 * 86_400  # 2024-09-01 00:00:00 up to 2026-08-31 23:59:59

FIRST = ("Anna", "Ben", "Chloe", "Dev", "Ella", "Farid", "Grace", "Hugo", "Isla", "Jon", "Kira", "Liam",
         "Maya", "Noah", "Olga", "Pia", "Quinn", "Ravi", "Sara", "Tom")  # fmt: skip
LAST = ("Ahmed", "Brown", "Clark", "Diaz", "Evans", "Fischer", "Green", "Hughes", "Ito", "Jones", "Khan",
        "Lopez", "Meyer", "Novak", "Owen", "Patel", "Reid", "Silva", "Turner", "Wood")  # fmt: skip
COUNTRIES = ("GB", "GB", "GB", "GB", "IE", "FR", "DE", "NL", "ES", "US")
DOMAINS = ("example.com", "mail.test", "fernhill.example", "post.example.org")
KINDS = ("Tents", "Footwear", "Jackets", "Backpacks", "Sleeping Bags", "Stoves", "Lamps", "Climbing",
         "Cycling", "Water", "Maps", "Base Layers", "Gloves", "Hats", "Socks", "Poles", "Kayaks", "Fishing",
         "Navigation", "First Aid")  # fmt: skip
STATUS = ("placed", "shipped", "delivered", "delivered", "delivered", "cancelled")
CHANNEL = ("web", "web", "web", "app", "app", "marketplace")
METHOD = ("card", "card", "card", "paypal", "gift_card")

TABLES = {
    "customers": ("customer_id", "email", "first_name", "last_name", "country_code", "signup_date"),
    "categories": ("category_id", "category_name"),
    "products": ("product_id", "sku", "product_name", "category_id", "list_price"),
    "orders": ("order_id", "customer_id", "order_ts", "status", "channel"),
    "order_lines": ("order_line_id", "order_id", "product_id", "quantity", "unit_price", "discount_amount"),
    "payments": ("payment_id", "order_id", "method", "amount", "paid_at"),
}


def _messy(rng: random.Random, text: str) -> str:
    """Now and then, the stray whitespace and odd capitals a real export has."""
    roll = rng.random()
    if roll < 0.04:
        return f"  {text}"
    if roll < 0.08:
        return f"{text} "
    if roll < 0.11:
        return text.upper()
    return text


def _email(rng: random.Random, n: int, first: str, last: str) -> str:
    good = f"{first}.{last}{n}@{rng.choice(DOMAINS)}".lower()
    roll = rng.random()
    if roll < 0.003:
        return ""  # no email on file
    if roll < 0.013:  # about 1% malformed
        return rng.choice((good.replace("@", ""), good.replace("@", " at "), good.split(".")[0] + "@", "n/a", good + "."))
    return _messy(rng, good)  # valid once trimmed and lower-cased


def generate() -> dict[str, list[tuple]]:
    """Every table as a list of rows, in the column order of ``TABLES``."""
    rng = random.Random(SEED)
    customers = []
    for n in range(1, CUSTOMERS + 1):
        first, last = rng.choice(FIRST), rng.choice(LAST)
        day = START - timedelta(days=rng.randrange(0, 900)) + timedelta(days=rng.randrange(0, 600))
        signup = day.strftime("%d/%m/%Y") if rng.random() < 0.2 else day.strftime("%Y-%m-%d")
        country = "" if rng.random() < 0.01 else _messy(rng, rng.choice(COUNTRIES)).replace("gb", "GB")
        if rng.random() < 0.03:
            country = country.lower()
        customers.append((n, _email(rng, n, first, last), _messy(rng, first), _messy(rng, last), country, signup))

    categories = [(n, f"{KINDS[(n - 1) % 20]}{'' if n <= 20 else ' Pro'}") for n in range(1, CATEGORIES + 1)]
    products = []
    for n in range(1, PRODUCTS + 1):
        category = rng.randint(1, CATEGORIES)
        name = _messy(rng, f"{categories[category - 1][1]} {rng.choice(('Trail', 'Summit', 'Ridge', 'Coast'))} {n}")
        products.append((n, f"FH-{n:05d}", name, category, f"{rng.randint(500, 40_000) / 100:.2f}"))
    price = {p[0]: float(p[4]) for p in products}

    orders, status_of = [], {}
    for n in range(1, ORDERS + 1):
        ts = START + timedelta(seconds=rng.randrange(SECONDS))
        status = rng.choice(STATUS)
        status_of[n] = status
        shown = status.capitalize() if rng.random() < 0.05 else status.upper() if rng.random() < 0.03 else status
        channel = rng.choice(CHANNEL)
        orders.append((n, rng.randint(1, CUSTOMERS), ts.strftime("%Y-%m-%d %H:%M:%S"),
                       shown, channel.capitalize() if rng.random() < 0.04 else channel))  # fmt: skip

    lines, totals = [], dict.fromkeys(range(1, ORDERS + 1), 0.0)
    for n in range(1, ORDER_LINES + 1):
        order_id = n if n <= ORDERS else rng.randint(1, ORDERS)  # every order has at least one line
        orphan = rng.random() < 0.005
        product_id = PRODUCTS + rng.randint(1, 100) if orphan else rng.randint(1, PRODUCTS)
        quantity = rng.choice((1, 1, 1, 2, 2, 3, 4, 5))
        unit = rng.randint(500, 40_000) / 100 if orphan else round(price[product_id] * rng.choice((1, 1, 0.9, 0.8)), 2)
        gross = quantity * unit
        discount = round(gross * rng.choice((0, 0, 0, 0.05, 0.1)), 2)
        totals[order_id] += gross - discount
        lines.append((n, order_id, product_id, quantity, f"{unit:.2f}", f"{discount:.2f}"))

    payments = []
    for n in range(1, ORDERS + 1):
        paid = "" if status_of[n] == "cancelled" and rng.random() < 0.6 else (
            START + timedelta(seconds=rng.randrange(SECONDS))).strftime("%Y-%m-%d %H:%M:%S")  # fmt: skip
        payments.append((n, n, rng.choice(METHOD), f"{totals[n]:.2f}", paid))

    return {"customers": customers, "categories": categories, "products": products, "orders": orders,
            "order_lines": lines, "payments": payments}  # fmt: skip


def write_csvs(out_dir: str | Path) -> Path:
    """Write the six tables as CSV files into ``out_dir`` (skipped when this version is already there)."""
    target = Path(out_dir)
    marker = target / ".version"
    if marker.is_file() and marker.read_text(encoding="utf-8") == VERSION and all(
        (target / f"{name}.csv").is_file() for name in TABLES
    ):
        return target
    target.mkdir(parents=True, exist_ok=True)
    for name, rows in generate().items():
        with (target / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle, lineterminator="\n")
            writer.writerow(TABLES[name])
            writer.writerows(rows)
    marker.write_text(VERSION, encoding="utf-8")
    return target
