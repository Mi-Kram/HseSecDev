from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.domain.errors import WishNotFoundError
from src.presentation.models.api_error import ApiError
from src.presentation.models.rfc7807 import create_problem_detail, create_security_problem_detail


async def api_error_handler(request: Request, ex: ApiError):
    problem = create_problem_detail(
        status=ex.status,
        title="API Error",
        detail=ex.message,
        type_="https://wishlist.example.com/problems/api-error",
        instance=str(request.url),
    )
    return JSONResponse(
        status_code=ex.status,
        content=problem.model_dump(exclude_none=True),
        headers={"Content-Type": "application/problem+json"},
    )


async def value_error_handler(request: Request, ex: ValueError):
    problem = create_security_problem_detail(
        status=status.HTTP_400_BAD_REQUEST,
        title="Validation Error",
        detail=str(ex),
        type_="https://wishlist.example.com/problems/validation-error",
        instance=str(request.url),
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=problem.model_dump(exclude_none=True),
        headers={"Content-Type": "application/problem+json"},
    )


async def wish_not_found_handler(request: Request, ex: WishNotFoundError):
    problem = create_problem_detail(
        status=status.HTTP_404_NOT_FOUND,
        title="Wish Not Found",
        detail=str(ex),
        type_="https://wishlist.example.com/problems/wish-not-found",
        instance=str(request.url),
    )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=problem.model_dump(exclude_none=True),
        headers={"Content-Type": "application/problem+json"},
    )


async def request_validation_error_handler(request: Request, ex: RequestValidationError):
    errors = []
    for error in ex.errors():
        field = " -> ".join(str(x) for x in error["loc"])
        message = error["msg"]
        errors.append(f"{field}: {message}")

    problem = create_security_problem_detail(
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        title="Validation Error",
        detail="; ".join(errors),
        type_="https://wishlist.example.com/problems/validation-error",
        instance=str(request.url),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=problem.model_dump(exclude_none=True),
        headers={"Content-Type": "application/problem+json"},
    )


async def validation_error_handler(request: Request, ex: ValidationError):
    errors = []
    for error in ex.errors():
        field = " -> ".join(str(x) for x in error["loc"])
        message = error["msg"]
        errors.append(f"{field}: {message}")

    problem = create_security_problem_detail(
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        title="Validation Error",
        detail="; ".join(errors),
        type_="https://wishlist.example.com/problems/validation-error",
        instance=str(request.url),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=problem.model_dump(exclude_none=True),
        headers={"Content-Type": "application/problem+json"},
    )


async def http_exception_handler(request: Request, ex: HTTPException):
    detail = ex.detail if isinstance(ex.detail, str) else "HTTP Error"
    problem = create_security_problem_detail(
        status=ex.status_code,
        title="HTTP Error",
        detail=detail,
        type_="https://wishlist.example.com/problems/http-error",
        instance=str(request.url),
    )
    return JSONResponse(
        status_code=ex.status_code,
        content=problem.model_dump(exclude_none=True),
        headers={"Content-Type": "application/problem+json"},
    )
