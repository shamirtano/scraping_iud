# Función para mostrar un menú de opciones
def menu_principal():
    print("Seleccione el sitio donde desea realizar scraping:")
    print("1. Books to Scrape")
    print("2. Quotes to Scrape")
    print("3. Mercado Libre")
    # opcion = input("Ingrese el número de la opción deseada: ")
    opcion = ""

    # Si input esta vacio colocar 3 por defecto para seleccionar Mercado Libre para evitar errores en el yml
    if opcion == "":
        opcion = "3"
    
    return opcion