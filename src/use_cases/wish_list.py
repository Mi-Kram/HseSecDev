from decimal import Decimal

from fastapi import Depends, HTTPException, status

from src.domain.entities import WishList
from src.domain.errors import WishNotFoundError
from src.domain.models import (
    WishListCreate,
    WishListDetailed,
    WishListUpdate,
    WishNoteCreate,
    WishNoteUpdate,
)
from src.infrastructure.persistence.wish_list import WishListStorage, WishNotesStorage


class WishListService:

    def __init__(
        self,
        wishes_storage: WishListStorage = Depends(),
        notes_storage: WishNotesStorage = Depends(),
    ):
        super().__init__()
        self._wishes_storage = wishes_storage
        self._notes_storage = notes_storage

    def get_all(self, maxPrice: Decimal | None = None) -> list[WishList]:
        return self._wishes_storage.get_all(maxPrice)

    def get_all_by_user_id(self, user_id: int, maxPrice: Decimal | None = None) -> list[WishList]:
        return self._wishes_storage.get_all_by_user_id(user_id, maxPrice)

    def get_by_id(self, wish_id: int, user_id: int) -> WishListDetailed:
        wish: WishList = self._wishes_storage.get_by_id(wish_id)
        if wish is None:
            raise WishNotFoundError(wish_id)

        # Check ownership
        if wish.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")

        detailed = WishListDetailed()
        detailed.wish_list_id = wish.wish_list_id
        detailed.user_id = wish.user_id
        detailed.title = wish.title
        detailed.description = wish.description
        detailed.estimate_price = wish.estimate_price
        detailed.link = wish.link
        detailed.notes = self._notes_storage.get_all_by_wish_id(wish_id)
        return detailed

    def create(self, wish: WishListCreate, notes: list[WishNoteCreate]) -> int:
        wish.title = wish.title.strip()
        wish.description = wish.description.strip()

        if len(wish.title) == 0:
            raise ValueError("wish title must be filled")

        if wish.estimate_price < 0:
            raise ValueError("estimate price must be zero or greater")

        for note in notes:
            note.title = note.title.strip()
            note.description = note.description.strip()

            if len(note.title) == 0:
                raise ValueError("note title must be filled")

        wish_id = self._wishes_storage.create(wish)
        for note in notes:
            self._notes_storage.create(wish_id, note)

        return wish_id

    def update(self, wish_id: int, wish: WishListUpdate, user_id: int) -> bool:
        # Check ownership first
        existing_wish = self._wishes_storage.get_by_id(wish_id)
        if existing_wish is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wish list not found")
        if existing_wish.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")

        wish.title = wish.title.strip()
        wish.description = wish.description.strip()

        if len(wish.title) == 0:
            raise ValueError("title must be filled")

        if wish.estimate_price < 0:
            raise ValueError("estimate price must be zero or greater")

        return self._wishes_storage.update(wish_id, wish)

    def delete(self, wish_id: int, user_id: int) -> bool:
        # Check ownership first
        existing_wish = self._wishes_storage.get_by_id(wish_id)
        if existing_wish is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wish list not found")
        if existing_wish.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")

        return self._wishes_storage.delete(wish_id)

    def add_notes(self, wish_id: int, notes: list[WishNoteCreate], user_id: int) -> bool:
        # Check ownership first
        existing_wish = self._wishes_storage.get_by_id(wish_id)
        if existing_wish is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wish list not found")
        if existing_wish.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")

        for note in notes:
            note.title = note.title.strip()
            note.description = note.description.strip()

            if len(note.title) == 0:
                raise ValueError("title must be filled")

        for note in notes:
            self._notes_storage.create(wish_id, note)

        return True

    def update_notes(self, wish_id: int, notes: list[WishNoteUpdate], user_id: int) -> bool:
        # Check ownership first
        existing_wish = self._wishes_storage.get_by_id(wish_id)
        if existing_wish is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wish list not found")
        if existing_wish.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")

        for note in notes:
            note.title = note.title.strip()
            note.description = note.description.strip()

            if len(note.title) == 0:
                raise ValueError("title must be filled")

        for note in notes:
            self._notes_storage.update(note)

        return True

    def delete_notes(self, wish_id: int, notes_id: list[int], user_id: int) -> bool:
        # Check ownership first
        existing_wish = self._wishes_storage.get_by_id(wish_id)
        if existing_wish is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wish list not found")
        if existing_wish.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")

        for id in notes_id:
            self._notes_storage.delete(id)
        return True
