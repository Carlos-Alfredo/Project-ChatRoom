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
        #server.connection_vector.append(connection)
        message=connection.recv(1024)
        while not message:
            message=connection.recv(1024)
        #nickname = eval(message.decode())['nickname']

        public_prime = eval(message.decode())['public_prime']
        public_primitive = eval(message.decode())['public_primitive']
        generated_key_user = eval(message.decode())['generated_key_user']
        private_key=random.randint(1,20)
        generated_key_server = int(pow(public_primitive,private_key,public_prime))
        connection.send(json.dumps({'generated_key_server':generated_key_server}).encode())
        secret_key = int(pow(generated_key_user,private_key,public_prime))

        message=connection.recv(1024)
        while not message:
            message=connection.recv(1024)
        message=cbc_decrypt(secret_key,message)
        operation=eval(message.decode())['operation']
        if operation=='LOGIN':
            nickname=eval(message.decode())['nickname']
            password=eval(message.decode())['password']
            if server.check_login(nickname,password):
                server.connection_vector.append([connection,nickname,secret_key])
                message=json.dumps({'response':'You are logged in'}).encode()
                start_new_thread(listen_users,(server,connection,nickname,secret_key,1))
            else:
                message=json.dumps({'response':'Wrong nickname or password'}).encode()
        if operation=='SIGNUP':
            nickname=eval(message.decode())['nickname']
            password=eval(message.decode())['password']
            if server.create_account(nickname,password):
                server.connection_vector.append([connection,nickname,secret_key])
                message=json.dumps({'response':'Your account has been created'}).encode()
                start_new_thread(listen_users,(server,connection,nickname,secret_key,1))
            else:
                message=json.dumps({'response':'Invalid nickname'}).encode()
            message_encrypted=cbc_encrypt(secret_key,message)
            connection.send(message_encrypted)

        
        
def listen_users(server,connection,nickname,secret_key,is_login):
    while is_login:
        tic=time.perf_counter()
        message=connection.recv(1024)
        toc=time.perf_counter()
        while not message and toc-tic<120:
            message=connection.recv(1024)
            toc=time.perf_counter()
        if toc-tic<120:
            message=cbc_decrypt(secret_key,message)
            server.send_mensage(eval(message.decode())['message'],nickname)
        else:
            is_login=0
            connection.close()#Timeout

server = ChatServer()

server.server_socket.bind(('127.0.0.1',65432))
server.server_socket.listen(1)

t_1 = threading.Thread(target = start_connection(server))

t_1.start()
