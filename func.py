import types
import random

consts = types.SimpleNamespace()
consts.DATA = 1
consts.MOTIVATIONAL_MESSAGE = 2
consts.SERVER_RESPONSE_COUNT = 3

def generateRandomIdentifier():
    '''Gera um identificador aleatório entre 1 e 65535.'''
    return random.randint(1, 65535)

def splitNumberInto2Bytes(number):
    '''Divide um número em dois bytes.'''
    number = number.to_bytes(2, byteorder='big')
    return number

def transformIPStringToBytes(ip):
    '''Transforma uma string de IP em bytes.'''
    string_list = ip.split('.')
    int_list = [int(i) for i in string_list]
    return bytes(int_list)


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


def calculateChecksum(byte_list):
    '''Calcula o checksum de uma lista de bytes.'''
    list_size = len(byte_list)
    if list_size % 2 != 0:
        byte_list += bytes([0])
    list_size = len(byte_list)
    index = 0
    result = 0
    for _ in range(int(list_size / 4)):
        result = add16BitWords(result, add16BitWords(byte_list[index] << 8 | byte_list[index + 1],
                                                     byte_list[index + 2] << 8 | byte_list[index + 3]))
        index += 4
    return ~result & 0xFFFF

def add16BitWords(word1, word2):
    '''Adiciona duas palavras de 16 bits.'''
    result = word1 + word2
    while result.bit_length() > 16:
        carry = result >> 16
        result &= 0xFFFF
        result += carry
    return result

def displayOptions():
    '''Exibe as opções de requisição.'''
    print("Opções de solicitação:")
    print("1 -> Data e hora")
    print("2 -> Uma mensagem motivacional para o final do semestre")
    print("3 -> A quantidade de respostas emitidas pelo servidor")
    print("4 -> Sair")

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

def bytesToString(byte_list):
    '''Converte uma lista de bytes em uma string.'''
    return ''.join(chr(i) for i in byte_list)

def bytesToInt(byte_list):
    '''Converte uma lista de bytes em um número inteiro.'''
    return int.from_bytes(bytes(byte_list), byteorder='big')
