from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from .database import get_async_session
from typing import Annotated

AsyncSessionDependency = Annotated[AsyncSession, Depends(get_async_session)]
