from fastapi import FastAPI, HTTPException
from models import OrderCreate, OrderUpdate

app = FastAPI(
    title="Order Service",
    description="Microservice for managing orders in the E-Commerce system",
    version="1.0.0",
)

# In-memory storage
orders = []
id_counter = 0


@app.get("/orders", tags=["Orders"])
def get_orders():
    """Retrieve all orders."""
    return orders


@app.get("/orders/{order_id}", tags=["Orders"])
def get_order(order_id: int):
    """Retrieve a single order by its ID."""
    for order in orders:
        if order["id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")


@app.post("/orders", status_code=201, tags=["Orders"])
def create_order(order: OrderCreate):
    """Create a new order."""
    global id_counter
    id_counter += 1
    new_order = {
        "id": id_counter,
        "status": "pending",
        **order.model_dump(),
    }
    orders.append(new_order)
    return {"message": "Order created successfully", "data": new_order}


@app.put("/orders/{order_id}", tags=["Orders"])
def update_order(order_id: int, order: OrderUpdate):
    """Update an existing order (e.g. change status)."""
    for idx, existing in enumerate(orders):
        if existing["id"] == order_id:
            update_data = order.model_dump(exclude_unset=True)
            orders[idx] = {**existing, **update_data}
            return {"message": "Order updated successfully", "data": orders[idx]}
    raise HTTPException(status_code=404, detail="Order not found")


@app.delete("/orders/{order_id}", tags=["Orders"])
def delete_order(order_id: int):
    """Delete an order by its ID."""
    for idx, existing in enumerate(orders):
        if existing["id"] == order_id:
            orders.pop(idx)
            return {"message": "Order deleted successfully"}
    raise HTTPException(status_code=404, detail="Order not found")
