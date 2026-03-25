from pydantic import BaseModel
from typing import Optional


class InventoryCreate(BaseModel):
    product_id: int
    quantity: int
    warehouse_location: str


class InventoryUpdate(BaseModel):
    quantity: Optional[int] = None
    warehouse_location: Optional[str] = None
