from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="FastAPI CI/CD Demo")

orders = {}


class OrderCreate(BaseModel):
    user_id: int
    start: str
    end: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/orders")
def create_order(order: OrderCreate):
    order_id = len(orders) + 1
    orders[order_id] = {
        "id": order_id,
        "user_id": order.user_id,
        "start": order.start,
        "end": order.end,
        "status": "CREATED",
    }
    return orders[order_id]


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="order not found")
    return orders[order_id]


@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: int):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="order not found")

    order = orders[order_id]

    if order["status"] != "CREATED":
        raise HTTPException(status_code=400, detail="only CREATED order can be canceled")

    order["status"] = "CANCELED"
    return order