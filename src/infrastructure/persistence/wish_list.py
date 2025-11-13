import os
from decimal import Decimal
from typing import Any

import psycopg

from src.domain.entities import WishList, WishNote
from src.domain.models import WishListCreate, WishListUpdate, WishNoteCreate, WishNoteUpdate


def _get_conn() -> psycopg.Connection[Any]:
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "5432"))
    dbname = os.getenv("DB_NAME", "wishlist")
    user = os.getenv("DB_USER", "wishlist")
    password = os.getenv("DB_PASSWORD", "wishlist")
    return psycopg.connect(host=host, port=port, dbname=dbname, user=user, password=password)


def _ensure_schema() -> None:
    with _get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS wish_lists (
                wish_list_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                estimate_price NUMERIC NOT NULL,
                link TEXT
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS wish_notes (
                wish_note_id SERIAL PRIMARY KEY,
                wish_list_id INTEGER NOT NULL REFERENCES wish_lists(wish_list_id) ON DELETE CASCADE,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                received BOOLEAN NOT NULL
            );
            """
        )
        conn.commit()


class WishListStorage:
    def __init__(self) -> None:
        _ensure_schema()

    def get_all(self, maxPrice: Decimal | None = None) -> list[WishList]:
        query = """
            SELECT
            wish_list_id, user_id, title, description, estimate_price, link
            FROM wish_lists
            """
        params: tuple[Any, ...] = ()
        if maxPrice is not None:
            query += " WHERE estimate_price <= %s"
            params = (maxPrice,)
        query += " ORDER BY wish_list_id"
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
        result: list[WishList] = []
        for r in rows:
            item = WishList()
            item.wish_list_id = r[0]
            item.user_id = r[1]
            item.title = r[2]
            item.description = r[3]
            item.estimate_price = r[4]
            item.link = r[5]
            result.append(item)
        return result

    def get_all_by_user_id(self, user_id: int, maxPrice: Decimal | None = None) -> list[WishList]:
        query = """
            SELECT
            wish_list_id, user_id, title, description, estimate_price, link
            FROM wish_lists
            WHERE user_id = %s
            """
        params: tuple[Any, ...] = (user_id,)
        if maxPrice is not None:
            query += " AND estimate_price <= %s"
            params = (user_id, maxPrice)
        query += " ORDER BY wish_list_id"
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
        result: list[WishList] = []
        for r in rows:
            item = WishList()
            item.wish_list_id = r[0]
            item.user_id = r[1]
            item.title = r[2]
            item.description = r[3]
            item.estimate_price = r[4]
            item.link = r[5]
            result.append(item)
        return result

    def get_by_id(self, wish_id: int) -> WishList | None:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                wish_list_id, user_id, title, description, estimate_price, link
                FROM wish_lists
                WHERE wish_list_id = %s
                """,
                (wish_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        item = WishList()
        item.wish_list_id = row[0]
        item.user_id = row[1]
        item.title = row[2]
        item.description = row[3]
        item.estimate_price = row[4]
        item.link = row[5]
        return item

    def create(self, wish: WishListCreate) -> int:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO wish_lists
                (user_id, title, description, estimate_price, link)
                VALUES
                (%s, %s, %s, %s, %s)
                RETURNING wish_list_id
                """,
                (wish.user_id, wish.title, wish.description, wish.estimate_price, None),
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            return int(new_id)

    def update(self, wish_id: int, wish: WishListUpdate) -> bool:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                UPDATE wish_lists
                SET
                title = %s,
                description = %s,
                estimate_price = %s,
                link = %s
                WHERE wish_list_id = %s
                """,
                (wish.title, wish.description, wish.estimate_price, wish.link, wish_id),
            )
            updated = cur.rowcount > 0
            conn.commit()
            return updated

    def delete(self, wish_id: int) -> bool:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM wish_lists WHERE wish_list_id = %s", (wish_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            return deleted


class WishNotesStorage:
    def __init__(self) -> None:
        _ensure_schema()

    def get_all(self) -> list[WishNote]:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                wish_note_id, wish_list_id, title, description, received
                FROM wish_notes
                """
            )
            rows = cur.fetchall()
        result: list[WishNote] = []
        for r in rows:
            item = WishNote()
            item.wish_note_id = r[0]
            item.wish_list_id = r[1]
            item.title = r[2]
            item.description = r[3]
            item.received = r[4]
            result.append(item)
        return result

    def get_all_by_wish_id(self, wish_id: int) -> list[WishNote]:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                wish_note_id, wish_list_id, title, description, received
                FROM wish_notes
                WHERE wish_list_id = %s
                """,
                (wish_id,),
            )
            rows = cur.fetchall()
        result: list[WishNote] = []
        for r in rows:
            item = WishNote()
            item.wish_note_id = r[0]
            item.wish_list_id = r[1]
            item.title = r[2]
            item.description = r[3]
            item.received = r[4]
            result.append(item)
        return result

    def get_by_id(self, note_id: int) -> WishNote | None:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                wish_note_id, wish_list_id, title, description, received
                FROM wish_notes
                WHERE wish_note_id = %s
                """,
                (note_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        item = WishNote()
        item.wish_note_id = row[0]
        item.wish_list_id = row[1]
        item.title = row[2]
        item.description = row[3]
        item.received = row[4]
        return item

    def create(self, wish_id: int, note: WishNoteCreate) -> int:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO wish_notes
                (wish_list_id, title, description, received)
                VALUES
                (%s, %s, %s, %s)
                RETURNING wish_note_id
                """,
                (wish_id, note.title, note.description, note.received),
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            return int(new_id)

    def update(self, note: WishNoteUpdate) -> bool:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                UPDATE wish_notes
                SET
                title = %s,
                description = %s,
                received = %s
                WHERE wish_note_id = %s
                """,
                (note.title, note.description, note.received, note.wish_note_id),
            )
            updated = cur.rowcount > 0
            conn.commit()
            return updated

    def delete(self, note_id: int) -> bool:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM wish_notes WHERE wish_note_id = %s", (note_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            return deleted

    def delete_by_wish_id(self, wish_id: int) -> bool:
        with _get_conn() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM wish_notes WHERE wish_list_id = %s", (wish_id,))
            conn.commit()
            return True
