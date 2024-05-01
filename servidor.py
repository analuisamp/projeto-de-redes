import socket

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 5000))

    print("Server is running...")

    while True:
        receive_buffer = bytearray(1024)
        receive_packet, client_address = server_socket.recvfrom(1024)  # Recebe a mensagem do cliente

        client_message = receive_packet.decode()
        print("Received from Client:", client_message)

        server_message = ""
        if client_message == '4':
            print("Opção 4 escolhida")
            break  # Encerra o loop para fechar o servidor
        elif client_message == '1':
            server_message = "Data e hora atual"
            print("Data e hora atual")
        elif client_message == '2':
            server_message = "Mensagem motivacional para o fim do semestre"
            print("Mensagem motivacional para o fim do semestre")
        elif client_message == '3':
            server_message = "Quantidade de respostas emitidas pelo servidor"
            print("Quantidade de respostas emitidas pelo servidor")

        send_buffer = server_message.encode()
        server_socket.sendto(send_buffer, client_address)  # Envia a resposta para o cliente

    server_socket.close()

if __name__ == "__main__":
    main()
