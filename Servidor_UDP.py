import socket

HOST = '0.0.0.0'
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print("El servidor está esperando conexiones en el puerto", PORT)

while True:
    message, address = server.recvfrom(1024)
    print("Recibido de", address[0], ":", message.decode('utf-8'))