import socket

server_address = ('host.docker.internal', 12345)

# Creează un socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(server_address)

try:
    # Trimite date către server
    message = "Hello, server!"
    client_socket.sendall(message.encode())

    # Primește și afișează datele primite de la server
    data = client_socket.recv(1024)
    print(f"Date primite de la server: {data.decode()}")

finally:   
    client_socket.close()
