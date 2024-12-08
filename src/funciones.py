import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

# Función para Mercado Libre - Selección de país
def menu_mercado_libre():
    '''print("\nSeleccione el país donde desea buscar en Mercado Libre:")
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
    # opcion = input("Ingrese el número de la opción deseada: ")'''
    opcion = ""

    # Si input esta vacio colocar 5 por defecto
    if opcion == "":
        opcion = "5"

    paises = {
        "1": "https://listado.mercadolibre.com.ar/",
        "2": "https://listado.mercadolibre.com.bo/",
        "3": "https://listado.mercadolibre.com.br/",
        "4": "https://listado.mercadolibre.cl/",
        "5": "https://listado.mercadolibre.com.co/",
        "6": "https://listado.mercadolibre.com.cr/",
        "7": "https://listado.mercadolibre.com.do/",
        "8": "https://listado.mercadolibre.com.ec/",
        "9": "https://listado.mercadolibre.com.gt/",
        "10": "https://listado.mercadolibre.com.hn/",
        "11": "https://listado.mercadolibre.com.mx/",
        "12": "https://listado.mercadolibre.com.ni/",
        "13": "https://listado.mercadolibre.com.pa/",
        "14": "https://listado.mercadolibre.com.py/",
        "15": "https://listado.mercadolibre.com.pe/",
        "16": "https://listado.mercadolibre.com.sv/",
        "17": "https://listado.mercadolibre.com.uy/",
        "18": "https://listado.mercadolibre.com.ve/"
    }

    return paises.get(opcion, None)

# Función de scraping para Books to Scrape
def scraping_books_to_scrape():
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Ejemplo: Extracción del título y precio de los primeros libros
    libros = []
    for producto in soup.select(".product_pod")[:50]:  # Limitar a los primeros 50 libros
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

    # Por defecto, se buscarán los primeros 100 productos y si el término de busqueda viene vacio se busca "smartwatch"
    if busqueda == "":
        busqueda = "smartwatch"

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
    
    total_productos = min(100, len(soup.select(".ui-search-result__wrapper")))  # Máximo 100 productos

    for producto in tqdm(soup.select(".ui-search-result__wrapper")[:total_productos], desc="Progreso", unit=" producto", unit_scale=True, ncols=100):
        # Título
        titulo = producto.select_one('.poly-component__title')
        nombre = titulo.text if titulo else "Título no disponible"

        # Precio
        precio_elemento = producto.select_one('.andes-money-amount__fraction')
        precio = precio_elemento.text if precio_elemento else "Precio no disponible"

        # URL del producto, sacarle del titulo el href
        url_producto = titulo.select_one('a')['href'] if titulo else "URL no disponible"

        # URL de la imagen del producto, buscar el elemento div que tiene la poly-card__portada y luego la imagen        
        img_elemento = producto.select_one('.poly-card__portada img')
        
        # si la imagen viene encriptada en base64 se debe ingresar al producto y buscar la imagen con la clase ui-pdp-image ui-pdp-gallery__figure__image
        if img_elemento.has_attr('src'):
            url_imagen = img_elemento['src']
            if url_imagen.startswith("data:image"):
                # Se debe ingresar al producto para obtener la imagen
                url_producto = url_base + url_producto                
                url_imagen = img_elemento['data-src'] if img_elemento else "URL Imagen no disponible"
        else:
            url_imagen = "URL Imagen no disponible"            
    
        productos.append({
            "Título": nombre,
            "Precio": precio,
            "URL": url_producto,
            "URL Imagen": url_imagen
        })

    # Limpiar URLs
    productos_limpios = limpiar_urls(productos, url_base)

    # Generar archivo CSV
    generar_csv(productos_limpios)

# Función para generar un archivo CSV con los resultados
def generar_csv(productos):
    if len(productos) == 0:
        print("No hay productos para generar el archivo CSV.")
        return

    # Crear un DataFrame con los productos
    df = pd.DataFrame(productos)

    # Generar el archivo CSV, si existe un archivo con el mismo nombre se sobreescribe
    df.to_csv("productos_mercado_libre.csv", index=False)
    print("Archivo CSV generado con éxito.")

# Funcion para limpiar las url del objeto productos, quitando la url_base de los productos que la contengan
def limpiar_urls(productos, url_base):
    # Recorremos el objeto
    for producto in productos:
        if url_base in producto["URL"]:
            producto["URL"] = producto["URL"].replace(url_base, "")
    
    return productos
