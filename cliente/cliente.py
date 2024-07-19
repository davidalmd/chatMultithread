import socket
import threading
import os

def handle_server(server_socket):
    def receive_messages():
        while True:
            try:
                msg = server_socket.recv(1024).decode('utf-8')
                if msg.startswith("FILE"):
                    file_info = msg.split()
                    file_name = file_info[1]
                    file_size = int(file_info[2])
                    
                    with open(file_name, 'wb') as f:
                        bytes_received = 0
                        while bytes_received < file_size:
                            chunk = server_socket.recv(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                            bytes_received += len(chunk)
                    print(f"Arquivo {file_name} recebido.")
                else:
                    print(f"Servidor: {msg}")
            except:
                print("Conexão com o servidor perdida.")
                server_socket.close()
                break

    def send_messages():
        while True:
            msg = input("Cliente: ")
            if msg.startswith("FILE"):
                file_path = msg.split()[1]
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    server_socket.send(f"FILE {os.path.basename(file_path)} {file_size}".encode('utf-8'))
                    with open(file_path, 'rb') as f:
                        chunk = f.read(1024)
                        while chunk:
                            server_socket.send(chunk)
                            chunk = f.read(1024)
                    print(f"Arquivo {file_path} enviado.")
                else:
                    print("Arquivo não encontrado.")
            else:
                server_socket.send(msg.encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages)
    send_thread.start()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))
    print("Conectado ao servidor.")

    handle_server(client)

if __name__ == "__main__":
    main()
