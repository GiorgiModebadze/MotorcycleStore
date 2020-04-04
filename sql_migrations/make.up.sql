CREATE TABLE make (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
    make text NOT NULL
);

CREATE UNIQUE INDEX make_unique ON make (make);

