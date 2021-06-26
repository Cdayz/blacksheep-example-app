"""Context integration."""

from blacksheep.messages import Response
from blacksheep.server import Application
from blacksheep_context.ctx import context
from blacksheep_context.middleware import ContextMiddleware
from blacksheep_context.plugins import HeaderPlugin


class RequestId(HeaderPlugin):
    """Request id plugin for context."""

    context_key = 'request-id'
    header_key = b'X-Request-Id'
    single_value_header = True

    async def enrich_response(self, response: Response):
        """Add request-id to response headers if exists."""
        request_id = context.get(self.context_key)

        if request_id:
            response.headers.add(b'X-Request-Id', request_id)


def setup_context(app: Application):
    """Configure context."""
    app.middlewares.append(ContextMiddleware(
        plugins=[RequestId()],
    ))
