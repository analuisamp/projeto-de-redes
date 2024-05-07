import types
import random
import socket

consts = types.SimpleNamespace()
consts.DATA = 1
consts.MOTIVATIONAL_MESSAGE = 2
consts.SERVER_RESPONSE_COUNT = 3

def splitNumberInto2Bytes(number):
    '''Divide um número em dois bytes.'''
    number = number.to_bytes(2, byteorder='big')
    return number

def createRequest(type, identifier):
    '''Cria uma mensagem de requisição com base no tipo e no identificador.'''
    byte1 = 0b00000000
    bytes_identifier = splitNumberInto2Bytes(identifier)
    match type:
        case consts.DATA:
            byte1 = byte1 | 0b0000
        case consts.MOTIVATIONAL_MESSAGE:
             byte1 = byte1 | 0b0001
        case consts.SERVER_RESPONSE_COUNT:
            byte1 = byte1 | 0b0010
        case _:
            byte1 =byte1|0b0011

    message = bytes([byte1, bytes_identifier[0], bytes_identifier[1]])
    return message

def generateRandomIdentifier():
    '''Gera um identificador aleatório entre 1 e 65535.'''
    return random.randint(1, 65535)

def displayOptions():
    '''Exibe as opções de requisição.'''
    print("Opções de solicitação:")
    print("1 -> Data e hora")
    print("2 -> Uma mensagem motivacional para o final do semestre")
    print("3 -> A quantidade de respostas emitidas pelo servidor")
    print("4 -> Sair")

def bytesToString(byte_list):
    '''Converte uma lista de bytes em uma string.'''
    return ''.join(chr(i) for i in byte_list)

def bytesToInt(byte_list):
    '''Converte uma lista de bytes em um número inteiro.'''
    return int.from_bytes(bytes(byte_list), byteorder='big')

def decodeResponse(data):
    '''Decodifica os dados da resposta.'''
    type = data[0]
    response_size = data[3]
    byte_list = []
    if type in [0x10, 0x11, 0x12]:
        for i in range(response_size):
            byte_list.append(data[4+i])
        if type in [0x10, 0x11]:
            return bytesToString(byte_list)
        elif type == 0x12:
            return bytesToInt(byte_list)   

''' Ponto de entrada principal do programa cliente UDP, que interage com um servidor remoto para realizar solicitações e exibir as respostas correspondentes ao usuário. '''
def main():
    
    print("CLIENTE UDP")
    displayOptions()  
    
    while True:
        type = input("Insira a solicitação: ")
        if (type == "4"):
            print("Encerrando o programa...")
            break
        ''' # Cria o socket UDP '''
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        message = createRequest(int(type), generateRandomIdentifier()) 
        ''' # Endereço do servidor remoto '''
        addressDestination = ('15.228.191.109', 50000)  
        udp_socket.sendto(message, addressDestination)  
        dados, addressOrigin = udp_socket.recvfrom(2040)  
        resposta = decodeResponse(dados) 
        print(resposta)
        udp_socket.close()

if __name__ == "__main__":
    main()
