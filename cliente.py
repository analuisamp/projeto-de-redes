import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 5000)

    print("Client is running...")

    while True:
        client_message = input("\nEscolha uma opção:\n1. Data e hora atual\n2. Mensagem motivacional para o fim do semestre\n3. Quantidade de respostas emitidas pelo servidor\n4. Sair\n")

        if client_message == '4':  # Verifique se é uma string, pois input retorna uma string
            print("Opção 4 escolhida")
            break
        elif client_message == '1':
            print("Opção 1 escolhida")
        elif client_message == '2':
            print("Opção 2 escolhida")
        elif client_message == '3':
            print("Opção 3 escolhida")

        client_socket.sendto(client_message.encode(), server_address)  # Envia a mensagem para o servidor

        receive_buffer = bytearray(1024)
        receive_packet, _ = client_socket.recvfrom(1024)  # Recebe a resposta do servidor

        server_message = receive_packet.decode()
        print(f"Received from Server: {server_message}")

    client_socket.close()

if __name__ == "__main__":
    main()
