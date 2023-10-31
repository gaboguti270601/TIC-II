import socket

HOST = '0.0.0.0'
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

message, address = server.recvfrom(1024)
print(message.decode('utf-8'))
server.sento("Hello Client!".encode('utf-8'), address)