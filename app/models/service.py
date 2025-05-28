from typing import Optional
from sqlmodel import SQLModel, Field


class Service(SQLModel, table=True):
    __tablename__ = "services"

    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    price: float
