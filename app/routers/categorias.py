from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
import datetime
from ..data import accesos
from ..database import get_db
from ..models import Acceso, CategoriaModel


class Categoria(BaseModel):
    id : str | None = None
    nombre : str

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)

categorias = []

async def verify_token(x_token : str = Header(...), db: Session = Depends(get_db)):
    db_query = db.query(Acceso).filter(Acceso.id == x_token)
    db_acceso = db_query.first()
    if not db_acceso:
        raise HTTPException(
            status_code=403,
            detail={
                "msg" : "Token incorrecto"
            }
        )
    
    db_query.update({
        "ultimo_login" : datetime.datetime.now()
    })
    db.commit()
    db.refresh(db_acceso)

    return x_token

@router.get("/", dependencies=[Depends(verify_token)])
async def list_categorias(db: Session = Depends(get_db)):
    lista = db.query(CategoriaModel).all()

    return {
        "msg" : "",
        "data" : lista
    }

@router.get("/{cat_id}", dependencies=[Depends(verify_token)])
async def get_categoria(cat_id : str):
    for cat in categorias:
        if cat.id == cat_id:
            return {
                "msg" : "",
                "data" : cat
            }
        
    raise HTTPException(
        status_code=404,
        detail={
            "msg" : "Categoria id not found"
        }
    )

@router.post("/", dependencies=[Depends(verify_token)])
async def create_categoria(categoria : Categoria):
    categoria.id = str(uuid4())
    # TODO: Trabajar con una base de datos
    categorias.append(categoria)
    return {
        "msg" : "",
        "data" : categoria
    }

@router.put("/", dependencies=[Depends(verify_token)])
async def update_categoria(categoria : Categoria):
    for cat in categorias:
        if cat.id == categoria.id:
            # Se encontro la categoria
            cat.nombre = categoria.nombre
            return {
                "msg" : "",
                "data" : cat
            }
    raise HTTPException(
        status_code=404,
        detail="Categoria id does not exist"
    ) 

@router.delete("/{categoria_id}", dependencies=[Depends(verify_token)])
async def delete_categoria(categoria_id : str):
    for i,cat in enumerate(categorias):
        if cat.id == categoria_id:
            categorias.pop(i)
            return {
                "msg" : ""
            }
        
    raise HTTPException(
        status_code=404,
        detail="Cannot delete the category: Not found"
    )
