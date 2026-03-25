from pydantic import BaseModel
from typing import List, Optional


class OrderCreate(BaseModel):
    customer_id: int
    product_ids: List[int]
    total_amount: float


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    total_amount: Optional[float] = None
