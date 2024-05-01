import socket
import datetime

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 5000))

    print("Server is running...")
    response_count = 0  # Inicializa response_count aqui

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
            response_count += 1
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            server_message = f"Data e hora atual: {current_time}"
            print("Data e hora atual:", current_time)
        elif client_message == '2':
            response_count += 1
            server_message = "Lembre-se de manter o foco, a determinação e a perseverança.\n"
            print("Mensagem motivacional para o fim do semestre")
        elif client_message == '3':
            response_count += 1  # Incrementa response_count
            server_message = f"Quantidade de respostas emitidas pelo servidor: {response_count}"
            print("Quantidade de respostas emitidas pelo servidor:", response_count)

        send_buffer = server_message.encode()
        server_socket.sendto(send_buffer, client_address)  # Envia a resposta para o cliente

    server_socket.close()

if __name__ == "__main__":
    main()

