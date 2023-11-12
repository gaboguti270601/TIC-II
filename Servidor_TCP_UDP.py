import socket
import threading
import json

def guardar_mensaje(tipo, direccion, mensaje):
    try:
        with open('mensajes.json', 'r') as file:
            mensajes = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        mensajes = []

    mensajes.append({
        'tipo': tipo,
        'direccion': direccion,
        'mensaje': mensaje
    })

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
                    datos = data.decode('utf-8')
                    ds = datos.split(" - ")
                    senddata = "Header:", [ds[0], ds[1], ds[2], ds[3], ds[4]], "Datos:", ds[5]
                    print("Recibido (TCP):", senddata[0], senddata[1], senddata[2], senddata[3])
                    respuesta = "Tu mensaje es " + ds[5]
                    conn.sendall(respuesta.encode('utf-8'))
                    guardar_mensaje('TCP', addr[0], {
                        'Header': senddata[1],
                        'Datos': senddata[3]
                    })

def udp_server():
    HOST_UDP = '0.0.0.0'
    PORT_UDP = 1235

    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_udp.bind((HOST_UDP, PORT_UDP))

    print("El servidor UDP está esperando conexiones en el puerto", PORT_UDP)

    while True:
        message, address = server_udp.recvfrom(1024)
        print('Conectado por', address[0])
        datos = message.decode('utf-8')
        ds = datos.split(" - ")
        senddata = "Header:", [ds[0], ds[1], ds[2], ds[3], ds[4]], "Datos:", ds[5]
        print("Recibido (UDP):", senddata[0], senddata[1], senddata[2], senddata[3])
        guardar_mensaje('UDP', address[0], {
            'Header': senddata[1],
            'Datos': senddata[3]
        })

def main():
    with open('mensajes.json', 'a') as file:
        pass

    tcp_thread = threading.Thread(target=tcp_server)
    udp_thread = threading.Thread(target=udp_server)

    tcp_thread.start()
    udp_thread.start()

    tcp_thread.join()
    udp_thread.join()

if __name__ == "__main__":
    main()
