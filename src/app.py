# Importamos las demás librerías
import requests
from bs4 import BeautifulSoup
import pandas as pd
# import json

# Metodos a utilizar
# Función para mostrar un menú de opciones
def menu_principal():
    print("Seleccione el sitio donde desea realizar scraping:")
    print("1. Books to Scrape")
    print("2. Quotes to Scrape")
    print("3. Mercado Libre")
    opcion = input("Ingrese el número de la opción deseada: ")

    # Si input esta vacio colocar 3 por defecto para seleccionar Mercado Libre para evitar errores en el yml
    if opcion == "":
        opcion = "3"
    
    return opcion

# Función para Mercado Libre - Selección de país
def menu_mercado_libre():
    print("\nSeleccione el país donde desea buscar en Mercado Libre:")
    print("1. Argentina")
    print("2. Bolivia")
    print("3. Brasil")
    print("4. Chile")
    print("5. Colombia")
    print("6. Costa Rica")
    print("7. Dominicana")
    print("8. Ecuador")
    print("9. Guatemala")
    print("10. Honduras")
    print("11. México")
    print("12. Nicaragua")
    print("13. Panamá")
    print("14. Paraguay")
    print("15. Perú")
    print("16. El Salvador")
    print("17. Uruguay")
    print("18. Venezuela")
    opcion = input("Ingrese el número de la opción deseada: ")

    # Si input esta vacio colocar 5 por defecto
    if opcion == "":
        opcion = "5"

    paises = {
        "1": "https://listado.mercadolibre.com.ar",
        "2": "https://listado.mercadolibre.com.bo",
        "3": "https://listado.mercadolibre.com.br",
        "4": "https://listado.mercadolibre.cl",
        "5": "https://listado.mercadolibre.com.co",
        "6": "https://listado.mercadolibre.com.cr",
        "7": "https://listado.mercadolibre.com.do",
        "8": "https://listado.mercadolibre.com.ec",
        "9": "https://listado.mercadolibre.com.gt",
        "10": "https://listado.mercadolibre.com.hn",
        "11": "https://listado.mercadolibre.com.mx",
        "12": "https://listado.mercadolibre.com.ni",
        "13": "https://listado.mercadolibre.com.pa",
        "14": "https://listado.mercadolibre.com.py",
        "15": "https://listado.mercadolibre.com.pe",
        "16": "https://listado.mercadolibre.com.sv",
        "17": "https://listado.mercadolibre.com.uy",
        "18": "https://listado.mercadolibre.com.ve"
    }

    return paises.get(opcion, None)

# Función de scraping para Books to Scrape
def scraping_books_to_scrape():
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Ejemplo: Extracción del título y precio de los primeros libros
    libros = []
    for producto in soup.select(".product_pod")[:5]:  # Limitar a los primeros 5 libros
        titulo = producto.h3.a["title"]
        precio = producto.find("p", class_="price_color").text
        libros.append({"Título": titulo, "Precio": precio})

    print("\nLibros obtenidos de Books to Scrape:")
    for libro in libros:
        print(f"{libro['Título']} - {libro['Precio']}")

# Función de scraping para Quotes to Scrape
def scraping_quotes_to_scrape():
    url = "https://quotes.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Ejemplo: Extracción de las primeras 5 citas
    citas = []
    for quote in soup.select(".quote")[:5]:  # Limitar a las primeras 5 citas
        texto = quote.find("span", class_="text").get_text()
        autor = quote.find("small", class_="author").get_text()
        citas.append({"Cita": texto, "Autor": autor})

    print("\nCitas obtenidas de Quotes to Scrape:")
    for cita in citas:
        print(f"\"{cita['Cita']}\" - {cita['Autor']}")

# Función de scraping para Mercado Libre
def scraping_mercado_libre(url_base, busqueda):

    # Por defecto, se buscarán los primeros 5 productos y si el término de busqueda viene vacio se busca "celulares"
    if busqueda == "":
        busqueda = "celulares"

    url = f"{url_base}/{busqueda.replace(' ', '%20')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    # Validación de respuesta
    if response.status_code != 200:
        print("Error al acceder a la página. Verifique la URL o intente de nuevo más tarde.")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    # Extracción del título, precio, url y url_imagen de los primeros productos
    productos = []
    for producto in soup.select(".ui-search-result__wrapper")[:5]:  # Limite de cantidad de productos
        # Título
        titulo = producto.select_one('.poly-component__title')
        nombre = titulo.text if titulo else "Título no disponible"

        # Precio
        precio_elemento = producto.select_one('.andes-money-amount__fraction')
        precio = precio_elemento.text if precio_elemento else "Precio no disponible"

        # URL del producto
        enlace = titulo.select_one('a')
        url_producto = enlace['href'] if enlace else "URL no disponible"

        # URL de la imagen
        img_elemento = producto.select_one('.poly-component__picture.poly-component__picture--contain')
        url_imagen = img_elemento['src'] if img_elemento else "URL de imagen no disponible"

        productos.append({
            "Título": nombre,
            "Precio": precio,
            "URL": url_producto,
            "URL Imagen": url_imagen
        })

        # Mostramos el progreso
        print(f"Producto {len(productos)} agregado.")

    # Imprimimos la lista de los productos
    print(f"\nProductos obtenidos de Mercado Libre ({url_base}):")
    for producto in productos:
        print(f"Título: {producto['Título']} - Precio: {producto['Precio']} - URL: {producto['URL']} - URL Imagen: {producto['URL Imagen']}")
        print()

# Ejecución principal
opcion = menu_principal() 

if opcion == "1":
    scraping_books_to_scrape()
elif opcion == "2":
    scraping_quotes_to_scrape()
elif opcion == "3":
    url_base = menu_mercado_libre()
    if url_base:
        busqueda = input("Ingrese el término de búsqueda: ")
        scraping_mercado_libre(url_base, busqueda)
    else:
        print("Opción de país no válida. Intente de nuevo.")
else:
    print("Opción no válida. Intente de nuevo.")