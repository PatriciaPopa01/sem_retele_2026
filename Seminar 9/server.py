import socket

HOST        = '127.0.0.1'
PORT        = 9999
BUFFER_SIZE = 1024

clienti_conectati = {}
mesaje_postate = {}
next_id = 1

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print("=" * 50)
print(f"  SERVER UDP pornit pe {HOST}:{PORT}")
print("  Asteptam mesaje de la clienti...")
print("=" * 50)

while True:
    try:
        date_brute, adresa_client = server_socket.recvfrom(BUFFER_SIZE)
        mesaj_primit = date_brute.decode('utf-8').strip()

        parti = mesaj_primit.split(' ', 1)
        comanda = parti[0].upper()
        argumente = parti[1] if len(parti) > 1 else ''

        print(f"\n[PRIMIT] De la {adresa_client}: '{mesaj_primit}'")

        if comanda != 'CONNECT' and adresa_client not in clienti_conectati:
            raspuns = "EROARE: Nu esti conectat. Trimite CONNECT mai intai."
        
        elif comanda == 'CONNECT':
            if adresa_client in clienti_conectati:
                raspuns = "EROARE: Esti deja conectat la server."
            else:
                clienti_conectati[adresa_client] = True
                raspuns = f"OK: Conectat cu succes. Clienti activi: {len(clienti_conectati)}"
                print(f"[SERVER] Client nou conectat: {adresa_client}")

        elif comanda == 'DISCONNECT':
            if adresa_client in clienti_conectati:
                del clienti_conectati[adresa_client]
                raspuns = "OK: Deconectat cu succes. La revedere!"
                print(f"[SERVER] Client deconectat: {adresa_client}")
            else:
                raspuns = "EROARE: Nu esti conectat la server."

        elif comanda == 'PUBLISH':
            if not argumente.strip():
                raspuns = "EROARE: Mesajul nu poate fi gol."
            else:
                mesaje_postate[next_id] = {"text": argumente, "autor": adresa_client}
                raspuns = f"OK: Mesaj publicat cu ID={next_id}"
                next_id += 1

        elif comanda == 'DELETE':
            if not argumente.isdigit():
                raspuns = "EROARE: ID-ul trebuie sa fie un numar intreg."
            else:
                id_sters = int(argumente)
                if id_sters in mesaje_postate:
                    if mesaje_postate[id_sters]["autor"] == adresa_client:
                        del mesaje_postate[id_sters]
                        raspuns = f"OK: Mesajul {id_sters} a fost sters."
                    else:
                        raspuns = "EROARE: Nu ai permisiunea sa stergi acest mesaj (nu esti autorul)."
                else:
                    raspuns = f"EROARE: Mesajul cu ID {id_sters} nu a fost gasit."

        elif comanda == 'LIST':
            if not mesaje_postate:
                raspuns = "INFO: Nu exista mesaje de afisat."
            else:
                raspuns = "LISTA MESAJE:\n"
                for mid, date in mesaje_postate.items():
                    raspuns += f"ID {mid}: {date['text']}\n"

        else:
            raspuns = f"EROARE: Comanda '{comanda}' este necunoscuta."

        server_socket.sendto(raspuns.encode('utf-8'), adresa_client)
        print(f"[TRIMIS]  Catre {adresa_client}: '{raspuns}'")

    except KeyboardInterrupt:
        print("\n[SERVER] Oprire server...")
        break
    except Exception as e:
        print(f"[EROARE] {e}")

server_socket.close()