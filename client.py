from chat_client import ChatClient
from _thread import *
import threading
import asyncio

def listen_message(client):
    while True:
        message =client.rec_message()
        print("("+eval(message)['nickname']+")"+
              ": "+eval(message)['message'])
        
        if eval(message)['message']=='You have been disconnected from the chat room':
            client.client_socket.close()
            break
    
def send_message(client):
    while True:    
        message=input('')
        client.send_message(message)
        if message=='/LOGOUT':
            break

#server_ip =   input('Type the server IP: ')
#server_port = int(input('Type the server port: '))
server_ip = '127.0.0.1'
server_port = 65432
client = ChatClient(server_ip,server_port)
user_input = input('Type /LOGIN to LOGIN\nType /SIGNUP to SIGN UP: ')
if user_input =='/LOGIN':
    nickname = input('Type your nickname: ')
    password = input('Type your password: ')
    if client.login(nickname,password)==1:
        print("Conectado com o servidor, pode digitar as mensagens")
    else:
        print("Login e/ou senha incorretos")
if user_input =='/SIGNUP':
    nickname = input('Type a nickname: ')
    password = input('Type a password: ')
    if client.create_account(nickname,password)==1:
        print("Conta cadastrada com sucesso")
    else:
        print("Nome de usuario invalido")

    t_1 = threading.Thread(target=send_message, args=(client,))
    t_2 = threading.Thread(target=listen_message, args=(client,))

    t_1.start()

    t_2.start()

    


    
    
       
    