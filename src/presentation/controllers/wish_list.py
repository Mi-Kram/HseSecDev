from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.domain.models import WishListCreate
from src.presentation.dependencies import CurrentUserID, authorize
from src.presentation.models.wish_list import WishListPost, WishListPut, WishNotePost, WishNotePut
from src.use_cases.wish_list import WishListService

router = APIRouter(tags=["wishes"])


# ...?price=20
@router.get("")
@authorize
async def get_wishes(
    user_id: CurrentUserID = None,
    price: Optional[Decimal] = Query(None),
    service: WishListService = Depends(),
):
    return service.get_all_by_user_id(user_id, price)


# .../5
@router.get("/{id}")
@authorize
async def get_wish_by_id(
    id: int,
    user_id: CurrentUserID = None,
    service: WishListService = Depends(),
):
    return service.get_by_id(id, user_id)


# .../
@router.post("")
@authorize
async def create_wish(
    data: WishListPost,
    user_id: CurrentUserID = None,
    service: WishListService = Depends(),
):
    info = WishListCreate()
    info.user_id = user_id
    info.title = data.info.title
    info.description = data.info.description
    info.estimate_price = data.info.estimate_price
    return {"wish_list_id": service.create(info, data.notes)}


# .../5
@router.put("/{id}")
@authorize
async def update_wish(
    id: int,
    data: WishListPut,
    user_id: CurrentUserID = None,
    service: WishListService = Depends(),
):
    return {"success": service.update(id, data, user_id)}


# .../5
@router.delete("/{id}")
@authorize
async def delete_wish(
    id: int,
    user_id: CurrentUserID = None,
    service: WishListService = Depends(),
):
    return {"success": service.delete(id, user_id)}


# .../5/notes
@router.post("/{id}/notes")
@authorize
async def create_notes(
    id: int,
    data: WishNotePost,
    user_id: CurrentUserID = None,
    service: WishListService = Depends(),
):
    return {"success": service.add_notes(id, data.notes, user_id)}


# .../5/notes
@router.put("/{id}/notes")
@authorize
async def update_notes(
    id: int,
    data: WishNotePut,
    user_id: CurrentUserID = None,
    service: WishListService = Depends(),
):
    return {"success": service.update_notes(id, data.notes, user_id)}


# .../5/notes?ids=1&ids=2
@router.delete("/{id}/notes")
@authorize
async def delete_notes(
    id: int,
    user_id: CurrentUserID = None,
    ids: list[int] = Query([]),
    service: WishListService = Depends(),
):
    return {"success": service.delete_notes(id, ids, user_id)}
