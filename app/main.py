import os
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg

app = FastAPI()
DSN = os.environ["DATABASE_URL"]

class Order(BaseModel):
    product_id: int
    quantity: int

@app.get("/health")
def health():
    return {"status": "ok", "version": os.getenv("APP_VERSION", "dev")}

@app.get("/products")
def products():
    with psycopg.connect(DSN) as c:
        return [{"id": r[0], "name": r[1]} for r in c.execute("SELECT id, name FROM products")]

class OrderItems(BaseModel):
    user_id: int
    items: list[Order]

@app.post("/orders")
def create_order(o: OrderItems):
    with psycopg.connect(DSN) as c:
        with c.transaction():

            # Vérifier le stock de tous les produits
            for item in o.items:
                stock = c.execute("""
                    SELECT quantity
                    FROM user_stocks
                    WHERE user_id = %s AND product_id = %s
                    FOR UPDATE
                """, (o.user_id, item.product_id)).fetchone()

                if stock is None:
                    return {
                        "error": f"Aucun stock enregistré pour le produit {item.product_id}."
                    }

                if stock[0] < item.quantity:
                    return {
                        "error": f"Stock insuffisant pour le produit {item.product_id}. "
                                 f"Disponible : {stock[0]}, demandé : {item.quantity}."
                    }

            # Retirer les quantités du stock
            for item in o.items:
                c.execute("""
                    UPDATE user_stocks
                    SET quantity = quantity - %s
                    WHERE user_id = %s AND product_id = %s
                """, (item.quantity, o.user_id, item.product_id))

    return {"message": "Stock mis à jour avec succès."}