from pydantic import BaseModel
from typing import Optional


class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    method: str  # e.g. "credit_card", "debit_card", "paypal"


class PaymentUpdate(BaseModel):
    status: Optional[str] = None
