from pydantic import BaseModel

from src.domain.models import WishListUpdate, WishNoteCreate, WishNoteUpdate


class WishListCreatePydantic(BaseModel):
    title: str
    description: str
    estimate_price: float


class WishListPut(BaseModel, WishListUpdate):
    pass


class WishNoteCreatePydantic(BaseModel, WishNoteCreate):
    pass


class WishListPost(BaseModel):
    info: WishListCreatePydantic
    notes: list[WishNoteCreatePydantic]


class WishNotePost(BaseModel):
    notes: list[WishNoteCreatePydantic]


class WishNoteUpdatePydantic(BaseModel, WishNoteUpdate):
    pass


class WishNotePut(BaseModel):
    notes: list[WishNoteUpdatePydantic]
