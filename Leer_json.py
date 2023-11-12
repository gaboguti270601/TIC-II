import json

def leer_mensajes():
    try:
        with open('mensajes.json', 'r') as file:
            mensajes = json.load(file)
            return mensajes
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(f"Error al leer el archivo JSON: {e}")
        return []

def main():
    mensajes = leer_mensajes()

    if mensajes:
        print("Mensajes almacenados:")
        for mensaje in mensajes:
            tipo = mensaje.get('tipo', 'Tipo no especificado')
            direccion = mensaje.get('direccion', 'Dirección no especificada')
            mensaje_data = mensaje.get('mensaje', {})
            header = mensaje_data.get('Header', 'Header no especificado')
            datos = mensaje_data.get('Datos', 'Datos no especificados')
            
            print(f"{tipo} de {direccion}: Header: {header}, Datos: {datos}")
    else:
        print("No hay mensajes almacenados.")

if __name__ == "__main__":
    main()
