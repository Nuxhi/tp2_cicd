import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import psycopg

app = FastAPI()
DSN = os.environ["DATABASE_URL"]


# ---------------------------------------------------------------------------
# Modèles (formats des requêtes)
# ---------------------------------------------------------------------------

class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class Order(BaseModel):
    user_id: int
    items: list[OrderItem]

class StockUpdate(BaseModel):
    user_id: int
    quantity: int


# ---------------------------------------------------------------------------
# Santé
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok", "version": os.getenv("APP_VERSION", "dev")}


# ---------------------------------------------------------------------------
# Produits
# ---------------------------------------------------------------------------

@app.get("/products")
def products():
    with psycopg.connect(DSN) as c:
        return [
            {"id": r[0], "name": r[1]}
            for r in c.execute("SELECT id, name FROM products")
        ]


# ---------------------------------------------------------------------------
# Stock des producteurs
# ---------------------------------------------------------------------------

@app.put("/products/{product_id}/stock")
def update_stock(product_id: int, stock_update: StockUpdate):
    if stock_update.quantity < 0:
        raise HTTPException(status_code=422, detail="Le stock doit être positif ou nul")

    with psycopg.connect(DSN) as c:
        product_exists = c.execute(
            "SELECT 1 FROM products WHERE id = %s", (product_id,)
        ).fetchone()
        if product_exists is None:
            raise HTTPException(status_code=404, detail="Produit introuvable")

        producer_exists = c.execute(
            "SELECT 1 FROM users WHERE id = %s", (stock_update.user_id,)
        ).fetchone()
        if producer_exists is None:
            raise HTTPException(status_code=404, detail="Producteur introuvable")

        stock = c.execute(
            """
            INSERT INTO user_stocks (user_id, product_id, quantity)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, product_id)
            DO UPDATE SET quantity = EXCLUDED.quantity
            RETURNING user_id, product_id, quantity
            """,
            (stock_update.user_id, product_id, stock_update.quantity),
        ).fetchone()

    return {"user_id": stock[0], "product_id": stock[1], "quantity": stock[2]}

@app.get("/products/{product_id}/stock")
def get_stock(product_id: int, user_id: int):
    with psycopg.connect(DSN) as c:
        product_exists = c.execute(
            "SELECT 1 FROM products WHERE id = %s", (product_id,)
        ).fetchone()
        if product_exists is None:
            raise HTTPException(status_code=404, detail="Produit introuvable")

        stock = c.execute(
            """
            SELECT quantity
            FROM user_stocks
            WHERE user_id = %s AND product_id = %s
            """,
            (user_id, product_id),
        ).fetchone()

    return {"user_id": user_id, "product_id": product_id, "quantity": stock[0] if stock else 0}


# ---------------------------------------------------------------------------
# Commandes (règle : commande > stock -> refus)
# ---------------------------------------------------------------------------

@app.post("/orders", status_code=201)
def create_order(o: Order):
    if not o.items:
        raise HTTPException(status_code=422, detail="La commande doit contenir au moins un produit")

    # Un même produit peut apparaître sur plusieurs lignes : on additionne.
    items_by_product = {}
    for item in o.items:
        items_by_product[item.product_id] = (
            items_by_product.get(item.product_id, 0) + item.quantity
        )

    with psycopg.connect(DSN) as c:
        # Si une erreur sort du bloc, tout est annulé (ni commande, ni stock modifié).
        with c.transaction():
            # 1) Vérification du stock de chaque produit (ligne verrouillée).
            for product_id, quantity in items_by_product.items():
                stock = c.execute(
                    """
                    SELECT quantity
                    FROM user_stocks
                    WHERE user_id = %s AND product_id = %s
                    FOR UPDATE
                    """,
                    (o.user_id, product_id),
                ).fetchone()

                if stock is None:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Aucun stock enregistré pour le produit {product_id}.",
                    )

                if stock[0] < quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            f"Stock insuffisant pour le produit {product_id}. "
                            f"Disponible : {stock[0]}, demandé : {quantity}."
                        ),
                    )

            # 2) Création de la commande.
            order = c.execute(
                "INSERT INTO orders (user_id) VALUES (%s) RETURNING id",
                (o.user_id,),
            ).fetchone()

            # 3) Décrémentation du stock et enregistrement des lignes.
            for product_id, quantity in items_by_product.items():
                c.execute(
                    """
                    UPDATE user_stocks
                    SET quantity = quantity - %s
                    WHERE user_id = %s AND product_id = %s
                    """,
                    (quantity, o.user_id, product_id),
                )
                c.execute(
                    """
                    INSERT INTO order_items (order_id, product_id, quantity)
                    VALUES (%s, %s, %s)
                    """,
                    (order[0], product_id, quantity),
                )

    return {"order_id": order[0], "message": "Commande créée et stock mis à jour."}
