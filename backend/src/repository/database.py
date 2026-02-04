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
#AsyncSession=one db transaction , async_sessionmaker= a factory that creates AsyncSession
#We NEVER store AsyncSession in an init time because that would create one global session and will cause random transaction leaks
from sqlalchemy.ext.asyncio import AsyncEngine,create_async_engine,AsyncSession,async_sessionmaker
from src.config.manager import settings
from sqlalchemy.pool import Pool

class AsyncDatabase:
    #Eager initialization
    #One action. One invariant.
    def __init__(self):

        self.postgres_url:pydantic.PostgresDsn = pydantic.PostgresDsn(
        url=f"{settings.DB_POSTGRES_SCHEMA}://{settings.DB_POSTGRES_USERNAME}:{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:{settings.DB_POSTGRES_PORT}/{settings.DB_POSTGRES_NAME}",
        scheme=f"{settings.DB_POSTGRES_SCHEMA}"
        )

        self.async_engine:AsyncEngine=create_async_engine(
            url=self.set_async_db_uri,
            echo=settings.IS_DB_ECHO_LOG,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_POOL_OVERFLOW
        )

        #session factory 
        self.async_session:async_sessionmaker=async_sessionmaker(bind=self.async_engine,expire_on_commit=False)

    @property
    def set_async_db_uri(self)->str | pydantic.PostgresDsn:
        return self.postgres_url.replace("postgresql://","postgresql+asyncpg://")
        

async_db:AsyncDatabase=AsyncDatabase()