import uuid
from sqlalchemy import UUID, Column, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
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
    perfil = relationship("Perfil", back_populates="usuario", uselist=False)

class Perfil(Base):
    __tablename__ = "perfil"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    nombre = Column(String)
    pais = Column(String)
    direccion = Column(String)
    usuario_id = Column(
        String(36),
        ForeignKey("usuario.id"),
        unique=True
    )
    usuario = relationship("Usuario", back_populates="perfil")

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

class CategoriaModel(Base):
    __tablename__ = "categoria"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    nombre = Column(String)

    videojuegos = relationship("Videojuego", back_populates="categoria")

videojuego_plataforma = Table(
    "videojuego_plataforma",
    Base.metadata,
    Column("videojuego_id", ForeignKey("videojuego.id"), primary_key=True),
    Column("plataforma_id", ForeignKey("plataforma.id"), primary_key=True)
)

class Videojuego(Base):
    __tablename__ = "videojuego"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    nombre = Column(String)
    descripcion = Column(String)
    url_imagen = Column(String)
    categoria_id = Column(
        UUID(as_uuid=True),
        ForeignKey("categoria.id"),
        unique=True
    )

    categoria = relationship("CategoriaModel", back_populates="videojuegos")
    plataformas = relationship(
        "Plataforma", 
        secondary=videojuego_plataforma, 
        back_populates="videojuegos"
    )

class Plataforma(Base):
    __tablename__ = "plataforma"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    nombre = Column(String)

    videojuegos = relationship(
        "Videojuego",
        secondary=videojuego_plataforma,
        back_populates="plataformas"
    )