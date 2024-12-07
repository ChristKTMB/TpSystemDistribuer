import socket
import threading

def handle_client(client_socket, server_socket):
    try:
        while True:
            # Recevoir le message du client
            message = client_socket.recv(1024)
            if not message:
                print("Client disconnected")
                break
            print(f"Middleware received from client: {message.decode()}")

            # Envoyer le message au serveur
            server_socket.send(message)
            response = server_socket.recv(1024)
            print(f"Middleware received from server: {response.decode()}")

            # Renvoyer la réponse au client
            client_socket.send(response)
            print(f"Middleware sent to client: {response.decode()}")
    except ConnectionResetError:
        print("ConnectionResetError: Client disconnected")
    finally:
        client_socket.close()

def main():
    # Serveur middleware pour gérer les connexions des clients
    middleware_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    middleware_server.bind(('0.0.0.0', 5000))
    middleware_server.listen(5)
    print("Middleware en écoute sur le port 5000")

    # Connexion au serveur de chat principal
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(('localhost', 4000))

    while True:
        client_socket, addr = middleware_server.accept()
        print(f"Middleware accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, server_socket))
        client_handler.start()

if __name__ == "__main__":
    main()
