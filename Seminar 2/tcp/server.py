import socket

server_address = ('0.0.0.0', 12345)

# Creează un socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(server_address)

server_socket.listen(1)

print(f"Așteaptă conexiuni pe {server_address}")

while True:    
    connection, client_address = server_socket.accept()
    
    try:
        print(f"Conexiune acceptată de la {client_address}")

        # Primește și afișează datele primite de la client
        data = connection.recv(1024)
        print(f"Date primite: {data.decode()}")

        # Trimite date către client
        message_to_client = "Hello, client!"
        connection.sendall(message_to_client.encode())

    finally:       
        connection.close()
