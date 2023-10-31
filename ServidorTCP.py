import socket

HOST = '0.0.0.0'
PORT = 1234

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    
    print("El servidor está esperando conexiones en el puerto" , PORT)
    
    while True:
        conn, addr = s.accept()
        with conn:
            print('Conectdo por', addr)
            data = conn.recv(1024)
            if data:
                print("Recibido: ", data.decode('utf-8'))
                respuesta = "tu mensaje es " +data.decode('utf-8')
                conn.sendall(respuesta.encode('utf-8'))