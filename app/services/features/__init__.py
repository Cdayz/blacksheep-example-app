"""Features service and all related types."""

from blacksheep.server import Application

from app.services.features.service import FeaturesService
from app.services.features.types import AppFeatures


def setup_features_service(app: Application):
    """Configure features service."""
    app.services.add_transient(FeaturesService)


__all__ = [
    'AppFeatures',
    'FeaturesService',
    'setup_features_service',
]
