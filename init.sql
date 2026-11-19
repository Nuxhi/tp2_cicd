CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role_id INTEGER NOT NULL REFERENCES roles(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_order_items PRIMARY KEY (order_id, product_id)
);

-- Stock de chaque utilisateur pour chaque produit
CREATE TABLE user_stocks (
    user_id INTEGER NOT NULL REFERENCES users(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),

    CONSTRAINT pk_user_stocks PRIMARY KEY (user_id, product_id)
);

INSERT INTO roles (name) VALUES ('producteur'), ('client')
ON CONFLICT (name) DO NOTHING;

-- 2. Insertion de quelques utilisateurs (producteurs et clients)
INSERT INTO users (username, email, password, role_id) VALUES
    ('ferme_soleil', 'contact@fermedusoleil.fr', 'hash_factice_1', 1),
    ('verger_bio', 'info@vergerbio.fr', 'hash_factice_2', 1),
    ('resto_paoli', 'chef@restopaoli.fr', 'hash_factice_3', 2),
    ('client_jean', 'jean.dupont@email.fr', 'hash_factice_4', 2)
ON CONFLICT (username) DO NOTHING;

-- 3. Insertion des 1 200 produits
INSERT INTO products (name)
SELECT 'Produit fermier #' || i
FROM generate_series(1, 1200) AS s(i);

