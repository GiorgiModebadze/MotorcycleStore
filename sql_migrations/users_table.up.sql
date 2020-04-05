CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
    username text NOT NULL,
    hash text NOT NULL,
    phone_number text,
    email text NOT NULL
);

CREATE UNIQUE INDEX username ON "users" ("username");

