# PROJETO DE REDES

## Projeto desenvolvido como Trabalho Final da cadeira de Redes de Computadores I

- O programa é implementado na linguagem Python. 

- Implementamos dois clientes (um utilizando socket UDP e outro utilizando socket RAW) de uma
aplicação do tipo cliente/servidor que encaminha requisições para o servidor que está executando através
dos protocolos UDP/IP no endereço IP 15.228.191.109 e porta 50000.

- Cada cliente deve solicitar ao
usuário a escolha de um dos tipos de requisição abaixo:
1. Data e hora atual;
2. Uma mensagem motivacional para o fim do semestre;
3. A quantidade de respostas emitidas pelo servidor até o momento.
4. Sair.

- Uma vez que o usuário tenha feito a sua escolha, o cliente deverá encaminhar uma requisição
devidamente formatada para o servidor. O servidor por sua vez emitirá uma resposta de volta para o cliente utilizando o mesmo formato de
mensagem.

- Em seguida o cliente deverá exibir a resposta recebida pelo servidor de uma forma adequada
para a legibilidade pelo usuário final.

-Por fim, o programa cliente deverá aguardar novas requisições do
cliente até que o usuário selecione a opção “Sair”.


### Para rodar o Cliente UDP
```bash
python3 cliente_udp.py
```

### Para rodar o Cliente RAW
```bash
sudo python3 cliente_raw.py
```

