from app.controllers.pay_controller import PayController
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends
from app.config.database import get_async_session
from app.schemas.pay_schema import PayCreate, PayResponse


pay_router = APIRouter()


@pay_router.get("/", response_model=list[PayResponse])
async def get_pays(
    *,
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session),
):
    """Get all pays with pagination"""
    return await PayController.get_pays(session=session, offset=offset, limit=limit)


@pay_router.get("/{pay_id}", response_model=PayResponse)
async def get_pay_by_id(*, session=Depends(get_async_session), pay_id: int):
    """Get a pay by ID"""

    return await PayController.get_pay_by_id(session=session, pay_id=pay_id)


@pay_router.post("/", response_model=PayResponse, status_code=201)
async def create_pay(*, session=Depends(get_async_session), pay: PayCreate):
    """Create a new pay"""
    return await PayController.create_pay(session=session, pay=pay)


@pay_router.patch("/{pay_id}", response_model=PayResponse)
async def update_pay(
    *, session=Depends(get_async_session), pay_id: int, pay: PayCreate
):
    """Update a pay by ID"""
    return await PayController.update_pay(session=session, pay_id=pay_id, pay=pay)
