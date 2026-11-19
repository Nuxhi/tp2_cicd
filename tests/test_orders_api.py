import pytest
from fastapi.testclient import TestClient

import app.main as main

client = TestClient(main.app)


def commande(items, user_id=1):
    return {"user_id": user_id, "items": [{"product_id": p, "quantity": q} for p, q in items]}


# --- Règle : commande > stock -> refus -------------------------------------

def test_commande_dans_le_stock_acceptee_et_stock_decremente(db):
    r = client.post("/orders", json=commande([(1, 3)]))
    assert r.status_code == 201
    assert r.json()["order_id"] == 1
    assert db.stocks[(1, 1)] == 2
    assert db.items == [(1, 1, 3)]


def test_commande_egale_au_stock_acceptee(db):
    r = client.post("/orders", json=commande([(1, 5)]))
    assert r.status_code == 201
    assert db.stocks[(1, 1)] == 0


def test_commande_superieure_au_stock_refusee_avec_message_clair(db):
    r = client.post("/orders", json=commande([(1, 6)]))
    assert r.status_code == 400
    assert r.json()["detail"] == "Stock insuffisant pour le produit 1. Disponible : 5, demandé : 6."


def test_commande_refusee_n_ecrit_rien(db):
    client.post("/orders", json=commande([(1, 6)]))
    assert db.stocks == {(1, 1): 5, (1, 2): 3}
    assert db.orders == []
    assert db.items == []


def test_commande_refusee_si_aucun_stock_enregistre(db):
    r = client.post("/orders", json=commande([(1, 1)], user_id=2))
    assert r.status_code == 400
    assert r.json()["detail"] == "Aucun stock enregistré pour le produit 1."


def test_un_seul_produit_en_rupture_refuse_toute_la_commande(db):
    r = client.post("/orders", json=commande([(1, 2), (2, 4)]))  # produit 2 : stock 3
    assert r.status_code == 400
    assert db.stocks == {(1, 1): 5, (1, 2): 3}
    assert db.orders == []


def test_lignes_du_meme_produit_additionnees(db):
    r = client.post("/orders", json=commande([(1, 3), (1, 3)]))  # 6 > 5
    assert r.status_code == 400
    assert "demandé : 6" in r.json()["detail"]


def test_commande_de_plusieurs_produits(db):
    r = client.post("/orders", json=commande([(1, 1), (2, 3)]))
    assert r.status_code == 201
    assert db.stocks == {(1, 1): 4, (1, 2): 0}


@pytest.mark.parametrize("quantite", [0, -1])
def test_quantite_invalide_rejetee(db, quantite):
    r = client.post("/orders", json=commande([(1, quantite)]))
    assert r.status_code == 422


def test_commande_vide_rejetee(db):
    r = client.post("/orders", json=commande([]))
    assert r.status_code == 422
    assert db.orders == []


# --- Déclaration du stock : PUT /products/{id}/stock -----------------------

def test_declarer_un_stock_nouveau(db):
    r = client.put("/products/2/stock", json={"user_id": 2, "quantity": 10})
    assert r.status_code == 200
    assert r.json() == {"user_id": 2, "product_id": 2, "quantity": 10}
    assert db.stocks[(2, 2)] == 10


def test_declarer_un_stock_remplace_l_ancien(db):
    client.put("/products/1/stock", json={"user_id": 1, "quantity": 20})
    assert db.stocks[(1, 1)] == 20


def test_stock_negatif_refuse(db):
    r = client.put("/products/1/stock", json={"user_id": 1, "quantity": -1})
    assert r.status_code == 422
    assert db.stocks[(1, 1)] == 5


def test_stock_produit_inconnu(db):
    r = client.put("/products/999/stock", json={"user_id": 1, "quantity": 1})
    assert r.status_code == 404
    assert r.json()["detail"] == "Produit introuvable"


def test_stock_producteur_inconnu(db):
    r = client.put("/products/1/stock", json={"user_id": 999, "quantity": 1})
    assert r.status_code == 404
    assert r.json()["detail"] == "Producteur introuvable"


# --- Consultation du stock : GET /products/{id}/stock ----------------------

def test_consulter_le_stock(db):
    r = client.get("/products/1/stock", params={"user_id": 1})
    assert r.status_code == 200
    assert r.json() == {"user_id": 1, "product_id": 1, "quantity": 5}


def test_consulter_un_stock_non_declare_renvoie_zero(db):
    r = client.get("/products/1/stock", params={"user_id": 2})
    assert r.json()["quantity"] == 0


def test_consulter_le_stock_d_un_produit_inconnu(db):
    r = client.get("/products/999/stock", params={"user_id": 1})
    assert r.status_code == 404


# --- Santé et produits -----------------------------------------------------

def test_health_expose_la_version(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "v1.2.3")
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "version": "v1.2.3"}


def test_liste_des_produits(db):
    r = client.get("/products")
    assert r.status_code == 200
    assert r.json() == [{"id": 1, "name": "Produit 1"}, {"id": 2, "name": "Produit 2"}]
