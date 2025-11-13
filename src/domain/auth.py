from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    user_id: int | None = None
    email: str | None = None
    password_hash: str | None = None
    created_at: datetime | None = None
    blocked_until: datetime | None = None


@dataclass
class UserCreate:
    email: str
    password: str


@dataclass
class UserPublic:
    user_id: int
    email: str
