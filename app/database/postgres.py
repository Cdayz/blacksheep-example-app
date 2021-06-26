"""Postgresql database abstraction layer."""

import contextlib
from typing import AsyncGenerator, Optional

import asyncpg


class PostgresConnectionPool:
    """Postgresql connection pool."""

    def __init__(self, dsn: str, **connection_settings):
        """Initialize connection pool.

        Args:
            - dsn - DSN to connect to database
            - connection_settings - keyword arguments passed to asyncpg.create_pool
        """
        self.dsn = dsn
        self.connection_settings = connection_settings

        self._pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Connect to database."""
        self._pool = await asyncpg.create_pool(dsn=self.dsn, **self.connection_settings)

    async def disconnect(self):
        """Disconnect from database."""
        if self._pool is not None:
            await self._pool.close()

    @property
    def pool(self) -> asyncpg.Pool:
        """Return current connection pool."""
        return self._pool

    @contextlib.asynccontextmanager
    async def connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """Get connection from pool."""
        async with self.pool.acquire() as conn:
            yield conn
