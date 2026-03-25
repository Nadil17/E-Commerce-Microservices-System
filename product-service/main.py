from fastapi import FastAPI, HTTPException
from models import ProductCreate, ProductUpdate

app = FastAPI(
    title="Product Service",
    description="Microservice for managing products in the E-Commerce system",
    version="1.0.0",
)

# In-memory storage
products = []
id_counter = 0


@app.get("/products", tags=["Products"])
def get_products():
    """Retrieve all products."""
    return products


@app.get("/products/{product_id}", tags=["Products"])
def get_product(product_id: int):
    """Retrieve a single product by its ID."""
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products", status_code=201, tags=["Products"])
def add_product(product: ProductCreate):
    """Add a new product."""
    global id_counter
    id_counter += 1
    new_product = {"id": id_counter, **product.model_dump()}
    products.append(new_product)
    return {"message": "Product added successfully", "data": new_product}


@app.put("/products/{product_id}", tags=["Products"])
def update_product(product_id: int, product: ProductUpdate):
    """Update an existing product by its ID."""
    for idx, existing in enumerate(products):
        if existing["id"] == product_id:
            update_data = product.model_dump(exclude_unset=True)
            products[idx] = {**existing, **update_data}
            return {"message": "Product updated successfully", "data": products[idx]}
    raise HTTPException(status_code=404, detail="Product not found")


@app.delete("/products/{product_id}", tags=["Products"])
def delete_product(product_id: int):
    """Delete a product by its ID."""
    for idx, existing in enumerate(products):
        if existing["id"] == product_id:
            products.pop(idx)
            return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")
