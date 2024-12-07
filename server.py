import mysql.connector
import socket
import threading
import logging

# Configurez le logger
logging.basicConfig(filename='chat_server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_message(message):
    logging.info(message)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3309",
    password="Ch16donbosco",
    database="center"
)
cursor = db.cursor()

clients = []

def handle_client(client_socket, client_address):
    name = None
    try:
        # Authentification
        client_socket.send("LOGIN_PROMPT".encode())
        message = client_socket.recv(1024).decode()
        if message.startswith('LOGIN'):
            _, name, password = message.split()
            if authenticate_user(name, password):
                name = name
                client_socket.send("LOGIN_SUCCESS".encode())
                broadcast(f"{name} a rejoint le chat", client_socket)
                log_message(f"User {name} logged in")
            else:
                client_socket.send("LOGIN_FAILED".encode())
                log_message(f"Failed login attempt for user {name}")
                client_socket.close()
                return

        # Gestion des messages
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            if message.startswith('LOGOUT'):
                broadcast(f"{name} a quitté le chat", client_socket)
                log_message(f"User {name} logged out")
                break
            if name:
                broadcast(f"{name}: {message}", client_socket)
                save_message(name, message)
                log_message(f"Message from {name}: {message}")
    except ConnectionResetError:
        pass
    finally:
        if name:
            broadcast(f"{name} a quitté le chat", client_socket)
            log_message(f"User {name} disconnected")
        clients.remove(client_socket)
        client_socket.close()

def authenticate_user(name, password):
    cursor.execute("SELECT * FROM users WHERE name = %s AND password = %s", (name, password))
    return cursor.fetchone() is not None

def save_message(name, message):
    cursor.execute("INSERT INTO messages (name, message) VALUES (%s, %s)", (name, message))
    db.commit()

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 4000))
    server.listen(5)
    print("Serveur central en écoute sur le port 4000")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    main()
