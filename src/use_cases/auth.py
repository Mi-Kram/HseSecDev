import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status

from src.domain.auth import UserCreate, UserPublic
from src.infrastructure.persistence.auth import UsersRepository


class AuthService:
    def __init__(self, users_repo: UsersRepository = Depends()):
        self._users = users_repo
        self._jwt_secret = os.getenv("JWT_SECRET", "WishList Jwt Secret")
        self._jwt_algo = os.getenv("JWT_ALGO", "HS256")
        self._jwt_exp_minutes = int(os.getenv("JWT_EXP_MINUTES", "60"))

    def register(self, data: UserCreate) -> UserPublic:
        email = data.email.strip().lower()
        password = data.password.strip()

        if len(email) == 0 or len(password) < 6:
            raise ValueError("invalid registration data")

        # Check password length limit for bcrypt (72 bytes)
        if len(password.encode("utf-8")) > 72:
            raise ValueError("password too long (max 72 bytes)")

        existing = self._users.get_by_email(email)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="email already registered"
            )
        user_id = self._users.create(UserCreate(email=email, password=password))
        return UserPublic(user_id=user_id, email=email)

    def login(self, email: str, password: str) -> str:
        email = email.strip().lower()
        password = password.strip()

        # Check password length limit for bcrypt (72 bytes)
        if len(password.encode("utf-8")) > 72:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials"
            )

        user = self._users.get_by_email(email)
        if user is None or user.password_hash is None:
            # do not leak whether email exists
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials"
            )
        # block check
        if user.blocked_until is not None:
            now = datetime.now(timezone.utc)
            if user.blocked_until.tzinfo is None:
                # assume UTC if naive
                user_blocked_until = user.blocked_until.replace(tzinfo=timezone.utc)
            else:
                user_blocked_until = user.blocked_until
            if user_blocked_until > now:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user is blocked")
        if not self._users.verify_password(password, user.password_hash):
            # track failed attempt and block after 5 consecutive failures for 10 minutes
            new_count = self._users.increment_failed_attempts(user.user_id)
            if new_count >= 5:
                block_until = datetime.now(timezone.utc) + timedelta(minutes=10)
                self._users.set_block_until(user.user_id, block_until)
                # reset counter after blocking window starts
                self._users.reset_failed_attempts(user.user_id)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials"
            )
        # successful login resets attempts and clears any past block
        self._users.reset_failed_attempts(user.user_id)
        if user.blocked_until is not None:
            self._users.set_block_until(user.user_id, None)
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user.user_id),
            "email": user.email,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self._jwt_exp_minutes)).timestamp()),
        }
        return jwt.encode(payload, self._jwt_secret, algorithm=self._jwt_algo)

    def verify_token(self, token: str) -> Optional[int]:
        try:
            payload = jwt.decode(token, self._jwt_secret, algorithms=[self._jwt_algo])
            sub = payload.get("sub")
            return int(sub) if sub is not None else None
        except jwt.PyJWTError:
            return None

    def block_user_until(self, user_id: int, until: datetime) -> None:
        # normalize to UTC timezone-aware
        when = until if until.tzinfo is not None else until.replace(tzinfo=timezone.utc)
        self._users.set_block_until(user_id, when)
