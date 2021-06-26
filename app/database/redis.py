"""Redis database abstraction layer."""

import contextlib
from typing import AsyncGenerator, Optional

import aioredis


class RedisConnectionPool:
    """Redis connection pool."""

    def __init__(
        self,
        host: str,
        port: int,
        db_num: int,
        username: Optional[str],
        password: Optional[str],
        is_sentinel: bool,
        sentinel_master: str,
    ):
        """Initialize redis."""
        self.host = host
        self.port = port
        self.db_num = db_num
        self.username = username
        self.password = password
        self.is_sentinel = is_sentinel
        self.sentinel_master = sentinel_master

        self._conn: Optional[aioredis.ConnectionsPool] = None

    async def connect(self):
        """Connect to redis."""
        if self.is_sentinel:
            sentinel_pool = await aioredis.sentinel.create_sentinel_pool(
                [(self.host, self.port)],
                db=self.db_num,
                password=self.password,
            )
            self._pool = sentinel_pool.master_for(self.sentinel_master)
        else:
            self._pool = await aioredis.create_pool((self.host, self.port), db=self.db_num, password=self.password)

    async def disconnect(self):
        """Disconnect from redis."""
        self._pool.close()
        await self._pool.wait_closed()

    @property
    def pool(self) -> aioredis.ConnectionsPool:
        """Return current connection pool."""
        return self._pool

    @contextlib.asynccontextmanager
    async def connection(self) -> AsyncGenerator[aioredis.Redis, None]:
        """Get redis client from connection pool."""
        yield aioredis.Redis(self.pool)
