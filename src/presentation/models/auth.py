from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("password too long (max 72 bytes)")
        return v


class RegisterResponse(BaseModel):
    user_id: int
    email: EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(max_length=72)

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("password too long (max 72 bytes)")
        return v


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class BlockUserRequest(BaseModel):
    user_id: int
    # ISO 8601 datetime string
    blocked_until: str
