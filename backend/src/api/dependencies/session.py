#this file will create one session per transaction
#session.py defines a dependency, not a service.
#Dependencies in FastAPI are functions, not classes, Hence no class is created here that will result in unnecessary abstraction this seesion.py is stateless it owns nothing 

import fastapi
import typing
from src.repository.database import async_db
from sqlalchemy.ext.asyncio import AsyncSession

async def get_async_session()->typing.AsyncGenerator[AsyncSession,None]:
    async with async_db.async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise