from pydantic import BaseModel, Field
from typing import Optional


class ServiceBase(BaseModel):

    description: str = Field(
        ...,
        title="Service Description",
        description="Description of the service",
        example="Cambio de croche",
    )
    price: float = Field(
        ...,
        title="Service Price",
        description="Price of the service",
        example=50.0,
    )


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    description: Optional[str] = Field(
        None,
        title="Service Description",
        description="Description of the service",
        example="Cambio de croche",
    )

    price: Optional[float] = Field(
        None,
        title="Service Price",
        description="Description of the service",
        example=50.5,
    )


class ServiceResponse(ServiceBase):
    id: int = Field(..., example=1)

    class Config:
        from_attributes = True
