from datetime import datetime, date as dt_date
from sqlmodel import SQLModel, Field


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: int | None = Field(None, primary_key=True)
    service_id: int = Field(foreign_key="services.id")
    client_id: int = Field(foreign_key="clients.id")
    vehicle: str
    description: str
    date: dt_date = Field(default_factory=dt_date.today)
    status: str
