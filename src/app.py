# Importar las funciones y menú
from funciones import *
from menu import *

# Ejecución principal
opcion = "3" # Seleccionar Mercado Libre por defecto

if opcion == "3":
    url_base = menu_mercado_libre()
    if url_base:
        busqueda = "" # Si no se ingresa nada se busca por defecto "celulares"
        scraping_mercado_libre(url_base, busqueda)
    else:
        print("Opción de país no válida. Intente de nuevo.")
else:
    print("Opción no válida. Intente de nuevo.")