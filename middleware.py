import socket
import threading
import logging
import time

# Configuration du journal
logging.basicConfig(filename='middleware.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_request(message, direction):
    logging.info(f"{direction}: {message}")

def handle_client(client_socket, server_socket):
    try:
        while True:
            # Recevoir le message du client
            message = client_socket.recv(1024)
            if not message:
                print("Client disconnected")
                break
            decoded_message = message.decode()
            print(f"Middleware received from client: {decoded_message}")

            # Journaliser la demande du client
            log_request(decoded_message, "Client to Middleware")

            # Envoyer le message au serveur
            server_socket.send(message)
            response = server_socket.recv(1024)
            decoded_response = response.decode()
            print(f"Middleware received from server: {decoded_response}")

            # Journaliser la réponse du serveur
            log_request(decoded_response, "Server to Middleware")

            # Renvoyer la réponse au client
            client_socket.send(response)
            print(f"Middleware sent to client: {decoded_response}")
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
    print("Connected to main server on port 4000")

    while True:
        client_socket, addr = middleware_server.accept()
        print(f"Middleware accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, server_socket))
        client_handler.start()

if __name__ == "__main__":
    main()
