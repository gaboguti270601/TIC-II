import json

def leer_mensajes():
    try:
        with open('mensajes.json', 'r') as file:
            mensajes = json.load(file)
            return mensajes
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

def main():
    mensajes = leer_mensajes()

    if mensajes:
        print("Mensajes almacenados:")
        for mensaje in mensajes:
            print(f"{mensaje['tipo']} de {mensaje['direccion']}: {mensaje['mensaje']}")
    else:
        print("No hay mensajes almacenados.")

if __name__ == "__main__":
    main()