"""All used blacksheep extensions."""

from blacksheep.server import Application

from app.extensions.context import setup_context
from app.extensions.prometheus import setup_prometheus


def setup_extensions(app: Application):
    """Configure extensions."""
    setup_context(app)
    setup_prometheus(app)
