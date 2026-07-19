from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def iniciar_driver() -> webdriver.Chrome:
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )

    driver.maximize_window()

    return driver


def obtener_libros() -> list[dict]:
    driver = iniciar_driver()

    wait = WebDriverWait(driver, 10)

    driver.get("https://books.toscrape.com")

    categorias = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".side_categories ul li ul li a")
        )
    )

    lista_categorias = []

    for categoria in categorias:
        href = categoria.get_attribute("href")

        lista_categorias.append(
            {
                "nombre": categoria.text.strip(),
                "url": href
            }
        )
        

    datos_libros = []

    for categoria in lista_categorias:

        driver.get(categoria["url"])

        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "article.product_pod")
            )
        )

        while True:

            nombre_categoria = categoria["nombre"]

            libros = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "article.product_pod")
                )
            )

            for libro in libros:
                try:
                    titulo = libro.find_element(
                        By.CSS_SELECTOR,
                        "h3 a"
                    ).get_attribute("title")

                    precio = libro.find_element(
                        By.CSS_SELECTOR,
                        ".price_color"
                    ).text

                    precio = float(precio.replace("£", ""))

                    disponibilidad = libro.find_element(
                        By.CSS_SELECTOR,
                        ".availability"
                    ).text.strip()

                    disponible = "In stock" in disponibilidad

                    estrellas = libro.find_element(
                        By.CSS_SELECTOR,
                        ".star-rating"
                    ).get_attribute("class").split()[-1]

                    conversion = {
                        "One": 1,
                        "Two": 2,
                        "Three": 3,
                        "Four": 4,
                        "Five": 5
                    }

                    valoracion = conversion[estrellas]

                    url_detalle = libro.find_element(
                        By.CSS_SELECTOR,
                        "h3 a"
                    ).get_attribute("href")

                    datos_libros.append(
                        {
                            "titulo": titulo,
                            "precio": precio,
                            "valoracion": valoracion,
                            "disponible": disponible,
                            "categoria": nombre_categoria,
                            "url_detalle": url_detalle
                        }
                    )

                except Exception as e:
                    print(f"Error al procesar un libro: {e}")

            try:
                siguiente = driver.find_element(
                    By.CSS_SELECTOR,
                    "li.next a"
                )

                siguiente.click()

                wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "article.product_pod")
                    )
                )

            except:
                break

    driver.quit()

    return datos_libros


if __name__ == "__main__":
    libros = obtener_libros()