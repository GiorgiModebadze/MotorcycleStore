CREATE TABLE condition (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
    condition_name text NOT NULL
);

CREATE UNIQUE INDEX condition_name ON condition (condition_name);

INSERT INTO condition (condition_name)
    VALUES ('new'), ('used');

