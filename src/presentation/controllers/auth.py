from fastapi import APIRouter, Depends

from src.domain.auth import UserCreate
from src.presentation.models.auth import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)
from src.use_cases.auth import AuthService

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=RegisterResponse)
async def register(data: RegisterRequest, service: AuthService = Depends()):
    created = service.register(UserCreate(email=data.email, password=data.password))
    return RegisterResponse(user_id=created.user_id, email=created.email)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, service: AuthService = Depends()):
    token = service.login(data.email, data.password)
    return TokenResponse(access_token=token)
