class WishNotFoundError(Exception):
    def __init__(self, wish_id, message="Wish Not Found"):
        self.wish_id = wish_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: wish_id = {self.wish_id}"
