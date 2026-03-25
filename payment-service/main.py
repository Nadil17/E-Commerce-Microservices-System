from fastapi import FastAPI, HTTPException
from models import PaymentCreate

app = FastAPI(
    title="Payment Service",
    description="Microservice for processing payments in the E-Commerce system",
    version="1.0.0",
)

# In-memory storage
payments = []
id_counter = 0


@app.get("/payments", tags=["Payments"])
def get_payments():
    """Retrieve all payment records."""
    return payments


@app.get("/payments/{payment_id}", tags=["Payments"])
def get_payment(payment_id: int):
    """Retrieve a single payment by its ID."""
    for payment in payments:
        if payment["id"] == payment_id:
            return payment
    raise HTTPException(status_code=404, detail="Payment not found")


@app.post("/pay", status_code=201, tags=["Payments"])
def make_payment(payment: PaymentCreate):
    """Process a new payment."""
    global id_counter
    id_counter += 1
    new_payment = {
        "id": id_counter,
        "status": "completed",
        **payment.model_dump(),
    }
    payments.append(new_payment)
    return {"message": "Payment processed successfully", "data": new_payment}
