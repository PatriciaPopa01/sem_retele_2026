import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999
BUFFER_SIZE = 1024
TIMEOUT     = 5

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

este_conectat = False

def trimite_comanda(mesaj: str) -> str:
    try:
        client_socket.sendto(mesaj.encode('utf-8'), (SERVER_HOST, SERVER_PORT))
        date_brute, _ = client_socket.recvfrom(BUFFER_SIZE)
        return date_brute.decode('utf-8')
    except socket.timeout:
        return "EROARE: Serverul nu raspunde (timeout)."
    except Exception as e:
        return f"EROARE: {e}"

print("=" * 55)
print("  CLIENT UDP - Seminar 9")
print("=" * 55)

while True:
    try:
        intrare = input(">> ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nInchidere client...")
        break

    if not intrare:
        continue

    parti = intrare.split(' ', 1)
    comanda = parti[0].upper()
    argument = parti[1] if len(parti) > 1 else ""

    if comanda == 'EXIT':
        print("Inchidere client...")
        break

    if comanda in ['PUBLISH', 'DELETE', 'LIST', 'DISCONNECT'] and not este_conectat:
        print("EROARE LOCALA: Trebuie sa te conectezi inainte de a folosi aceasta comanda.")
        continue

    if comanda == 'CONNECT':
        raspuns = trimite_comanda(intrare)
        print(raspuns)
        if raspuns.startswith("OK"):
            este_conectat = True

    elif comanda == 'DISCONNECT':
        raspuns = trimite_comanda(intrare)
        print(raspuns)
        if raspuns.startswith("OK"):
            este_conectat = False

    elif comanda == 'PUBLISH':
        if not argument:
            print("EROARE LOCALA: Comanda PUBLISH necesita un mesaj (Ex: PUBLISH salut).")
            continue
        raspuns = trimite_comanda(intrare)
        print(raspuns)

    elif comanda == 'DELETE':
        if not argument or not argument.isdigit():
            print("EROARE LOCALA: Comanda DELETE necesita un ID numeric (Ex: DELETE 1).")
            continue
        raspuns = trimite_comanda(intrare)
        print(raspuns)

    elif comanda == 'LIST':
        raspuns = trimite_comanda(intrare)
        print(raspuns)

    else:
        print(f"Comanda '{comanda}' nu este recunoscuta de client.")

client_socket.close()