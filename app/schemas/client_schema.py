from pydantic import BaseModel, Field
from typing import Optional


class ClientBase(BaseModel):
    name: str = Field(
        ...,
        title="Client Name",
        description="Name of the client",
        example="Alissa Paez",
    )

    phone: str = Field(
        ...,
        title="Client Phone",
        description="Phone number of the client",
        example="01213456789",
    )
    address: Optional[str] = Field(
        None, title="Client Address", description="Address of the client"
    )


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        title="Client Name",
        description="Name of the client",
        example="Alissa Paez",
    )

    phone: Optional[str] = Field(
        None,
        title="Client Phone",
        description="Phone number of the client",
        example="01213456789",
    )

    address: Optional[str] = Field(
        None, title="Client Address", description="Address of the client"
    )


class ClientResponse(ClientBase):
    id: int = Field(..., example=1)

    class Config:
        from_attributes = True
