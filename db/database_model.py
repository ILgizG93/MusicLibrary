from typing import AsyncGenerator

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from globals import db

db_model = declarative_base(metadata=MetaData())

DB_URL = f"postgresql://{db.username}:{db.password}@{db.host}:{db.port}/{db.name}"
DB_URL_ASYNC = f"postgresql+asyncpg://{db.username}:{db.password}@{db.host}:{db.port}/{db.name}"

def get_db_session() -> Session:
    try:
        air_engine = create_engine(DB_URL)
        session: Session = Session(air_engine)
        return session
    finally:
        session.close()

async def get_db_session_async() -> AsyncGenerator[AsyncSession, None]:
    try:
        air_engine = create_async_engine(DB_URL_ASYNC, echo=True)
        air_async_session = sessionmaker(air_engine, class_=AsyncSession, expire_on_commit=False)
        session: AsyncSession = air_async_session()
        yield session
    finally:
        await session.close()
