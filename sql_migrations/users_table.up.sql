CREATE TABLE IF NOT EXISTS 'users' (
    'id' integer PRIMARY KEY AUTOINCREMENT NOT NULL,
    'username' text NOT NULL,
    'hash' text NOT NULL,
    'cash' numeric NOT NULL DEFAULT 10000.00
);

CREATE UNIQUE INDEX 'username' ON "users" ("username");

