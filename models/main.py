from queries import (
    total_items,
    cantidad_por_categoria,
    top_10_mas_caros,
    estadisticas_precios
)


while True:

    print("\n==============================")
    print(" BOOKS TO SCRAPE ")
    print("==============================")
    print("1. Total de libros")
    print("2. Cantidad por categoría")
    print("3. Top 10 libros más caros")
    print("4. Estadísticas de precios")
    print("5. Salir")

    opcion = input("\nSeleccione una opción: ")

    if opcion == "1":

        print(f"\nTotal de libros: {total_items()}")

    elif opcion == "2":

        print()

        for categoria, cantidad in cantidad_por_categoria():

            print(f"{categoria:<25} {cantidad}")

    elif opcion == "3":

        print()

        libros = top_10_mas_caros()

        for i, libro in enumerate(libros, start=1):

            print(
                f"{i}. {libro.titulo} - £{libro.precio}"
            )

    elif opcion == "4":

        datos = estadisticas_precios()

        print()

        print(f"Precio promedio : £{datos['promedio']}")
        print(f"Precio mínimo   : £{datos['minimo']}")
        print(f"Precio máximo   : £{datos['maximo']}")

    elif opcion == "5":

        print("\nHasta luego.")
        break

    else:

        print("\nOpción inválida.")