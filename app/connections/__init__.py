"""Connection settings."""

from blacksheep.server.application import Application

from app.connections.postgres import setup_postgres
from app.connections.redis import setup_redis


def setup_connections(app: Application):
    """Configure connections."""
    setup_postgres(app)
    setup_redis(app)
