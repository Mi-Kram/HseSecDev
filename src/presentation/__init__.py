from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from src.domain.errors import WishNotFoundError

from .controllers import auth, health, wish_list
from .handlers import exceptions
from .handlers.middleware import RequestSizeLimitMiddleware

# from .middleware.auth import AuthMiddleware
from .middleware.security_middleware import (
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
    SecurityLoggingMiddleware,
)
from .models.api_error import ApiError


def add_presentaion(app: FastAPI):
    app.add_exception_handler(ApiError, exceptions.api_error_handler)
    app.add_exception_handler(ValueError, exceptions.value_error_handler)
    app.add_exception_handler(RequestValidationError, exceptions.request_validation_error_handler)
    app.add_exception_handler(ValidationError, exceptions.validation_error_handler)
    app.add_exception_handler(WishNotFoundError, exceptions.wish_not_found_handler)
    app.add_exception_handler(HTTPException, exceptions.http_exception_handler)

    app.add_middleware(SecurityLoggingMiddleware)
    app.add_middleware(RateLimitMiddleware, requests_per_minute=100, burst_limit=50)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestSizeLimitMiddleware, max_body_size=1_048_576)
    # app.add_middleware(AuthMiddleware)

    # Routers
    app.include_router(health.router, prefix="/api")
    app.include_router(auth.router, prefix="/api/auth")
    app.include_router(wish_list.router, prefix="/api/wishes")
