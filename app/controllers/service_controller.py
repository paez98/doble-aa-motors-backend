from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.config.database import get_async_session
from app.models.service import Service
from app.schemas.service_schema import ServiceCreate, ServiceUpdate, ServiceResponse


class ServiceController:

    @staticmethod
    async def get_services(
        *,
        session: AsyncSession,
        offset: int,
        limit: int,
    ):
        """Get all services with pagination"""

        services = (
            (await session.execute(select(Service).offset(offset).limit(limit)))
            .scalars()
            .all()
        )

        return [ServiceResponse.model_validate(service) for service in services]

    @staticmethod
    async def get_service_by_id(*, session: AsyncSession, service_id: int):
        """Get a service by ID"""
        service = await session.get(entity=Service, ident=service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")

        return ServiceResponse.model_validate(service)

    @staticmethod
    async def create_service(*, service: ServiceCreate, session: AsyncSession):
        """Create a new service"""
        new_service = Service.model_validate(service)
        session.add(new_service)
        await session.commit()
        await session.refresh(new_service)
        return ServiceResponse.model_validate(new_service)

    @staticmethod
    async def update_service(
        *,
        session: AsyncSession,
        service_id: int,
        service: ServiceUpdate,
    ):
        """Update an existing service by ID"""
        db_service = await session.get(entity=Service, ident=service_id)
        if not db_service:
            raise HTTPException(status_code=404, detail="Service not found")

        update_data = service.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_service, key, value)

        session.add(db_service)
        await session.commit()
        await session.refresh(db_service)
        return ServiceResponse.model_validate(db_service)

    @staticmethod
    async def delete_service(*, session: AsyncSession, service_id: int):
        """Delete a service by ID"""
        db_service = await session.get(entity=Service, ident=service_id)
        if not db_service:
            raise HTTPException(status_code=404, detail="Service not found")

        await session.delete(db_service)
        await session.commit()
        return {"message": "Service deleted successfully"}
