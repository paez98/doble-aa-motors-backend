from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.client import Client
from sqlmodel import select
from app.schemas.client_schema import ClientCreate, ClientUpdate, ClientResponse


class ClientController:
    """
    Client service class to handle client-related operations.
    """

    @staticmethod
    async def get_client(*, session: AsyncSession, offset: int, limit: int):
        """
        Get all clients.
        """
        clients = (
            (await session.execute(select(Client).offset(offset).limit(limit)))
            .scalars()
            .all()
        )
        return [ClientResponse.model_validate(client) for client in clients]

    @staticmethod
    async def get_client_by_id(*, session: AsyncSession, client_id: int):
        """
        Get a client by ID.
        """
        client = await session.get(entity=Client, ident=client_id)
        if not client:
            raise ValueError("Client not found")

        return ClientResponse.model_validate(client)

    @staticmethod
    async def client_create(*, client: ClientCreate, session: AsyncSession):
        """
        Create a new client.
        """
        db_client = Client.model_validate(client)
        session.add(db_client)
        await session.commit()
        await session.refresh(db_client)
        return ClientResponse.model_validate(db_client)

    @staticmethod
    async def client_update(
        *, session: AsyncSession, client_id: int, client: ClientUpdate
    ):
        """
        Update an existing client.
        """
        db_client = await session.get(entity=Client, ident=client_id)
        if not db_client:
            raise ValueError("Client not found")

        update_data = client.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_client, key, value)

        session.add(db_client)
        await session.commit()
        await session.refresh(db_client)
        return ClientResponse.model_validate(db_client)

    @staticmethod
    async def client_delete(*, session: AsyncSession, client_id: int):
        """
        Delete a client by ID.
        """
        db_client = await session.get(entity=Client, ident=client_id)
        if not db_client:
            raise ValueError("Client not found")

        await session.delete(db_client)
        await session.commit()
        return {"message": "Client deleted successfully"}
