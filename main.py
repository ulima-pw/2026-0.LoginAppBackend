import bcrypt
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from routers import categorias, videojuegos
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

accesos = {}

@app.post("/login")
async def login(login_request : LoginRequest):
    if login_request.username == "PROGRAWEB" and login_request.password == "123123123":
        hora_actual = time.time_ns()
        cadena_a_encriptar = f"{login_request.username}-{str(hora_actual)}"
        cadena_hasheada = bcrypt.hashpw(bytearray(cadena_a_encriptar), bcrypt.gensalt())
        accesos[cadena_hasheada] = {
            "ultimo_login" : time.time_ns()
        }

        return {
            "msg" : "Acceso concedido",
            "token" : cadena_hasheada
        }
    else:
        raise HTTPException(
            status_code=400, 
            detail="Error en login, credenciales incorrectas")

app.include_router(categorias.router)
app.include_router(videojuegos.router)

