from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.config.database import get_async_session
from app.models.client import Client
from app.models.order import Order
from app.models.service import Service
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderResponse
from app.controllers.order_controller import OrderController


order_router = APIRouter()


@order_router.get("/", response_model=list[OrderResponse])
async def get_orders(
    *,
    session: AsyncSession = Depends(get_async_session),
    offset: int = 0,
    limit: int = 100,
):
    """Get all orders"""
    orders = await OrderController.get_orders(
        session=session, offset=offset, limit=limit
    )
    return orders


@order_router.get("/{order_id}", response_model=OrderResponse)
async def get_order_bi_id(
    *, session: AsyncSession = Depends(get_async_session), order_id: int
):
    """Create a new Order"""

    order = await OrderController.get_order_by_id(session=session, order_id=order_id)

    return order


@order_router.post(
    "/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED
)
async def create_order(
    *, session: AsyncSession = Depends(get_async_session), order: OrderCreate
):
    """Create a new Order"""

    db_order = await OrderController.create_order(session=session, order=order)
    return db_order


@order_router.patch("/{order_id}", response_model=OrderResponse)
async def order_update(
    *,
    session: AsyncSession = Depends(get_async_session),
    order_id: int,
    order: OrderUpdate,
):
    """Update an existing order"""
    db_order = await OrderController.order_update(
        session=session, order_id=order_id, order=order
    )
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@order_router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    *, session: AsyncSession = Depends(get_async_session), order_id: int
):
    """Delete an order by ID"""
    await OrderController.delete_order(session=session, order_id=order_id)
    return {"message": "Order deleted successfully"}
