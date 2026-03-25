from fastapi import FastAPI, HTTPException
from models import CustomerCreate, CustomerUpdate

app = FastAPI(
    title="Customer Service",
    description="Microservice for managing customers in the E-Commerce system",
    version="1.0.0",
)

# In-memory storage
customers = []
id_counter = 0


@app.get("/customers", tags=["Customers"])
def get_customers():
    """Retrieve all customers."""
    return customers


@app.get("/customers/{customer_id}", tags=["Customers"])
def get_customer(customer_id: int):
    """Retrieve a single customer by their ID."""
    for customer in customers:
        if customer["id"] == customer_id:
            return customer
    raise HTTPException(status_code=404, detail="Customer not found")


@app.post("/customers", status_code=201, tags=["Customers"])
def add_customer(customer: CustomerCreate):
    """Register a new customer."""
    global id_counter
    id_counter += 1
    new_customer = {"id": id_counter, **customer.model_dump()}
    customers.append(new_customer)
    return {"message": "Customer added successfully", "data": new_customer}


@app.put("/customers/{customer_id}", tags=["Customers"])
def update_customer(customer_id: int, customer: CustomerUpdate):
    """Update an existing customer by their ID."""
    for idx, existing in enumerate(customers):
        if existing["id"] == customer_id:
            update_data = customer.model_dump(exclude_unset=True)
            customers[idx] = {**existing, **update_data}
            return {"message": "Customer updated successfully", "data": customers[idx]}
    raise HTTPException(status_code=404, detail="Customer not found")


@app.delete("/customers/{customer_id}", tags=["Customers"])
def delete_customer(customer_id: int):
    """Delete a customer by their ID."""
    for idx, existing in enumerate(customers):
        if existing["id"] == customer_id:
            customers.pop(idx)
            return {"message": "Customer deleted successfully"}
    raise HTTPException(status_code=404, detail="Customer not found")
