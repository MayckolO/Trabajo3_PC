from sqlmodel import select
from database import create_db, get_session
from models import Categoria, Libro
from scraper import obtener_libros

def cargar_datos() -> None:
    create_db()

    libros = obtener_libros()

    with get_session() as session:

        print(f"Se obtuvieron {len(libros)} libros.")

        for libro in libros:

            categoria = session.exec(
                select(Categoria).where(
                    Categoria.nombre == libro["categoria"]
                )
            ).first()

            if categoria is None:

                categoria = Categoria(
                    nombre=libro["categoria"]
                )

                session.add(categoria)
                session.commit()
                session.refresh(categoria)

            libro_existente = session.exec(
                select(Libro).where(
                    Libro.url_detalle == libro["url_detalle"]
                )
            ).first()

            if libro_existente:
                continue

            nuevo_libro = Libro(
                titulo=libro["titulo"],
                precio=libro["precio"],
                valoracion=libro["valoracion"],
                disponible=libro["disponible"],
                url_detalle=libro["url_detalle"],
                categoria_id=categoria.id
            )

            session.add(nuevo_libro)    
        
        session.commit()

        print("Datos guardados correctamente.")

if __name__ == "__main__":
    cargar_datos()