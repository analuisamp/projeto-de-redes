import types
import random
consts = types.SimpleNamespace()
consts.DATA = 1
consts.MOTIVATIONAL_MESSAGE = 2
consts.QUANTITY_RESPONSES_SERVER = 3

def displayOptions():
    print("Request options: ")
    print("1 -> Date and time")
    print("2 -> A motivational message for the end of the semester")
    print("3 -> The number of responses issued by the server")
    print("4 -> Exit")

def Checksum(listBytes):
    sizeList = len(listBytes)
    if sizeList % 2 == 0:                  
       pass
    else:
        listBytes = listBytes + bytes([0])  
    sizeList = len(listBytes)            
    i = 0
    result = 0
    for i in range(int(sizeList/4)):
        result = addWord16Bits(result, addWord16Bits(listBytes[i] << 8 | listBytes[i + 1],listBytes[i + 2] << 8 | listBytes[i + 3]))
        i += 4
    return ~result & 0xFFFF           

def addWord16Bits(word1, word2):
    result = word1 + word2
    while result.bit_length() > 16:   
        carry = result >> 16
        result &= 0xFFFF
        result += carry
    return result

def dividesNumberBytes(n):     
    n = n.to_bytes(2, byteorder='big')
    return n

def transformStringIPemBytes(ip):  
    listString = ip.split('.')
    listInt = []
    for i in listString:
        listInt.append(int(i))
    return bytes(listInt)

def generateRandomIdentifier():          
    return random.randint(1, 65535)

def createRequest(tipo, ID):  
    byte1 = 0b00000000
    bytesID = dividesNumberBytes(ID)
    match tipo:
        case consts.DATA:
            pass
        case consts.MOTIVATIONAL_MESSAGE:
            byte1 = byte1 | 0b0001
        case consts.QUANTITY_RESPONSES_SERVER:
            byte1 = byte1 | 0b0010

    message = bytes([byte1, bytesID[0], bytesID[1]])
    return message

def bytesToString(listBytes):  
    return ''.join(chr(i) for i in listBytes)

def bytesToInteger(listBytes):     
    return int.from_bytes(bytes(listBytes), byteorder='big')

def decodeResponse(data):   
    tipo = data[0]
    tamanho_resposta = data[3]
    listBytes = []
    match tipo:
        case 0x10:
            for i in range(tamanho_resposta):
                listBytes.append(data[4+i])
            return bytesToString(listBytes)
        case 0x11:
            for i in range(tamanho_resposta):
                listBytes.append(data[4+i])
            return bytesToString(listBytes)
        case 0x12:
            for i in range(tamanho_resposta):
                listBytes.append(data[4+i])
            return bytesToInteger(listBytes)
