import socket

server_address = ('0.0.0.0', 12345) 

# Creează un socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(server_address)

print(f"Așteaptă mesaje pe {server_address}")

while True:
    # Așteaptă primirea unui mesaj
    data, client_address = server_socket.recvfrom(1024)

    print(f"Mesaj primit de la {client_address}: {data.decode()}")

    # Trimite un răspuns către client
    response_message = "Hello, client!"
    server_socket.sendto(response_message.encode(), client_address)
