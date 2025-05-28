from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.config.database import get_async_session
from app.models.service import Service
from app.schemas.service_schema import ServiceCreate, ServiceUpdate, ServiceResponse
from app.controllers.service_controller import ServiceController


service_router = APIRouter()


@service_router.get("/", response_model=list[ServiceResponse])
async def get_service(
    *,
    session: AsyncSession = Depends(get_async_session),
    offset: int = 0,
    limit: int = 100,
):
    """Get all services with pagination"""
    services = await ServiceController.get_services(
        session=session, offset=offset, limit=limit
    )
    return services


@service_router.get("/{service_id}", response_model=ServiceResponse)
async def get_service_by_id(
    *, session: AsyncSession = Depends(get_async_session), service_id: int
):
    """Get a service by ID"""
    service = await ServiceController.get_service_by_id(
        session=session, service_id=service_id
    )
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return service


@service_router.post(
    "/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED
)
async def create_service(
    *, service: ServiceCreate, session: AsyncSession = Depends(get_async_session)
):
    """Create a new service"""
    new_service = await ServiceController.create_service(
        service=service, session=session
    )
    if not new_service:
        raise HTTPException(status_code=400, detail="Service creation failed")

    return new_service


@service_router.patch("/{service_id}", response_model=ServiceResponse)
async def update_service(
    *,
    session: AsyncSession = Depends(get_async_session),
    service_id: int,
    service: ServiceUpdate,
):
    """Update an existing service by ID"""
    service_db = await session.get(entity=Service, ident=service_id)

    if not service_db:
        raise HTTPException(status_code=404, detail="Service not found")

    service_data = service.model_dump(exclude_unset=True)

    for key, value in service_data.items():
        setattr(service_db, key, value)

    session.add(service_db)
    await session.commit()
    await session.refresh(service_db)
    return ServiceResponse.model_validate(service_db)


@service_router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    *, session: AsyncSession = Depends(get_async_session), service_id: int
):
    """Delete a service by ID"""
    await ServiceController.delete_service(session=session, service_id=service_id)

    return {"detail": "Service deleted successfully"}
