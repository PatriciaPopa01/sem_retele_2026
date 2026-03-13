import socket
import threading
import os

HOST = "127.0.0.1"
PORT = 3333
BUFFER_SIZE = 1024

class State:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def add(self, key, value):
        with self.lock:
            self.data[key] = value
        return f"{key} added"

    def get(self, key):
        with self.lock:
            return self.data.get(key, "Key not found")

    def remove(self, key):
        with self.lock:
            if key in self.data:
                del self.data[key]
                return f"{key} removed"
            return "Key not found"
    
    def list(self):
        x=[]
        with self.lock:
            if not self.data:
                return "Empty dictionary"
            
            for key in self.data.keys():
                x.append(f"{key}={self.data.get(key)}")
            return str(x)
    
    def count(self):
        with self.lock:
            return str(len(self.data))
        
    def clear(self):
        with self.lock:
            self.data.clear()
            return str(self.data) + " All data deleted"
        
    def update(self, key, newValue):
        with self.lock:
            x=[]
            if key in self.data:
                self.data[key] = newValue
                res = [f"{k}={v}" for k, v in self.data.items()]
                return str(res)
            else:
                return "Key not found"
            
    def pop(self, key):
        with self.lock:
            temp=[]
            if key in self.data:
                temp.append(f"{self.data.get(key)}")
                del self.data[key]
                return str(temp)
            else:
                return "Key not found"
            
    def quit(self):
        return "SERVER_SHUTTING_DOWN"


state = State()

def process_command(command):
    parts = command.split()

    
    cmd = parts[0]


    if cmd == "list" and len(parts) == 1:
        return state.list()
    elif cmd == "count" and len(parts) == 1:
        return state.count()
    elif cmd == "clear" and len(parts) == 1:
        return state.clear()
    elif cmd == "quit" and len(parts) == 1:
        return state.quit()

   
    if len(parts) < 2:
        return "Invalid command format"


    key = parts[1]
    
    if cmd == "add" and len(parts) > 2:
        return state.add(key, ' '.join(parts[2:]))
    elif cmd == "get" and len(parts) == 2:
        return state.get(key)
    elif cmd == "remove" and len(parts) == 2:
        return state.remove(key)
    elif cmd == "update" and len(parts) > 2:
        return state.update(key,parts[2:])
    elif cmd == "pop" and len(parts) == 2:
        return state.pop(key)
    
    return "Invalid command"

def handle_client(client_socket):
    with client_socket:
        while True:
            try:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break

                command = data.decode('utf-8').strip()
                response = process_command(command)
                
                response_data = f"{len(response)} {response}".encode('utf-8')
                client_socket.sendall(response_data)

                if response == "SERVER_SHUTTING_DOWN":
                    print("[SERVER] Shutting down...")
                    os._exit(0)

            except Exception as e:
                client_socket.sendall(f"Error: {str(e)}".encode('utf-8'))
                break

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[SERVER] Listening on {HOST}:{PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"[SERVER] Connection from {addr}")
            threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
