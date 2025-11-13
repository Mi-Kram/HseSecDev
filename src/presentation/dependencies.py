from functools import wraps
from typing import Annotated, Callable

from fastapi import Depends, HTTPException, Request, status

from src.use_cases.auth import AuthService


def get_current_user_id(request: Request, auth_service: AuthService = Depends()) -> int:
    """Extract user_id from JWT token in Authorization header"""
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing or invalid authorization header",
        )

    token = auth_header.split(" ", 1)[1]
    user_id = auth_service.verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

    return user_id


# Type alias for dependency injection
CurrentUserID = Annotated[int, Depends(get_current_user_id)]


def authorize(func: Callable):
    @wraps(func)
    async def wrapper(user_id: CurrentUserID, *args, **kwargs):
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="missing or invalid authorization header",
            )
        return await func(*args, **kwargs)

    return wrapper
