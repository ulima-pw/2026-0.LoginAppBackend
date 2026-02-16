from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/videojuegos",
    tags=["Videojuegos"]
)

videojuegos = []

@router.get("/")
async def list_videojuegos():
    return {
        "msg" : "",
        "data" : videojuegos
    }