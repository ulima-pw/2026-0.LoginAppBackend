import bcrypt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .routers import categorias, videojuegos
from .data import accesos
from .database import get_db
from sqlalchemy.orm import Session
from .models import Usuario

import time

app = FastAPI()



origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

class LoginRequest(BaseModel):
    username : str = Field(..., min_length=5)
    password : str = Field(..., min_length=8)

@app.post("/login")
async def login(login_request : LoginRequest, db : Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.username == login_request.username,
        Usuario.password == login_request.password
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=400, 
            detail="Error en login, credenciales incorrectas")
    
    hora_actual = time.time_ns()
    cadena_a_encriptar = f"{login_request.username}-{str(hora_actual)}"
    cadena_hasheada = bcrypt.hashpw(
        cadena_a_encriptar.encode("utf-8"), 
        bcrypt.gensalt()
    )
    #accesos[cadena_hasheada] = {
    #    "ultimo_login" : time.time_ns()
    #}

    return {
        "msg" : "Acceso concedido",
        "token" : cadena_hasheada
    }


    # if login_request.username == "PROGRAWEB" and login_request.password == "123123123":
    #     hora_actual = time.time_ns()
    #     cadena_a_encriptar = f"{login_request.username}-{str(hora_actual)}"
    #     cadena_hasheada = bcrypt.hashpw(
    #         cadena_a_encriptar.encode("utf-8"), 
    #         bcrypt.gensalt()
    #     )
    #     accesos[cadena_hasheada] = {
    #         "ultimo_login" : time.time_ns()
    #     }

    #     return {
    #         "msg" : "Acceso concedido",
    #         "token" : cadena_hasheada
    #     }
    # else:
    #     raise HTTPException(
    #         status_code=400, 
    #         detail="Error en login, credenciales incorrectas")
    
@app.get("/logout")
async def logout(token : str):
    if token.encode("utf-8") in accesos:
        accesos.pop(token.encode("utf-8"))
        return {
            "msg" : ""
        }
    else :
        return {
            "msg" : "Token no existe"
        }

app.include_router(categorias.router)
app.include_router(videojuegos.router)

