import socket
import threading

def tcp_server():
    HOST_TCP = '0.0.0.0'
    PORT_TCP = 1234

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp:
        s_tcp.bind((HOST_TCP, PORT_TCP))
        s_tcp.listen()
        
        print("El servidor TCP est0á esperando conexiones en el puerto", PORT_TCP)
        
        while True:
            conn, addr = s_tcp.accept()
            with conn:
                print('Conectado por', addr[0])
                data = conn.recv(1024)
                if data:
                    print("Recibido (TCP):", data.decode('utf-8'))
                    respuesta = "Tu mensaje es " + data.decode('utf-8')
                    conn.sendall(respuesta.encode('utf-8'))

def udp_server():
    HOST_UDP = '0.0.0.0'
    PORT_UDP = 1235

    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_udp.bind((HOST_UDP, PORT_UDP))

    print("El servidor UDP está esperando conexiones en el puerto", PORT_UDP)

    while True:
        print('Conectado por', address[0])
        message, address = server_udp.recvfrom(1024)
        print("Recibido (UDP):", message.decode('utf-8'))

def main():
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
