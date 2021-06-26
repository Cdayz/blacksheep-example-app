"""Prometheus integration."""

from blacksheep.server import Application
from blacksheep_prometheus import PrometheusMiddleware, metrics


def setup_prometheus(app: Application):
    """Configure prometheus metrics."""
    app.middlewares.append(PrometheusMiddleware())
    app.router.add_get('/metrics', metrics)
