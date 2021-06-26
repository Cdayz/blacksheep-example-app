"""All bussiness logic grouped by services."""

from blacksheep.server import Application

from app.services.features import setup_features_service


def setup_services(app: Application):
    """Configure all services."""
    setup_features_service(app)
