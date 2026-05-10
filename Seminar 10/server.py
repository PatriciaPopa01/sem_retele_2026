import socket
import json
import os
import threading
from datetime import datetime

# Configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 5000
FILES_DIR = 'files'
DEFAULT_USER = 'student'
DEFAULT_PASSWORD = '1234'

# Lista globala pentru istoric
file_history = []

def ensure_files_dir():
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)

def add_to_history(operation, filename, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_history.append({
        "timestamp": timestamp,
        "operation": operation,
        "filename": filename,
        "details": details
    })

def authenticate(username, password):
    return username == DEFAULT_USER and password == DEFAULT_PASSWORD

def handle_client(conn, addr):
    print(f"\n🔗 Client connected from {addr}")
    authenticated = False
    current_user = None
    
    try:
        while True:
            request_data = conn.recv(4096).decode('utf-8')
            if not request_data: break
            
            try:
                request = json.loads(request_data)
                command = request.get('command')
                print(f"📨 Command received: {command}")
                
                if command == 'login':
                    username = request.get('username')
                    password = request.get('password')
                    if authenticate(username, password):
                        authenticated = True
                        current_user = username
                        response = {'status': 'success', 'message': f'Welcome {username}!'}
                    else:
                        response = {'status': 'error', 'message': 'Invalid credentials'}
                
                elif not authenticated:
                    response = {'status': 'error', 'message': 'Not authenticated'}

                # --- IMPLEMENTARI STUDENT ---

                elif command == 'upload':
                    filename = request.get('filename')
                    content = request.get('content')
                    filepath = os.path.join(FILES_DIR, filename)
                    with open(filepath, 'w') as f:
                        f.write(content)
                    add_to_history("UPLOAD", filename)
                    response = {'status': 'success', 'message': f'File {filename} uploaded'}

                elif command == 'rename_file':
                    old_name = request.get('old_name')
                    new_name = request.get('new_name')
                    old_path = os.path.join(FILES_DIR, old_name)
                    new_path = os.path.join(FILES_DIR, new_name)
                    
                    if os.path.exists(old_path):
                        os.rename(old_path, new_path)
                        add_to_history("RENAME", old_name, f"Renamed to {new_name}")
                        response = {'status': 'success', 'message': f'Renamed {old_name} to {new_name}'}
                    else:
                        response = {'status': 'error', 'message': 'Original file not found'}

                elif command == 'read_file' or command == 'download':
                    filename = request.get('filename')
                    filepath = os.path.join(FILES_DIR, filename)
                    if os.path.exists(filepath):
                        with open(filepath, 'r') as f:
                            content = f.read()
                        add_to_history(command.upper(), filename)
                        response = {'status': 'success', 'content': content, 'message': 'File read successfully'}
                    else:
                        response = {'status': 'error', 'message': 'File not found'}

                elif command == 'edit_file':
                    filename = request.get('filename')
                    new_content = request.get('content')
                    filepath = os.path.join(FILES_DIR, filename)
                    if os.path.exists(filepath):
                        with open(filepath, 'w') as f:
                            f.write(new_content)
                        add_to_history("EDIT", filename)
                        response = {'status': 'success', 'message': f'File {filename} updated'}
                    else:
                        response = {'status': 'error', 'message': 'File not found'}

                elif command == 'see_file_operation_history':
                    filename = request.get('filename')
                    # Filtram istoricul pentru un anumit fisier
                    relevant = [h for h in file_history if h['filename'] == filename]
                    response = {'status': 'success', 'history': relevant}

                elif command == 'list_files':
                    files = os.listdir(FILES_DIR)
                    response = {'status': 'success', 'files': files}
                
                elif command == 'logout':
                    authenticated = False
                    response = {'status': 'success', 'message': 'Logged out'}
                
                else:
                    response = {'status': 'error', 'message': f'Unknown command: {command}'}
                
            except Exception as e:
                response = {'status': 'error', 'message': str(e)}
            
            conn.send(json.dumps(response).encode('utf-8'))
    finally:
        conn.close()

def start_server():
    ensure_files_dir()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print("🚀 FTP SERVER STARTED")
    try:
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    finally:
        server_socket.close()

if __name__ == '__main__':
    start_server()