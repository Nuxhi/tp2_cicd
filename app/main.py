import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import psycopg

from app.orders import place_order
from app.stock import InsufficientStock

app = FastAPI()
DSN = os.environ["DATABASE_URL"]


class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class Order(BaseModel):
    user_id: int
    items: list[OrderItem] = Field(min_length=1)


@app.get("/health")
def health():
    return {"status": "ok", "version": os.getenv("APP_VERSION", "dev")}


@app.get("/products")
def products():
    with psycopg.connect(DSN) as c:
        return [{"id": r[0], "name": r[1]} for r in c.execute("SELECT id, name FROM products")]


@app.post("/orders", status_code=201)
def create_order(o: Order):
    try:
        with psycopg.connect(DSN) as c:
            order_id = place_order(c, o.user_id, [(i.product_id, i.quantity) for i in o.items])
    except InsufficientStock as e:
        raise HTTPException(status_code=409, detail=str(e))
    except psycopg.errors.ForeignKeyViolation:
        raise HTTPException(status_code=404, detail="Utilisateur ou produit inconnu")
    return {"status": "created", "order_id": order_id}
