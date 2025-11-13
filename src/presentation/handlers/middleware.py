from typing import Any, Awaitable, Callable

from fastapi.responses import PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Rejects requests whose Content-Length exceeds the configured limit.

    This middleware relies on the Content-Length header. If the header is
    missing, the request is allowed to proceed.
    """

    def __init__(self, app: Callable[..., Awaitable[Any]], max_body_size: int) -> None:
        super().__init__(app)
        self.max_body_size = max_body_size

    async def dispatch(self, request, call_next):  # type: ignore[override]
        content_length = request.headers.get("content-length")

        if content_length and content_length.isdigit():
            if int(content_length) > self.max_body_size:
                return PlainTextResponse("Request payload too large", status_code=413)

        return await call_next(request)
