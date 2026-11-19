import pytest

from app.stock import InsufficientStock, allocate


def test_commande_egale_au_stock_acceptee():
    assert allocate(1, [(10, 5)], 5) == [(10, 5)]


def test_commande_inferieure_au_stock_acceptee():
    assert allocate(1, [(10, 5)], 2) == [(10, 2)]


def test_commande_superieure_au_stock_refusee():
    with pytest.raises(InsufficientStock) as e:
        allocate(1, [(10, 5)], 6)
    assert e.value.requested == 6
    assert e.value.available == 5


def test_message_clair():
    with pytest.raises(InsufficientStock) as e:
        allocate(7, [(10, 5)], 6)
    assert str(e.value) == "Stock insuffisant pour le produit 7 : demandé 6, disponible 5"


def test_produit_sans_stock_refuse():
    with pytest.raises(InsufficientStock) as e:
        allocate(1, [], 1)
    assert e.value.available == 0


def test_stock_reparti_sur_plusieurs_producteurs():
    assert allocate(1, [(10, 3), (11, 4)], 5) == [(10, 3), (11, 2)]


def test_stock_total_de_plusieurs_producteurs_depasse():
    with pytest.raises(InsufficientStock) as e:
        allocate(1, [(10, 3), (11, 4)], 8)
    assert e.value.available == 7
