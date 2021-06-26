"""All views for features service."""

from blacksheep.server import Application
from blacksheep.server.responses import json

from app.services.features import FeaturesService


async def get_features(application: str, service: FeaturesService):
    """Fetch features by application name."""
    features = await service.get_features(application)
    return json(features)


def setup_features_view(app: Application):
    """Configure routes."""
    app.router.add_get('/features.get', get_features)
