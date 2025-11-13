from typing import Awaitable, Callable

from fastapi import Request

from src.use_cases.auth import AuthService


class AuthMiddleware:
    def __init__(self, app, exempt_paths: list[str] | None = None) -> None:
        self.app = app
        self.exempt_paths = set(
            exempt_paths
            or [
                "/api/health",
                "/api/auth/login",
                "/api/auth/register",
                "/openapi.json",
                "/docs",
                "/redoc",
            ]
        )
        self._auth_service = AuthService()

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        if path in self.exempt_paths or path.startswith("/docs") or path.startswith("/static"):
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.lower().startswith("bearer "):
            await self._reject(send)
            return

        token = auth_header.split(" ", 1)[1]
        user_id = self._auth_service.verify_token(token)
        if user_id is None:
            await self._reject(send)
            return

        # check if user is blocked
        from datetime import datetime, timezone

        from src.infrastructure.persistence.auth import UsersRepository

        repo = UsersRepository()
        user = repo.get_by_id(user_id)
        if user is None:
            await self._reject(send)
            return
        if user.blocked_until is not None:
            now = datetime.now(timezone.utc)
            when = (
                user.blocked_until
                if user.blocked_until.tzinfo is not None
                else user.blocked_until.replace(tzinfo=timezone.utc)
            )
            if when > now:
                await self._reject(send)
                return

        scope["user_id"] = user_id
        await self.app(scope, receive, send)

    async def _reject(self, send: Callable[..., Awaitable[None]]):
        await send(
            {
                "type": "http.response.start",
                "status": 401,
                "headers": [(b"content-type", b"application/json")],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": b'{"detail":"Unauthorized"}',
            }
        )
