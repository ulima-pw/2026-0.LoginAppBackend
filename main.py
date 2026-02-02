from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class LoginRequest(BaseModel):
    username : str = Field(..., min_length=5)
    password : str = Field(..., min_length=8)

@app.post("/login")
async def login(login_request : LoginRequest):
    if login_request.username == "PROGRAWEB" and login_request.password == "123123123":
        return {
            "msg" : "Acceso concedido"
        }
    else:
        raise HTTPException(
            status_code=400, 
            detail="Error en login, credenciales incorrectas")