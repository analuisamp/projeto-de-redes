import socket
import funcoes

def main():
    print("CLIENTE UDP")
    
    # Exibe as opções de solicitação para o usuário
    funcoes.displayOptions()
    
    # Cria o socket UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    
    try:
        while True:
            tipo = input("Insira a solicitação: ")
            
            # Verifica se o tipo inserido é válido
            if tipo not in ["1", "2", "3", "4"]:
                print("Opção inválida. Insira um número entre 1 e 4.")
                continue
            
            if tipo == "4":
                print("Encerrando o programa...")
                break
            
            # Gera a mensagem a ser enviada para o servidor conforme a solicitação
            mensagem = funcoes.createRequest(int(tipo), funcoes.generateRandomIdentifier()) 
            endereco_destino = ('15.228.191.109', 50000) # Endereço do servidor
            
            # Envia a mensagem para o servidor
            udp_socket.sendto(mensagem, endereco_destino) 
            
            # Recebe a resposta do servidor
            dados, endereco_origem = udp_socket.recvfrom(2040) 
            resposta = funcoes.decodeResponse(dados) # Decodifica a resposta de acordo com o tipo da solicitação
            print(resposta)
    finally:
        udp_socket.close() # Fecha o socket após todas as operações

if __name__ == "__main__":
    main()
