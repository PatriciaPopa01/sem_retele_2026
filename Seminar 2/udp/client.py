import socket

server_address = ('host.docker.internal', 12345)

# Creează un socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Trimite un mesaj către server
    message = "Hello, server!"
    client_socket.sendto(message.encode(), server_address)

    # Așteaptă răspunsul de la server
    response, server_address = client_socket.recvfrom(1024)
    print(f"Răspuns de la server: {response.decode()}")

finally: 
    client_socket.close()
