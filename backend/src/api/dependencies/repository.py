#generates FastAPI dependencies that automatically inject a DB session into a repository

from src.api.dependencies.session import get_async_session
import typing
from src.repository.crud.accounts import BaseCRUDRepository
from sqlalchemy.ext.asyncio import AsyncSession

import typing

import fastapi
from sqlalchemy.ext.asyncio import (
    async_sessionmaker as sqlalchemy_async_sessionmaker,
    AsyncSession as SQLAlchemyAsyncSession,
)

from src.api.dependencies.session import get_async_session
from src.repository.crud.base import BaseCRUDRepository


def get_repository(
    repo_type: typing.Type[BaseCRUDRepository],
) -> typing.Callable[[SQLAlchemyAsyncSession], BaseCRUDRepository]:
    def _get_repo(
        async_session: SQLAlchemyAsyncSession = fastapi.Depends(get_async_session),
    ) -> BaseCRUDRepository:
        return repo_type(async_session=async_session)

    return _get_repo