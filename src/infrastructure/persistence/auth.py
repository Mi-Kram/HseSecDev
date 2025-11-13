import os
from typing import Any, Optional

import psycopg
from passlib.context import CryptContext

from src.domain.auth import User, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _get_conn() -> psycopg.Connection[Any]:
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "5432"))
    dbname = os.getenv("DB_NAME", "wishlist")
    user = os.getenv("DB_USER", "wishlist")
    password = os.getenv("DB_PASSWORD", "wishlist")
    print(host, port, dbname, user, password)
    return psycopg.connect(host=host, port=port, dbname=dbname, user=user, password=password)


def _ensure_schema() -> None:
    with _get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                blocked_until TIMESTAMPTZ,
                failed_attempts INTEGER NOT NULL DEFAULT 0
            );
            """
        )
        conn.commit()


class UsersRepository:
    def __init__(self) -> None:
        _ensure_schema()

    def get_by_email(self, email: str) -> Optional[User]:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                user_id, email, password_hash, created_at, blocked_until
                FROM users
                WHERE email = %s
                """,
                (email,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        user = User()
        user.user_id = row[0]
        user.email = row[1]
        user.password_hash = row[2]
        user.created_at = row[3]
        user.blocked_until = row[4]
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                user_id, email, password_hash, created_at, blocked_until
                FROM users
                WHERE user_id = %s
                """,
                (user_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        user = User()
        user.user_id = row[0]
        user.email = row[1]
        user.password_hash = row[2]
        user.created_at = row[3]
        user.blocked_until = row[4]
        return user

    def create(self, data: UserCreate) -> int:
        password_hash = pwd_context.hash(data.password)
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users
                (email, password_hash)
                VALUES
                (%s, %s)
                RETURNING user_id
                """,
                (data.email, password_hash),
            )
            new_id = cur.fetchone()[0]
            conn.commit()
        return int(new_id)

    def verify_password(self, plain_password: str, password_hash: str) -> bool:
        return pwd_context.verify(plain_password, password_hash)

    def set_block_until(self, user_id: int, blocked_until) -> None:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET blocked_until = %s
                WHERE user_id = %s
                """,
                (blocked_until, user_id),
            )
            conn.commit()

    def increment_failed_attempts(self, user_id: int) -> int:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET failed_attempts = failed_attempts + 1
                WHERE user_id = %s
                RETURNING failed_attempts
                """,
                (user_id,),
            )
            new_count_row = cur.fetchone()
            conn.commit()
        return int(new_count_row[0]) if new_count_row else 0

    def reset_failed_attempts(self, user_id: int) -> None:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET failed_attempts = 0
                WHERE user_id = %s
                """,
                (user_id,),
            )
            conn.commit()
