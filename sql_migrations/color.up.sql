CREATE TABLE color (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
    color text NOT NULL
);

CREATE UNIQUE INDEX color_name ON color (color);

INSERT INTO color (color)
    VALUES ('White'), ('Yellow'), ('Blue'), ('Red'), ('Green'), ('Black'), ('Brown'), ('Other');

