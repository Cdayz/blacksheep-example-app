"""ASGI application."""

from blacksheep.server import Application

from app.connections import setup_connections
from app.extensions import setup_extensions
from app.services import setup_services
from app.views import setup_views


def factory() -> Application:
    """Make asgi application."""
    app = Application(show_error_details=True, debug=True)

    setup_connections(app)
    setup_extensions(app)
    setup_services(app)
    setup_views(app)

    return app
