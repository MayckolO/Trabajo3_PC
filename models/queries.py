from sqlmodel import select, func
from database import get_session
from models import Categoria, Libro


def total_items() -> int:
    with get_session() as session:

        total = session.exec(
            select(func.count()).select_from(Libro)
        ).one()

        return total


def cantidad_por_categoria():

    with get_session() as session:

        resultado = session.exec(
            select(
                Categoria.nombre,
                func.count(Libro.id)
            )
            .join(Libro)
            .group_by(Categoria.id)
            .order_by(func.count(Libro.id).desc())
        ).all()

        return resultado


def top_10_mas_caros():

    with get_session() as session:

        libros = session.exec(
            select(Libro)
            .order_by(Libro.precio.desc())
            .limit(10)
        ).all()

        return libros


def estadisticas_precios():

    with get_session() as session:

        promedio, minimo, maximo = session.exec(
            select(
                func.avg(Libro.precio),
                func.min(Libro.precio),
                func.max(Libro.precio)
            )
        ).one()

        return {
            "promedio": round(promedio, 2),
            "minimo": minimo,
            "maximo": maximo
        }