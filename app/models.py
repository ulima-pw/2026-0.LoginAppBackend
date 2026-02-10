import uuid
from sqlalchemy import Column, String, DateTime
from .database import Base

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    username = Column(String, unique=True)
    password = Column(String, unique=True)

class Acceso(Base):
    __tablename__ = "acceso"
    id = Column(
        String,
        primary_key=True,
        index=True
    )
    ultimo_login = Column(
        DateTime
    )