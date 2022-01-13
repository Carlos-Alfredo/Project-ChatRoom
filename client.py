from chat_client import ChatClient
from _thread import *
import threading 

def listen_mensage(client):
    while True:
        mensage =client.rec_mensage()
        print("("+eval(mensage)['nickname']+")"+
              ": "+eval(mensage)['mensagem'])
        
        if eval(mensage)['mensagem']=='Você foi desconectado da sala de chat':
            client.client_socket.close()
            break
    
def send_mensage(client):
    while True:    
        mensagem=input('')
        client.send_mensage(mensagem)
        if mensagem=='/SAIR':
            break

user_input = input('Digite /ENTRAR para ENTRAR: ')
if user_input =='/ENTRAR':
    nickname =    input('Digite o seu nickname: ')
    server_ip =   input('Digite o ip do servidor: ')
    server_port = int(input('Digite a porta associada: '))
    # Porta: 65432
    #local_host: '127.0.0.1'
    client = ChatClient(nickname,server_ip,server_port)

    print("Conectado com o servidor, pode digitar as mensagens")

    t_1 = threading.Thread(target=send_mensage, args=(client,))
    t_2 = threading.Thread(target=listen_mensage, args=(client,))

    t_1.start()

    t_2.start()

    


    
    
       
    