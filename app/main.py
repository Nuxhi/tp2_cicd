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

@app.post("/orders", status_code=201)
def create_order(o: Order):
    with psycopg.connect(DSN) as c:
        c.execute("INSERT INTO orders(product_id, quantity) VALUES (%s,%s)", (o.product_id, o.quantity))
    return {"status": "created"}