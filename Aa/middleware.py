import socket
import threading
import time

clients = []
servers = [('localhost', 6000), ('localhost', 6001)]  # List of server addresses

def handle_client(client_socket, addr):
    print(f"Client connecté depuis {addr}")
    server_socket = None
    try:
        server_socket = connect_to_server()
        if not server_socket:
            client_socket.send("No available servers".encode())
            client_socket.close()
            return

        while True:
            message = client_socket.recv(1024).decode()
            if message == "DISCONNECT":
                break
            server_socket.send(message.encode())
            response = server_socket.recv(1024).decode()
            client_socket.send(response.encode())
    except:
        pass
    finally:
        if server_socket:
            server_socket.close()
        client_socket.close()
        clients.remove(client_socket)
        print(f"Client déconnecté depuis {addr}")

def connect_to_server():
    for server_address in servers:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect(server_address)
            return server_socket
        except:
            continue
    return None

def routine_maintenance():
    while True:
        time.sleep(30)  # Intervalle de maintenance de 30 secondes
        print("Maintenance de routine :")
        print(f"Clients connectés : {len(clients)}")
        for client in clients:
            print(client.getpeername())
        print("Serveurs disponibles :")
        for server_address in servers:
            print(server_address)

def main():
    middleware = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    middleware.bind(('0.0.0.0', 5000))
    middleware.listen(5)
    print("Middleware en écoute sur le port 5000")

    # Démarrer le thread de maintenance
    maintenance_thread = threading.Thread(target=routine_maintenance)
    maintenance_thread.daemon = True  # Ce thread s'arrêtera lorsque le programme principal s'arrête
    maintenance_thread.start()

    while True:
        client_socket, addr = middleware.accept()
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    main()
