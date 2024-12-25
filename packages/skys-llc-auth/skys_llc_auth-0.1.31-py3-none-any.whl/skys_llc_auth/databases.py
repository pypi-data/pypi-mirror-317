import enum
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class ClientState(enum.Enum):
    # UNOPENED:
    #   The client has been instantiated, but has not been used to send a request,
    #   or been opened by entering the context of a `with` block.
    UNOPENED = 1
    # OPENED:
    #   The client has either sent a request, or is within a `with` block.
    OPENED = 2
    # CLOSED:
    #   The client has either exited the `with` block, or `close()` has
    #   been called explicitly.
    CLOSED = 3


class DatabaseConfig:
    def __init__(
        self,
        db_url_postgresql: str,
    ):
        self.db_url_postgresql = db_url_postgresql
        self.state: ClientState = ClientState.UNOPENED
        self._session = None

    @property
    def engine(self):
        return create_async_engine(self.db_url_postgresql, echo=True)

    @property
    def async_session_maker(self):
        return async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        # try:
        async with self.async_session_maker() as session:
            self.state = ClientState.OPENED
            self._session = session
            yield self._session

        # except:  # noqa: E722
        #     if self._session:
        #         await self._session.rollback()
        #         await self._session.close()
        #         self.state = ClientState.CLOSED
        #         raise
        # else:
        #     await self._session.close()
        #     self.state = ClientState.CLOSED
