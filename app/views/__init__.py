"""All application views."""

from blacksheep.server.application import Application

from app.views.features import setup_features_view


def setup_views(app: Application):
    """Configure all views into application."""
    setup_features_view(app)
