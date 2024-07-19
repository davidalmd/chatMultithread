import socket
import threading
import os

def handle_client(client_socket):
    def receive_messages():
        while True:
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                if msg.startswith("FILE"):
                    file_info = msg.split()
                    file_name = file_info[1]
                    file_size = int(file_info[2])
                    
                    with open(file_name, 'wb') as f:
                        bytes_received = 0
                        while bytes_received < file_size:
                            chunk = client_socket.recv(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                            bytes_received += len(chunk)
                    print(f"Arquivo {file_name} recebido.")
                else:
                    print(f"Cliente: {msg}")
            except:
                print("Cliente desconectado.")
                client_socket.close()
                break

    def send_messages():
        while True:
            msg = input("Servidor: ")
            if msg.startswith("FILE"):
                file_path = msg.split()[1]
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    client_socket.send(f"FILE {os.path.basename(file_path)} {file_size}".encode('utf-8'))
                    with open(file_path, 'rb') as f:
                        chunk = f.read(1024)
                        while chunk:
                            client_socket.send(chunk)
                            chunk = f.read(1024)
                    print(f"Arquivo {file_path} enviado.")
                else:
                    print("Arquivo não encontrado.")
            else:
                client_socket.send(msg.encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages)
    send_thread.start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(1)
    print("Aguardando conexão de cliente...")

    client_socket, addr = server.accept()
    print(f"Cliente conectado: {addr}")

    handle_client(client_socket)

if __name__ == "__main__":
    main()
