-- Runs once, when the postgres volume is first created (and again after `docker compose down -v`).
CREATE SCHEMA IF NOT EXISTS sample;

CREATE TABLE sample.customers (
    customer_id integer PRIMARY KEY,
    name        text        NOT NULL,
    email       text        NOT NULL,
    country     char(2)     NOT NULL,
    created_at  timestamptz NOT NULL
);

CREATE TABLE sample.orders (
    order_id    integer PRIMARY KEY,
    customer_id integer       NOT NULL REFERENCES sample.customers (customer_id),
    ordered_at  timestamptz   NOT NULL,
    status      text          NOT NULL CHECK (status IN ('placed', 'shipped', 'returned')),
    amount      numeric(10,2) NOT NULL
);

INSERT INTO sample.customers VALUES
    (1, 'Ada Lovelace',   'ADA@example.com ',    'GB', '2026-01-03 09:12:00+00'),
    (2, 'Grace Hopper',   'grace@example.com',   'US', '2026-01-05 14:40:00+00'),
    (3, 'Alan Turing',    'alan@example.com',    'GB', '2026-01-09 08:05:00+00'),
    (4, 'Katherine Johnson', 'kj@example.com',   'US', '2026-02-11 17:30:00+00'),
    (5, 'Edsger Dijkstra', ' edsger@example.com', 'NL', '2026-02-20 10:00:00+00');

INSERT INTO sample.orders VALUES
    (101, 1, '2026-03-01 10:00:00+00', 'shipped',  42.50),
    (102, 2, '2026-03-01 11:30:00+00', 'placed',   15.00),
    (103, 1, '2026-03-02 09:45:00+00', 'returned', 42.50),
    (104, 3, '2026-03-02 16:20:00+00', 'shipped',  99.99),
    (105, 4, '2026-03-03 12:00:00+00', 'shipped',  12.75),
    (106, 5, '2026-03-03 13:10:00+00', 'placed',   64.00),
    (107, 2, '2026-03-04 08:00:00+00', 'shipped',  23.10);
