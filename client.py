from chat_client import ChatClient
from _thread import *
import threading 

def listen_mensage(client):
    while True:
        message =client.rec_message()
        print("("+eval(mensage)['nickname']+")"+
              ": "+eval(mensage)['message'])
        
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
    client.login(nickname,password)
    print("Conectado com o servidor, pode digitar as mensagens")

    t_1 = threading.Thread(target=send_mensage, args=(client,))
    t_2 = threading.Thread(target=listen_mensage, args=(client,))

    t_1.start()

    t_2.start()

    


    
    
       
    