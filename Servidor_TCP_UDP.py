import socket
import threading
import json

def guardar_mensaje(tipo, direccion, mensaje):
    # Intentar leer mensajes existentes del archivo
    try:
        with open('mensajes.json', 'r') as file:
            mensajes = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        mensajes = []

    # Agregar el nuevo mensaje
    mensajes.append({
        'tipo': tipo,
        'direccion': direccion,
        'mensaje': mensaje
    })

    # Escribir los mensajes de vuelta al archivo
    with open('mensajes.json', 'w') as file:
        json.dump(mensajes, file)

def tcp_server():
    HOST_TCP = '0.0.0.0'
    PORT_TCP = 1234

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp:
        s_tcp.bind((HOST_TCP, PORT_TCP))
        s_tcp.listen()
        
        print("El servidor TCP está esperando conexiones en el puerto", PORT_TCP)
        
        while True:
            conn, addr = s_tcp.accept()
            with conn:
                print('Conectado por', addr[0])
                data = conn.recv(1024)
                if data:
                    mensaje = data.decode('utf-8')
                    print("Recibido (TCP):", mensaje)
                    respuesta = "Tu mensaje es " + mensaje
                    conn.sendall(respuesta.encode('utf-8'))
                    guardar_mensaje('TCP', addr[0], mensaje)

def udp_server():
    HOST_UDP = '0.0.0.0'
    PORT_UDP = 1235

    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_udp.bind((HOST_UDP, PORT_UDP))

    print("El servidor UDP está esperando conexiones en el puerto", PORT_UDP)

    while True:
        message, address = server_udp.recvfrom(1024)
        print('Conectado por', address[0])
        mensaje = message.decode('utf-8')
        print("Recibido (UDP):", mensaje)
        guardar_mensaje('UDP', address[0], mensaje)

def main():
    # Crear el archivo si no existe
    with open('mensajes.json', 'a') as file:
        pass

    # Iniciar servidores en hilos separados
    tcp_thread = threading.Thread(target=tcp_server)
    udp_thread = threading.Thread(target=udp_server)

    # Iniciar hilos
    tcp_thread.start()
    udp_thread.start()

    # Esperar a que ambos hilos terminen
    tcp_thread.join()
    udp_thread.join()

if __name__ == "__main__":
    main()
