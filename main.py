import socket
import threading

def client(h, p):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.connect((h, p))
        print("Conectado ao servidor")
    except Exception as e:
        print("Erro ao conectar:", e)
        return

    while True:
        try:
            choice = input("Escolha uma opção:\n1. Data e hora atual\n2. Mensagem motivacional\n3. Quantidade de respostas emitidas pelo servidor\n4. Sair\n")
            s.sendall(choice.encode())

            if choice == '4':
                break

            response = s.recv(1024).decode()
            print("Resposta do servidor:", response)
        except Exception as e:
            print("Erro na comunicação com o servidor:", e)
            break

    s.close()
    print("Conexão encerrada")

def server():
    host = '127.0.0.1'
    port = 50000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(2)
    print("Servidor escutando")

    clients = []

    while True:
        conn, addr = s.accept()
        print("Cliente conectado:", addr)
        clients.append(conn)
        
        threading.Thread(target=handle_client, args=(conn, clients)).start()

    s.close()

def handle_client(conn, clients):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            if data == '1':
                conn.sendall("Data e hora atual".encode())
            elif data == '2':
                conn.sendall("Mensagem motivacional para o fim do semestre".encode())
            elif data == '3':
                conn.sendall("Quantidade de respostas emitidas pelo servidor".encode())
            elif data == '4':
                conn.sendall("Saindo...".encode())
                break
            else:
                conn.sendall("Opção inválida".encode())
        except Exception as e:
            print("Erro no cliente:", e)
            break

    conn.close()
    clients.remove(conn)
    print("Cliente desconectado")

if __name__ == '__main__':
    threading.Thread(target=server).start()
    host = input("Entre com o IP do servidor remoto: ")
    port = int(input("Entre com a porta do servidor remoto: "))
    client(host, port)
