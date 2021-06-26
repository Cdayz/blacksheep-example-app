"""Postgres connection settings."""

from blacksheep.server import Application

from app import settings
from app.database import PostgresConnectionPool


async def init_postgres(app: Application):
    """Configure postgres connection pool for application."""
    postgres = PostgresConnectionPool(
        dsn=settings.DATABASE_DSN,
        min_size=10,
        max_size=10,
        max_inactive_connection_lifetime=600,  # 600 seconds lifetime for idle connections
    )

    await postgres.connect()
    app.services.add_instance(postgres, PostgresConnectionPool)


async def close_postgres(app: Application):
    """Destroy postgres connection pool on app exit."""
    await app.services[PostgresConnectionPool].disconnect()


def setup_postgres(app: Application):
    """Configure postgres connection."""
    app.on_start += init_postgres
    app.on_stop += close_postgres
