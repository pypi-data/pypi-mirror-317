from collections.abc import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool


class Base(DeclarativeBase):
    pass


class DatabaseConfig:
    def __init__(
        self,
        db_url_postgresql: str,
    ):
        self.db_url_postgresql = db_url_postgresql

    @property
    def engine(self):
        return create_async_engine(self.db_url_postgresql, echo=True, poolclass=NullPool)

    @property
    def async_session_maker(self):
        return async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        session = None
        try:
            async with self.async_session_maker() as session:
                yield session
        except SQLAlchemyError:
            if session:
                await session.rollback()
            raise
        else:
            if session:
                await session.close()
