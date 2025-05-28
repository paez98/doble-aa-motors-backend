from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException
from app.models.pay import Pay
from app.models.client import Client
from app.models.service import Service
from app.schemas.pay_schema import PayCreate, PayResponse


class PayController:

    @staticmethod
    async def get_pays(session: AsyncSession, offset: int = 0, limit: int = 100):
        """Get all pays with pagination"""
        pays = (
            (await session.execute(select(Pay).offset(offset).limit(limit)))
            .scalars()
            .all()
        )
        result = []
        for pay in pays:
            client = await session.get(Client, pay.client_id)
            service = await session.get(Service, pay.service_id)
            result.append(
                PayResponse(
                    id=pay.id,
                    client_id=pay.client_id,
                    service_id=pay.service_id,
                    amount=pay.amount,
                    method=pay.method,
                    payment_date=pay.payment_date,
                    client_name=client.name if client else "",
                    service_name=service.description if service else "",
                )
            )
        return result

    @staticmethod
    async def get_pay_by_id(session: AsyncSession, pay_id: int):
        """Get a pay by ID"""
        client = await session.get(Client, pay_id)
        service = await session.get(Service, pay_id)
        pay = await session.get(entity=Pay, ident=pay_id)
        if not pay:
            raise HTTPException(status_code=404, detail="Pay not found")
        return PayResponse(
            id=pay.id,
            client_id=pay.client_id,
            service_id=pay.service_id,
            amount=pay.amount,
            method=pay.method,
            payment_date=pay.payment_date,
            client_name=client.name if client else "",
            service_name=service.description if service else "",
        )

    @staticmethod
    async def create_pay(session: AsyncSession, pay: PayCreate):
        """Create a new pay"""
        new_pay = Pay.model_validate(pay)
        client = await session.get(Client, new_pay.client_id)
        service = await session.get(Service, new_pay.service_id)
        if not client or not service:
            raise HTTPException(status_code=404, detail="Client or service not found")
        client_name = client.name if client else ""
        service_name = service.description if service else ""
        session.add(new_pay)
        await session.commit()
        await session.refresh(new_pay)
        return PayResponse(
            id=new_pay.id,
            client_id=new_pay.client_id,
            service_id=new_pay.service_id,
            amount=new_pay.amount,
            method=new_pay.method,
            payment_date=new_pay.payment_date,
            client_name=client_name,
            service_name=service_name,
        )

    @staticmethod
    async def update_pay(*, session: AsyncSession, pay_id: int, pay: PayCreate):
        """Update a pay by ID"""
        existing_pay = await session.get(Pay, pay_id)
        if not existing_pay:
            raise HTTPException(status_code=404, detail="Pay not found")
        updated_pay = existing_pay.model_validate(pay)
        existing_pay.client_id = updated_pay.client_id
        existing_pay.service_id = updated_pay.service_id
        existing_pay.amount = updated_pay.amount
        existing_pay.method = updated_pay.method
        existing_pay.payment_date = updated_pay.payment_date
        client = await session.get(Client, updated_pay.client_id)
        service = await session.get(Service, updated_pay.service_id)
        client_name = client.name if client else ""
        service_name = service.description if service else ""
        await session.commit()
        await session.refresh(existing_pay)
        return PayResponse(
            id=existing_pay.id,
            client_id=existing_pay.client_id,
            service_id=existing_pay.service_id,
            amount=existing_pay.amount,
            method=existing_pay.method,
            payment_date=existing_pay.payment_date,
            client_name=client_name,
            service_name=service_name,
        )
