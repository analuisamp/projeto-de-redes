import socket
import funcoes

# Constants
DESTINATION_IP = '15.228.191.109'
DESTINATION_PORT = 50000
MAX_SIZE = 2040

def findPortOrigin():
    """
    Encontra uma porta disponível no sistema local.
    """
    with socket.socket() as sock:
        sock.bind(('', 0))
        return sock.getsockname()[1]

def findIPOrigin():
    """
    Retorna o endereço IP local.
    """
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def assemblePackageUDP(portOrigin, destinationport, sizePackageUDP, udp_checksum):
    """
    Monta o cabeçalho UDP.
    """
    portOrigin = funcoes.dividesNumberBytes(portOrigin)
    destinationport = funcoes.dividesNumberBytes(destinationport)
    sizePackageUDP = funcoes.dividesNumberBytes(sizePackageUDP)
    udp_checksum = funcoes.dividesNumberBytes(udp_checksum)

    udp_cabecalho = bytes([portOrigin[0], portOrigin[1], destinationport[0], destinationport[1], sizePackageUDP[0], sizePackageUDP[1], udp_checksum[0], udp_checksum[1]])
    return udp_cabecalho

def assemblePseudoCabecalho(ip_origem, ip_destino, sizePackageUDP):
    """
    Monta o pseudo cabeçalho IP.
    """
    protocolo = socket.IPPROTO_UDP.to_bytes(1, byteorder='big')
    ip_origem = funcoes.transformStringIPemBytes(ip_origem)
    ip_destino = funcoes.transformStringIPemBytes(ip_destino)
    zero = 0b00000000
    sizePackageUDP = funcoes.dividesNumberBytes(sizePackageUDP)
    createdHeader = ip_origem + ip_destino + bytes([zero, protocolo[0], sizePackageUDP[0],sizePackageUDP[1]])
    return createdHeader

def extractChargeUtil(data):
    """
    Extrai a carga útil dos data recebidos.
    """
    payload = data[28:]
    return payload

def main():
    """
    Função principal do cliente RAW.
    """
    print("CLIENTE RAW")
    funcoes.displayOptions()
    while True:
        tipo = input("Insira a solicitação: ")

            # Verifica se o tipo inserido é válido
        if tipo not in ["1", "2", "3", "4"]:
            print("Opção inválida. Insira um número entre 1 e 4.")
            continue
            
        if tipo == "4":
            print("Encerrando o programa...")
            break

        data = funcoes.createRequest(int(tipo), funcoes.generateRandomIdentifier())

        # Montagem do cabeçalho UDP
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP) as socket_raw:
                portOrigin = findPortOrigin()
                sizePackageUDP = 8 + len(data)
                udp_checksum = 0
                pacote_udp = assemblePackageUDP(portOrigin, DESTINATION_PORT, sizePackageUDP, udp_checksum)
                segmento = pacote_udp + data

                # Montagem do pseudo cabeçalho IP 
                ip_origem = findIPOrigin()
                createdHeader = assemblePseudoCabecalho(ip_origem, DESTINATION_IP, sizePackageUDP)
                udp_checksum = funcoes.Checksum(createdHeader + segmento)
                pacote_udp = assemblePackageUDP(portOrigin, DESTINATION_PORT, sizePackageUDP, udp_checksum)

                endereco_destino = (DESTINATION_IP, DESTINATION_PORT)
                socket_raw.sendto(segmento, endereco_destino)

                data, endereco_origem = socket_raw.recvfrom(MAX_SIZE)
                payload = extractChargeUtil(data)
                resposta = funcoes.decodeResponse(payload)
                print(resposta)
        except PermissionError:
            print("Erro de permissão. Execute o programa como administrador.")
            break
        except socket.error as e:
            print("Erro de socket:", e)
            break
        except Exception as e:
            print("Erro:", e)
            break

if __name__ == "__main__":
    main()
