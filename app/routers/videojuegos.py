from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..models import Videojuego
from ..database import get_db
from .security import verify_token

router = APIRouter(
    prefix="/videojuegos",
    tags=["Videojuegos"]
)


@router.get("/", dependencies=[Depends(verify_token)])
async def list_videojuegos(db: Session = Depends(get_db)):
    db_videojuegos = db.query(Videojuego).all()

    return {
        "msg" : "",
        "data" : db_videojuegos
    }