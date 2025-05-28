from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.config.database import get_async_session
from app.schemas.client_schema import ClientCreate, ClientUpdate, ClientResponse
from app.controllers.client_controller import ClientController


client_router = APIRouter()


@client_router.get("/", response_model=list[ClientResponse])
async def get_client(
    *,
    session: AsyncSession = Depends(get_async_session),
    offset: int = 0,
    limit: int = 100,
):
    """
    Get all clients.
    """
    clients = await ClientController.get_client(
        session=session, offset=offset, limit=limit
    )
    return [client for client in clients]


@client_router.get("/{client_id}", response_model=ClientResponse)
async def get_client_by_id(
    *, session: AsyncSession = Depends(get_async_session), client_id: int
):
    """
    Get a client by ID.
    """
    client = await ClientController.get_client_by_id(
        session=session, client_id=client_id
    )
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client


@client_router.post(
    "/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED
)
async def create_client(
    *,
    client: ClientCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Create a new client.
    """
    db_client = await ClientController.client_create(client=client, session=session)

    return db_client


@client_router.patch("/{client_id}", response_model=ClientResponse)
async def update_client(
    *,
    client_id: int,
    client: ClientUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update a client.
    """
    db_client = await ClientController.client_update(
        session=session, client_id=client_id, client=client
    )

    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    return db_client


@client_router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    *, client_id: int, session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a client.
    """
    db_client = await ClientController.client_delete(
        session=session, client_id=client_id
    )

    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    return True
