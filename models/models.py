from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)

    libros: list["Libro"] = Relationship(back_populates="categoria")


class Libro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    titulo: str
    precio: float
    valoracion: int
    disponible: bool
    url_detalle: str = Field(unique=True)

    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")

    categoria: Optional[Categoria] = Relationship(back_populates="libros")