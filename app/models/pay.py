from datetime import date
from sqlmodel import Field, SQLModel


class Pay(SQLModel, table=True):
    __tablename__ = "pays"
    id: int = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="clients.id")
    service_id: int = Field(foreign_key="services.id")
    amount: float = Field()
    method: str = Field(max_length=50)
    reference: str | None = Field(default=None, max_length=50)
    payment_date: date = Field()
