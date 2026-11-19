import os
from contextlib import contextmanager

import pytest

# main.py lit DATABASE_URL à l'import ; les tests n'ouvrent jamais de vraie connexion.
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test")

import app.main as main  # noqa: E402


class FakeCursor:
    def __init__(self, row=None):
        self.row = row

    def fetchone(self):
        return self.row


class FakeConn:
    """Mini base en mémoire qui imite les requêtes de main.py (pas de vraie base)."""

    def __init__(self, products, users, stocks):
        self.products = set(products)
        self.users = set(users)
        self.stocks = dict(stocks)  # {(user_id, product_id): quantité}
        self.orders = []  # user_id de chaque commande
        self.items = []  # (order_id, product_id, quantité)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    @contextmanager
    def transaction(self):
        # Comme PostgreSQL : si une exception sort du bloc, tout est annulé.
        sauvegarde = (dict(self.stocks), list(self.orders), list(self.items))
        try:
            yield
        except BaseException:
            self.stocks, self.orders, self.items = sauvegarde
            raise

    def execute(self, sql, params=()):
        s = " ".join(sql.split())
        if s.startswith("SELECT 1 FROM products"):
            return FakeCursor((1,) if params[0] in self.products else None)
        if s.startswith("SELECT 1 FROM users"):
            return FakeCursor((1,) if params[0] in self.users else None)
        if s.startswith("SELECT quantity FROM user_stocks"):
            quantite = self.stocks.get((params[0], params[1]))
            return FakeCursor(None if quantite is None else (quantite,))
        if s.startswith("INSERT INTO user_stocks"):
            user_id, product_id, quantite = params
            self.stocks[(user_id, product_id)] = quantite
            return FakeCursor((user_id, product_id, quantite))
        if s.startswith("INSERT INTO orders"):
            self.orders.append(params[0])
            return FakeCursor((len(self.orders),))
        if s.startswith("UPDATE user_stocks"):
            quantite, user_id, product_id = params
            self.stocks[(user_id, product_id)] -= quantite
            return FakeCursor()
        if s.startswith("INSERT INTO order_items"):
            self.items.append(params)
            return FakeCursor()
        if s.startswith("SELECT id, name FROM products"):
            return [(p, f"Produit {p}") for p in sorted(self.products)]
        raise AssertionError(f"Requête inattendue dans le test : {s}")


@pytest.fixture
def db(monkeypatch):
    """Base factice : produits 1 et 2, utilisateurs 1 (producteur) et 2, stock de l'utilisateur 1."""
    conn = FakeConn(products={1, 2}, users={1, 2}, stocks={(1, 1): 5, (1, 2): 3})
    monkeypatch.setattr(main.psycopg, "connect", lambda dsn: conn)
    return conn
