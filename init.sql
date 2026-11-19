CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    producer VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 100
);

INSERT INTO products (name, category, producer, price, stock)
SELECT
    'Produit fermier #' || i,
    (ARRAY['Légumes', 'Fruits', 'Produits laitiers', 'Viandes'])[floor(random() * 4 + 1)],
    'Producteur #' || floor(random() * 20 + 1),
    round((random() * 40 + 2)::numeric, 2),
    floor(random() * 150 + 10)::int
FROM generate_series(1, 1200) AS s(i); 