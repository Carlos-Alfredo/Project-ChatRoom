from chat_server import ChatServer
from _thread import *
import threading 
import json
import random
from cbc import cbc_encrypt,cbc_decrypt
import time


def start_connection(server):
    while True:
        connection,address=server.server_socket.accept()
        message=connection.recv(1024)
        while not message:
            message=connection.recv(1024)
        
        tic=time.perf_counter()
        
        public_prime = eval(message.decode())['public_prime']
        public_primitive = eval(message.decode())['public_primitive']
        generated_key_user = eval(message.decode())['generated_key_user']
        private_key=random.randint(pow(10,100),pow(10,101))
        generated_key_server = int(pow(public_primitive,private_key,public_prime))
        connection.send(json.dumps({'generated_key_server':generated_key_server}).encode())
        secret_key = int(pow(generated_key_user,private_key,public_prime))
        
        toc=time.perf_counter()
        '''with open('diffie_hellman_timer.json') as f:
            diffie_hellman_timer=json.load(f)
        diffie_hellman_timer.append(toc-tic)
        with open('diffie_hellman_timer.json', 'w') as f:
            json.dump(diffie_hellman_timer,f)'''


        message=connection.recv(1024)
        while not message:
            message=connection.recv(1024)
        server.verify_message(connection,message,secret_key,'')
def server_management(server):
    while True:
        server.save_credentials()


server = ChatServer('credentials.json')

server.server_socket.bind(('127.0.0.1',65432))
server.server_socket.listen(1)

t_1 = threading.Thread(target = start_connection(server))
t_2 = threading.Thread(target = server_management(server))

t_1.start()
t_2.start()
