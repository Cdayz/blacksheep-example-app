"""Redis connection settings."""

from blacksheep.server import Application

from app import settings
from app.database import RedisConnectionPool


async def init_redis(app: Application):
    """Configure redis connection pool for application."""
    redis = RedisConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db_num=settings.REDIS_DB_NUM,
        username=settings.REDIS_USER,
        password=settings.REDIS_PASS,
        is_sentinel=settings.REDIS_IS_SENTINEL,
        sentinel_master=settings.REDIS_SENTINEL_MASTER,
    )

    await redis.connect()
    app.services.add_instance(redis, RedisConnectionPool)


async def close_redis(app: Application):
    """Destroy redis connection pool on app exit."""
    await app.services[RedisConnectionPool].disconnect()


def setup_redis(app: Application):
    """Configure redis."""
    app.on_start += init_redis
    app.on_stop += close_redis
