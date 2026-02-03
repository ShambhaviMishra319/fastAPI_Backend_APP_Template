#this file set up the engine , create session and connrect to databae to perfore future database activity

#pool is:
#A set of already-open connections
#Sitting in memory
#Reused across requests

#One engine per app. Always.

#Session represent One transaction

#MENTAL MODEL :session borrows a connection from pool via engine
 

import pydantic
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncEngine,AsyncSession,async_sessionmaker,create_async_engine
from sqlalchemy.pool import Pool,QueuePool
from src.config.manager import settings

class AsyncDatabase:
    #Eager initialization
    #One action. One invariant.
    def __init__(self):

        self.postgres_uri:pydantic.PostgresDsn=pydantic.PostgresDsn(
             url=f"{settings.DB_POSTGRES_SCHEMA}://{settings.DB_POSTGRES_USENRAME}:{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:{settings.DB_POSTGRES_PORT}/{settings.DB_POSTGRES_NAME}",
             scheme=settings.DB_POSTGRES_SCHEMA,
        )

        self.async_engine:AsyncEngine=create_async_engine(
            url=self.set_async_db_uri,
            echo=settings.IS_DB_ECHO_LOG,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_POOL_OVERFLOW,
            poolclass=QueuePool

        )

    @property
    #setting syncronous database drivers to asyncronous as postgres defaults to sync,and async requires "postgressql+asyncpg"
    def set_async_db_uri(self)->str | pydantic.PostgresDsn:
        return self.postgres_async_uri.replace("postgresql://","postgresql+asyncpg://")


async_db:AsyncDatabase=AsyncDatabase()