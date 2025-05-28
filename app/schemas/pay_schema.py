from pydantic import BaseModel, Field
from datetime import date as dt


class PayBase(BaseModel):
    client_id: int = Field(..., description="ID of the client making the payment")
    service_id: int = Field(..., description="ID of the service being paid for")
    amount: float = Field(..., description="Amount of the payment")
    method: str = Field(..., max_length=50, description="Payment method used")
    reference: str | None = Field(
        default=None, max_length=50, description="Reference for the payment"
    )
    payment_date: dt = Field(..., description="Date of the payment")


class PayCreate(PayBase):
    """Schema for creating a new payment"""

    pass


class PayResponse(PayBase):
    """Schema for returning payment details"""

    client_name: str
    service_name: str
    id: int = Field(..., description="Unique identifier of the payment")

    class Config:
        from_attributes = True
