from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as dt_date


class OrderBase(BaseModel):
    client_id: int = Field(
        ...,
        title="Client ID",
        description="ID of the client placing the order",
        example=1,
    )
    service_id: int = Field(
        ...,
        title="Service ID",
        description="ID of the service being ordered",
        example=1,
    )

    vehicle: str = Field(
        ...,
        title="Vehicle",
        description="Vehicle associated with the order",
        example="Chevrolet Spark",
    )

    description: str = Field(
        ...,
        title="Description",
        description="Description of the order",
        example="Cambio de aceite y filtro de aceite",
    )
    status: str = Field(
        ..., title="Status", description="Order status", example="Pendiente"
    )


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    service_id: Optional[int] = Field(
        None,
        title="Service ID",
        description="ID of the service being ordered",
        example=1,
    )
    client_id: Optional[int] = Field(
        None,
        title="Client ID",
        description="ID of the client placing the order",
        example=1,
    )
    vehicle: Optional[str] = Field(
        None,
        title="Vehicle",
        description="Vehicle associated with the order",
        example="Chevrolet Spark",
    )
    description: Optional[str] = Field(
        None,
        title="Description",
        description="Description of the order",
        example="Cambio de aceite y filtro de aceite",
    )
    status: Optional[str] = Field(
        None, title="Status", description="Order status", example="Pendiente"
    )


class OrderResponse(OrderBase):
    client_name: str
    service_name: str
    date: dt_date
    id: int = Field(..., example=1)

    class Config:
        from_attributes = True
