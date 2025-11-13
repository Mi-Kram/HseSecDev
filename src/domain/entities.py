from decimal import Decimal
from typing import Optional


class WishList:
    wish_list_id: int
    user_id: int
    title: str
    description: str
    estimate_price: Decimal
    link: Optional[str]


class WishNote:
    wish_note_id: int
    wish_list_id: int
    title: str
    description: str
    received: bool
