from fastapi import FastAPI, Request
import httpx

app = FastAPI(
    title="API Gateway",
    description="Centralized API Gateway for the E-Commerce Microservices System. "
                "Routes all requests to the appropriate microservice through a single entry point.",
    version="1.0.0",
)

# Service registry — maps service names to their base URLs
SERVICES = {
    "product":   "http://localhost:8001",
    "customer":  "http://localhost:8002",
    "order":     "http://localhost:8003",
    "payment":   "http://localhost:8004",
    "inventory": "http://localhost:8005",
}


# ──────────────────────── Product Service ────────────────────────

@app.get("/products", tags=["Product Service"])
async def get_products():
    """Get all products (proxied to Product Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICES['product']}/products")
        return response.json()


@app.get("/products/{product_id}", tags=["Product Service"])
async def get_product(product_id: int):
    """Get a product by ID (proxied to Product Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICES['product']}/products/{product_id}")
        return response.json()


@app.post("/products", tags=["Product Service"])
async def add_product(request: Request):
    """Add a new product (proxied to Product Service)."""
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['product']}/products", json=body)
        return response.json()


@app.put("/products/{product_id}", tags=["Product Service"])
async def update_product(product_id: int, request: Request):
    """Update a product (proxied to Product Service)."""
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{SERVICES['product']}/products/{product_id}", json=body)
        return response.json()


@app.delete("/products/{product_id}", tags=["Product Service"])
async def delete_product(product_id: int):
    """Delete a product (proxied to Product Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{SERVICES['product']}/products/{product_id}")
        return response.json()


# ──────────────────────── Customer Service ────────────────────────

@app.get("/customers", tags=["Customer Service"])
async def get_customers():
    """Get all customers (proxied to Customer Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICES['customer']}/customers")
        return response.json()


@app.get("/customers/{customer_id}", tags=["Customer Service"])
async def get_customer(customer_id: int):
    """Get a customer by ID (proxied to Customer Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICES['customer']}/customers/{customer_id}")
        return response.json()


@app.post("/customers", tags=["Customer Service"])
async def add_customer(request: Request):
    """Add a new customer (proxied to Customer Service)."""
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['customer']}/customers", json=body)
        return response.json()


@app.put("/customers/{customer_id}", tags=["Customer Service"])
async def update_customer(customer_id: int, request: Request):
    """Update a customer (proxied to Customer Service)."""
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{SERVICES['customer']}/customers/{customer_id}", json=body)
        return response.json()


@app.delete("/customers/{customer_id}", tags=["Customer Service"])
async def delete_customer(customer_id: int):
    """Delete a customer (proxied to Customer Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{SERVICES['customer']}/customers/{customer_id}")
        return response.json()


# ──────────────────────── Order Service ────────────────────────

@app.get("/orders", tags=["Order Service"])
async def get_orders():
    """Get all orders (proxied to Order Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICES['order']}/orders")
        return response.json()


@app.get("/orders/{order_id}", tags=["Order Service"])
async def get_order(order_id: int):
    """Get an order by ID (proxied to Order Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICES['order']}/orders/{order_id}")
        return response.json()


@app.post("/orders", tags=["Order Service"])
async def create_order(request: Request):
    """Create a new order (proxied to Order Service)."""
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['order']}/orders", json=body)
        return response.json()


@app.put("/orders/{order_id}", tags=["Order Service"])
async def update_order(order_id: int, request: Request):
    """Update an order (proxied to Order Service)."""
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{SERVICES['order']}/orders/{order_id}", json=body)
        return response.json()


@app.delete("/orders/{order_id}", tags=["Order Service"])
async def delete_order(order_id: int):
    """Delete an order (proxied to Order Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{SERVICES['order']}/orders/{order_id}")
        return response.json()


# ──────────────────────── Payment Service ────────────────────────

@app.get("/payments", tags=["Payment Service"])
async def get_payments():
    """Get all payments (proxied to Payment Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICES['payment']}/payments")
        return response.json()


@app.get("/payments/{payment_id}", tags=["Payment Service"])
async def get_payment(payment_id: int):
    """Get a payment by ID (proxied to Payment Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICES['payment']}/payments/{payment_id}")
        return response.json()


@app.post("/pay", tags=["Payment Service"])
async def make_payment(request: Request):
    """Process a payment (proxied to Payment Service)."""
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['payment']}/pay", json=body)
        return response.json()


# ──────────────────────── Inventory Service ────────────────────────

@app.get("/inventory", tags=["Inventory Service"])
async def get_inventory():
    """Get all inventory items (proxied to Inventory Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICES['inventory']}/inventory")
        return response.json()


@app.get("/inventory/{item_id}", tags=["Inventory Service"])
async def get_inventory_item(item_id: int):
    """Get an inventory item by ID (proxied to Inventory Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICES['inventory']}/inventory/{item_id}")
        return response.json()


@app.post("/inventory", tags=["Inventory Service"])
async def add_inventory(request: Request):
    """Add an inventory item (proxied to Inventory Service)."""
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['inventory']}/inventory", json=body)
        return response.json()


@app.put("/inventory/{item_id}", tags=["Inventory Service"])
async def update_inventory(item_id: int, request: Request):
    """Update an inventory item (proxied to Inventory Service)."""
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{SERVICES['inventory']}/inventory/{item_id}", json=body)
        return response.json()


@app.delete("/inventory/{item_id}", tags=["Inventory Service"])
async def delete_inventory(item_id: int):
    """Delete an inventory item (proxied to Inventory Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{SERVICES['inventory']}/inventory/{item_id}")
        return response.json()
