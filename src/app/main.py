import dotenv
from fastapi import FastAPI

from src import presentation
from src.presentation.openapi import custom_openapi

dotenv.load_dotenv()

app = FastAPI(
    title="Wishlist App",
    version="0.1.0",
    description="Simple Wishlist API with JWT auth, user management and wishes CRUD.",
    swagger_ui_parameters={"persistAuthorization": True},
)

presentation.add_presentaion(app)
app.openapi = lambda: custom_openapi(app)
