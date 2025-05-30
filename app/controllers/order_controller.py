from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.client import Client
from app.models.order import Order
from app.models.service import Service
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderResponse


class OrderController:

    @staticmethod
    async def get_orders(*, session: AsyncSession, offset: int, limit: int):
        """Get all orders with pagination"""
        orders = (
            (await session.execute(select(Order).offset(offset).limit(limit)))
            .scalars()
            .all()
        )
        result = []
        for order in orders:
            client = await session.get(Client, order.client_id)
            service = await session.get(Service, order.service_id)
            result.append(
                OrderResponse(
                    id=order.id,
                    client_id=order.client_id,
                    service_id=order.service_id,
                    vehicle=order.vehicle,
                    description=order.description,
                    status=order.status,
                    date=order.date,
                    client_name=client.name if client else "",
                    service_name=service.description if service else "",
                )
            )
        return result
        
    @staticmethod
    async def get_order_by_id(*, session: AsyncSession, order_id: int):
        """Get an order by ID"""
        order = await session.get(entity=Order, ident=order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
        return OrderResponse.model_validate(order)

    @staticmethod
    async def create_order(*, session: AsyncSession, order: OrderCreate):
        """Create a new Order"""
        try:
            db_order = Order.model_validate(order)
            print(db_order)
            print(type(db_order))
            client = await session.get(Client, order.client_id)
            if not client:
                raise HTTPException(status_code=404, detail="Client not found")
            service = await session.get(Service, order.service_id)
            if not service:
                raise HTTPException(
                    status_code=404, detail="Service not found")
            session.add(db_order)
            await session.commit()
            await session.refresh(db_order)
            ne_ord = OrderResponse.model_dump(db_order)
            print(ne_ord)
            print(type(ne_ord))
            print(type(ne_ord))
            return ne_ord
        except Exception as e:
            return e

    @staticmethod
    async def order_update(*, session: AsyncSession, order_id: int, order: OrderUpdate):
        """Update an existing order"""
        db_order = await session.get(entity=Order, ident=order_id)
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")

        update_data = order.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_order, key, value)

        session.add(db_order)
        await session.commit()
        await session.refresh(db_order)
        return OrderResponse.model_validate(db_order)

    @staticmethod
    async def delete_order(*, session: AsyncSession, order_id: int):
        """Delete an existing order"""
        db_order = await session.get(entity=Order, ident=order_id)
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")

        await session.delete(db_order)
        await session.commit()
        return {"message": "Order deleted successfully"}
