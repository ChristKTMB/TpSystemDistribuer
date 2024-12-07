import socket
import threading

def handle_client(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            response = f"Message reçu: {message}"
            client_socket.send(response.encode())
    except:
        pass
    finally:
        client_socket.close()

def main(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"Serveur en écoute sur le port {port}")

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main(6000)  # Start the first server instance
    # main(6001)  # Uncomment to start the second server instance
