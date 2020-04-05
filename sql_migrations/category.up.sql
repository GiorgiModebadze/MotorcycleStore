CREATE TABLE category (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
    category text NOT NULL
);

CREATE UNIQUE INDEX category_unique ON category (category);

INSERT INTO category (category)
    VALUES ('Chopper / Cruiser'), ('Combination / Sidecar'), ('Dirt Bike'), ('Enduro / Touring Enduro'), ('Lightweight Motorcycle / Motorbike'), ('Motor - assisted Bicycle / Small Moped'), ('Motorcycle'), ('Naked Bike'), ('Racing'), ('Rally/Cross'), ('Scooter'), ('Sport/Super Sport'), ('Sport Touring'), ('Streetfighter'), ('Supter Moto'), ('Tourer'), ('Trike'), ('Other');

