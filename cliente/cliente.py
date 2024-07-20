import socket
import threading
import os
from colorama import init, Fore, Style
import sys

init()

def delete_last_line():
    sys.stdout.write('\033[A')
    sys.stdout.write('\033[K')
    sys.stdout.flush()

def handle_server(server_socket, name, my_color, their_color):
    def receive_messages():
        while True:
            try:
                msg = server_socket.recv(1024).decode('utf-8')
                if msg.upper().startswith("ARQUIVO"):
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
                    print(f"\n{Fore.GREEN}Arquivo {file_name} recebido.{Style.RESET_ALL}")
                else:
                    print(f"\n{their_color}{msg}{Style.RESET_ALL}")
                print(f"{my_color}{name}: {Style.RESET_ALL}", end="", flush=True)
            except:
                print(f"\n{Fore.RED}Conexão com o servidor perdida.{Style.RESET_ALL}")
                server_socket.close()
                break

    def send_messages():
        nonlocal name, my_color, their_color
        while True:
            print(f"{my_color}{name}: {Style.RESET_ALL}", end="", flush=True)
            msg = input()
            if msg.upper() == "MENU":
                print("1. Trocar nome")
                print("2. Trocar cor do meu texto")
                print("3. Trocar cor do texto do outro usuário")
                print("4. Sair")
                option = input("Escolha uma opção: ")
                if option == "1":
                    name = input("Digite o novo nome: ")
                elif option == "2":
                    my_color = choose_color()
                elif option == "3":
                    their_color = choose_color()
                elif option == "4":
                    server_socket.close()
                    print(f"{Fore.RED}Você saiu do chat.{Style.RESET_ALL}")
                    break
            elif msg.upper().startswith("ARQUIVO"):
                file_path = msg.split()[1]
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    server_socket.send(f"ARQUIVO {os.path.basename(file_path)} {file_size}".encode('utf-8'))
                    with open(file_path, 'rb') as f:
                        chunk = f.read(1024)
                        while chunk:
                            server_socket.send(chunk)
                            chunk = f.read(1024)
                    print(f"\n{Fore.GREEN}Arquivo {file_path} enviado.{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}Arquivo não encontrado.{Style.RESET_ALL}")
            else:
                delete_last_line()
                print(f"{my_color}{name}: {msg}{Style.RESET_ALL}")
                server_socket.send(f"{name}: {msg}".encode('utf-8'))

    def choose_color():
        print("Escolha uma cor:")
        print("1. Vermelho")
        print("2. Verde")
        print("3. Amarelo")
        print("4. Azul")
        print("5. Magenta")
        print("6. Ciano")
        print("7. Branco")
        color_option = input("Escolha uma opção: ")
        if color_option == "1":
            return Fore.RED
        elif color_option == "2":
            return Fore.GREEN
        elif color_option == "3":
            return Fore.YELLOW
        elif color_option == "4":
            return Fore.BLUE
        elif color_option == "5":
            return Fore.MAGENTA
        elif color_option == "6":
            return Fore.CYAN
        elif color_option == "7":
            return Fore.WHITE
        else:
            print("Opção inválida. Usando cor padrão (Branco).")
            return Fore.WHITE

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages)
    send_thread.start()

def main():
    name = input("Digite seu nome: ")
    my_color = Fore.WHITE
    their_color = Fore.WHITE

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))
    print("Conectado ao servidor.")

    handle_server(client, name, my_color, their_color)

if __name__ == "__main__":
    main()
