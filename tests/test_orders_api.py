from contextlib import contextmanager

import pytest
from fastapi.testclient import TestClient

import app.main as main
from app.stock import InsufficientStock

client = TestClient(main.app)

COMMANDE = {"user_id": 1, "items": [{"product_id": 1, "quantity": 3}]}


class FakeConn:
    """Connexion factice : l'API est testée sans base de données."""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


@pytest.fixture(autouse=True)
def fausse_base(monkeypatch):
    monkeypatch.setattr(main.psycopg, "connect", lambda dsn: FakeConn())


def test_commande_dans_le_stock_creee(monkeypatch):
    monkeypatch.setattr(main, "place_order", lambda conn, user_id, items: 42)
    r = client.post("/orders", json=COMMANDE)
    assert r.status_code == 201
    assert r.json() == {"status": "created", "order_id": 42}


def test_commande_au_dela_du_stock_refusee_avec_message_clair(monkeypatch):
    def refuse(conn, user_id, items):
        raise InsufficientStock(1, 3, 2)

    monkeypatch.setattr(main, "place_order", refuse)
    r = client.post("/orders", json=COMMANDE)
    assert r.status_code == 409
    assert r.json()["detail"] == "Stock insuffisant pour le produit 1 : demandé 3, disponible 2"


def test_place_order_recoit_les_lignes_de_la_commande(monkeypatch):
    recu = {}

    def espion(conn, user_id, items):
        recu["user_id"], recu["items"] = user_id, items
        return 1

    monkeypatch.setattr(main, "place_order", espion)
    client.post("/orders", json={"user_id": 2, "items": [{"product_id": 5, "quantity": 4}]})
    assert recu == {"user_id": 2, "items": [(5, 4)]}


@pytest.mark.parametrize("quantite", [0, -1])
def test_quantite_invalide_rejetee(quantite):
    r = client.post("/orders", json={"user_id": 1, "items": [{"product_id": 1, "quantity": quantite}]})
    assert r.status_code == 422


def test_commande_vide_rejetee():
    r = client.post("/orders", json={"user_id": 1, "items": []})
    assert r.status_code == 422
