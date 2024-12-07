import socket
import threading

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
    client.connect(('localhost', 5000))  # Connect to the middleware

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    try:
        while True:
            message = input()
            if message.lower() == 'exit':
                client.send("DISCONNECT".encode())
                break
            client.send(message.encode())
    except KeyboardInterrupt:
        client.send("DISCONNECT".encode())

    client.close()

if __name__ == "__main__":
    main()
