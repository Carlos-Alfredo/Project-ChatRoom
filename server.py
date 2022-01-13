from chat_server import ChatServer
from _thread import *
import threading 
import json
import random
from cbc import cbc_encrypt,cbc_decrypt

def start_connection(server):
    while True:
        connection,address=server.server_socket.accept()
        #server.connection_vector.append(connection)
        message=connection.recv(1024)
        #nickname = eval(message.decode())['nickname']

        public_prime = eval(message.decode())['public_prime']
        public_primitive = eval(message.decode())['public_primitive']
        generated_key_user = eval(message.decode())['generated_key_user']
        private_key=random.randint(1,20)
        generated_key_server = int(pow(public_primitive,private_key,public_prime))
        connection.send(json.dumps({'generated_key_server':generated_key_server}).encode())
        secret_key = int(pow(generated_key_user,private_key,public_prime))

        message=cbc_decrypt(secret_key,connection.recv(1024))
        if not message:
            connection.close()
        else:
            operation=eval(message.decode())['operation']
            if operation=='LOGIN':
                nickname=eval(message.decode())['nickname']
                password=eval(message.decode())['password']
                if server.check_login(nickname,password):
                    server.coonection_vector.append([connection,nickname])
                    message=json.dumps({'response':'You are logged in'}).encode()
                    start_new_thread(listen_users,(server,connection,secret_key,0))
                else:
                    message=json.dumps({'response':'Wrong nickname or password'}).encode()
            if operation=='SIGNUP':
                nickname=eval(message.decode())['nickname']
                password=eval(message.decode())['password']
                if server.create_account(nickname,password):
                    server.coonection_vector.append([connection,nickname])
                    message=json.dumps({'response':'Your account has been created'}).encode()
                    start_new_thread(listen_users,(server,connection,secret_key,0))
                else:
                    message=json.dumps({'response':'Invalid nickname'}).encode()
            message_encrypted=cbc_encrypt(secret_key,message)
            connection.send(message_encrypted)

        
        
def listen_users(server,connection,secret_key,is_login):
    while True:
        message=cbc_decrypt(secret_key,connection.recv(1024))
        if not message:
            connection.close()
        else:
            value = server.verify_mensage(connection,message)
            if value==1:
                server.send_mensage(message)
            if value==2:
                connection.close()
                break

server = ChatServer()

server.server_socket.bind(('127.0.0.1',65432))
server.server_socket.listen(1)

t_1 = threading.Thread(target = add_users(server))

t_1.start()
