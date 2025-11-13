from decimal import Decimal
from typing import Optional

from .entities import WishNote


class WishListDetailed:
    wish_list_id: int
    user_id: int
    title: str
    description: str
    estimate_price: Decimal
    link: Optional[str]
    notes: list[WishNote]


class WishListCreate:
    user_id: int
    title: str
    description: str
    estimate_price: Decimal


class WishListUpdate:
    title: str
    description: str
    estimate_price: Decimal
    link: Optional[str]


class WishNoteCreate:
    title: str
    description: str
    received: bool


class WishNoteUpdate:
    wish_note_id: int
    title: str
    description: str
    received: bool
