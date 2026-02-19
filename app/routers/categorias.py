from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload

from .security import verify_token
from ..database import get_db
from ..models import CategoriaModel
from ..schemas import Categoria

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)

categorias = []

@router.get("/", dependencies=[Depends(verify_token)])
async def list_categorias(db: Session = Depends(get_db)):
    lista = db.query(CategoriaModel).options(
        selectinload(CategoriaModel.videojuegos)
    ).all()
    

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
