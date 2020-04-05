CREATE TABLE model (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
    model text NOT NULL,
    make_id int NOT NULL,
    FOREIGN KEY (make_id) REFERENCES id (make)
);

CREATE UNIQUE INDEX model_unique ON model (model, make_id);

