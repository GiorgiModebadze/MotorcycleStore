CREATE TABLE advertisment (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id int NOT NULL REFERENCES users (id),
    created_at date NOT NULL DEFAULT CURRENT_TIMESTAMP,
    condition text NOT NULL,
    make text NOT NULL,
    model text NOT NULL,
    category text NOT NULL,
    price int NOT NULL,
    milage int NOT NULL,
    hp int NOT NULL,
    color text NOT NULL,
    picture BLOB NOT NULL,
    picture_name NOT NULL,
    description text NULL,
    active int NOT NULL
);

