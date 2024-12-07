import socket
import threading
import signal
import sys

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"\n{message}")
        except:
            print("\nDéconnexion du serveur")
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 4000))

    def handle_signal(signum, frame):
        client.send("LOGOUT".encode())
        client.close()
        sys.exit()

    signal.signal(signal.SIGINT, handle_signal)

    login_response = client.recv(1024).decode()
    if login_response == "LOGIN_PROMPT":
        name = input("Nom : ")
        password = input("Mot de passe : ")
        client.send(f"LOGIN {name} {password}".encode())
        login_response = client.recv(1024).decode()
        if login_response == "LOGIN_SUCCESS":
            print("Connecté avec succès")
            receive_thread = threading.Thread(target=receive_messages, args=(client,))
            receive_thread.start()

            while True:
                message = input("Message : ")
                if message.lower() == 'exit':
                    client.send("LOGOUT".encode())
                    break
                client.send(message.encode())
        else:
            print("Échec de la connexion")
    else:
        print("Erreur lors de la réception du prompt de connexion")
    
    client.close()

if __name__ == "__main__":
    main()
