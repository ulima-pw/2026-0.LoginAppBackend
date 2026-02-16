from pydantic import BaseModel

class Videojuego(BaseModel):
    id : str | None = None
    nombre : str
    descripcion : str
    url_imagen : str
    categoria : "Categoria"
    class Config:
        from_attributes = True

class Categoria(BaseModel):
    id : str | None = None
    nombre : str
    videojuegos : list[Videojuego] = []
    class Config:
        from_attributes = True

