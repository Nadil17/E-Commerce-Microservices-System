from fastapi import FastAPI, HTTPException
from models import InventoryCreate, InventoryUpdate

app = FastAPI(
    title="Inventory Service",
    description="Microservice for managing inventory / stock in the E-Commerce system",
    version="1.0.0",
)

# In-memory storage
inventory = []
id_counter = 0


@app.get("/inventory", tags=["Inventory"])
def get_inventory():
    """Retrieve all inventory items."""
    return inventory


@app.get("/inventory/{item_id}", tags=["Inventory"])
def get_inventory_item(item_id: int):
    """Retrieve a single inventory item by its ID."""
    for item in inventory:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Inventory item not found")


@app.post("/inventory", status_code=201, tags=["Inventory"])
def add_inventory(item: InventoryCreate):
    """Add a new inventory record."""
    global id_counter
    id_counter += 1
    new_item = {"id": id_counter, **item.model_dump()}
    inventory.append(new_item)
    return {"message": "Inventory item added successfully", "data": new_item}


@app.put("/inventory/{item_id}", tags=["Inventory"])
def update_inventory(item_id: int, item: InventoryUpdate):
    """Update an existing inventory item."""
    for idx, existing in enumerate(inventory):
        if existing["id"] == item_id:
            update_data = item.model_dump(exclude_unset=True)
            inventory[idx] = {**existing, **update_data}
            return {"message": "Inventory item updated successfully", "data": inventory[idx]}
    raise HTTPException(status_code=404, detail="Inventory item not found")


@app.delete("/inventory/{item_id}", tags=["Inventory"])
def delete_inventory(item_id: int):
    """Delete an inventory item by its ID."""
    for idx, existing in enumerate(inventory):
        if existing["id"] == item_id:
            inventory.pop(idx)
            return {"message": "Inventory item deleted successfully"}
    raise HTTPException(status_code=404, detail="Inventory item not found")
