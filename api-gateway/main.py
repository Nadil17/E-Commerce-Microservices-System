from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
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


# ──────────────────────── Pydantic Models ────────────────────────

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None

class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str
    address: str

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class OrderCreate(BaseModel):
    customer_id: int
    product_ids: List[int]
    total_amount: float

class OrderRequest(BaseModel):
    """Used by the gateway — total_amount is auto-calculated from product prices."""
    customer_id: int
    product_ids: List[int]

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    total_amount: Optional[float] = None

class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    method: str  # e.g. "credit_card", "debit_card", "paypal"

class InventoryCreate(BaseModel):
    product_id: int
    quantity: int
    warehouse_location: str

class InventoryUpdate(BaseModel):
    quantity: Optional[int] = None
    warehouse_location: Optional[str] = None


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
async def add_product(product: ProductCreate):
    """Add a new product (proxied to Product Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['product']}/products", json=product.model_dump())
        return response.json()


@app.put("/products/{product_id}", tags=["Product Service"])
async def update_product(product_id: int, product: ProductUpdate):
    """Update a product (proxied to Product Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{SERVICES['product']}/products/{product_id}", json=product.model_dump())
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
async def add_customer(customer: CustomerCreate):
    """Add a new customer (proxied to Customer Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['customer']}/customers", json=customer.model_dump())
        return response.json()


@app.put("/customers/{customer_id}", tags=["Customer Service"])
async def update_customer(customer_id: int, customer: CustomerUpdate):
    """Update a customer (proxied to Customer Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{SERVICES['customer']}/customers/{customer_id}", json=customer.model_dump())
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
async def create_order(order: OrderRequest):
    """
    Create a new order (proxied to Order Service).

    - Validates customer_id against the Customer Service.
    - Validates every product_id against the Product Service.
    - Auto-calculates total_amount from product prices — do NOT enter it manually.
    """
    # Step 1: Validate customer exists
    async with httpx.AsyncClient() as client:
        customer_resp = await client.get(f"{SERVICES['customer']}/customers/{order.customer_id}")
        if customer_resp.status_code == 404:
            raise HTTPException(
                status_code=422,
                detail=f"Customer with ID {order.customer_id} does not exist. "
                       f"Please add the customer first before placing an order."
            )

    # Step 2: Validate product IDs and calculate total
    invalid_ids = []
    total_amount = 0.0

    async with httpx.AsyncClient() as client:
        for pid in order.product_ids:
            resp = await client.get(f"{SERVICES['product']}/products/{pid}")
            if resp.status_code == 404:
                invalid_ids.append(pid)
            else:
                product_data = resp.json()
                total_amount += product_data.get("price", 0.0)

    if invalid_ids:
        raise HTTPException(
            status_code=422,
            detail=f"The following product IDs do not exist: {invalid_ids}. "
                   f"Please add these products first before placing an order."
        )

    payload = {
        "customer_id": order.customer_id,
        "product_ids": order.product_ids,
        "total_amount": round(total_amount, 2),
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['order']}/orders", json=payload)
        return response.json()



@app.put("/orders/{order_id}", tags=["Order Service"])
async def update_order(order_id: int, order: OrderUpdate):
    """Update an order (proxied to Order Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{SERVICES['order']}/orders/{order_id}", json=order.model_dump())
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
async def make_payment(payment: PaymentCreate):
    """Process a payment (proxied to Payment Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['payment']}/pay", json=payment.model_dump())
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
async def add_inventory(item: InventoryCreate):
    """Add an inventory item (proxied to Inventory Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['inventory']}/inventory", json=item.model_dump())
        return response.json()


@app.put("/inventory/{item_id}", tags=["Inventory Service"])
async def update_inventory(item_id: int, item: InventoryUpdate):
    """Update an inventory item (proxied to Inventory Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{SERVICES['inventory']}/inventory/{item_id}", json=item.model_dump())
        return response.json()


@app.delete("/inventory/{item_id}", tags=["Inventory Service"])
async def delete_inventory(item_id: int):
    """Delete an inventory item (proxied to Inventory Service)."""
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{SERVICES['inventory']}/inventory/{item_id}")
        return response.json()
