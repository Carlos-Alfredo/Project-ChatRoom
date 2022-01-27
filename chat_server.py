import json
import socket
from _thread import *
from cbc import cbc_encrypt,cbc_decrypt
import time

class ChatServer():

    def __init__(self,credentials_file_path):

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_vector = [] #connection,nickname and secret key
        with open(credentials_file_path) as f:
            self.credentials = json.load(f)#nickname,password
        
    
    def check_login(self,nickname,password):
        for cred in self.credentials:
            if(cred[0]==nickname and cred[1]==password):
                return 1
        return 0

    def create_account(self,nickname,password):
        for cred in self.credentials:
            if(cred[0]==nickname):
                return 0
        self.credentials.append([nickname,password])
        return 1

    def send_message(self,message,nickname):
        msg=json.dumps({'message':message,
                        'nickname':nickname}).encode()
        for connection in self.connection_vector:
            encrypted_msg=cbc_encrypt(connection[2],msg)
            connection[0].send(encrypted_msg)
    
    def remove_user(self,connection_user):

        for i in range(len(self.connection_vector)):
            if self.connection_vector[i][0]==connection_user:
                nickname=self.connection_vector[i][1]
                self.connection_vector[i][0].close()
                self.connection_vector.pop(i)
                return nickname
        return 0
    
    def verify_message(self,connection,message,secret_key,nickname):
        return_code=0
        message=cbc_decrypt(secret_key,message)
        operation=eval(message.decode())['operation']
        if operation=='LOGIN':
            nickname=eval(message.decode())['nickname']
            password=eval(message.decode())['password']
            if self.check_login(nickname,password):
                self.connection_vector.append([connection,nickname,secret_key])
                message=json.dumps({'response':'You are logged in'}).encode()
                start_new_thread(listen_users,(self,connection,nickname,secret_key,1))
                return_code=1
            else:
                message=json.dumps({'response':'Wrong nickname or password'}).encode()
            message_encrypted=cbc_encrypt(secret_key,message)
            connection.send(message_encrypted)
        elif operation=='SIGNUP':
            nickname=eval(message.decode())['nickname']
            password=eval(message.decode())['password']
            if self.create_account(nickname,password):
                self.connection_vector.append([connection,nickname,secret_key])
                message=json.dumps({'response':'Your account has been created'}).encode()
                start_new_thread(listen_users,(self,connection,nickname,secret_key,1))
                return_code=1
            else:
                message=json.dumps({'response':'Invalid nickname'}).encode()
            message_encrypted=cbc_encrypt(secret_key,message)
            connection.send(message_encrypted)
        elif operation=='LOGOUT':
            message_user=json.dumps({'response':'You have been disconnected from the chat room'}).encode()
            message_user_encrypted=cbc_encrypt(secret_key,message)
            connection.send(message_user_encrypted)
            nickname = self.remove_user(connection)
            if nickname!=0:
                message_server=nickname+' left the chat room.'
                self.send_message(message_server,'Server')
            return_code=-1
        elif operation=='SENDMESSAGE':
            message=eval(message.decode())['message']
            self.send_message(message,nickname)
            return_code=1
        return return_code

    def save_credentials(self):
        with open(credentials_file_path,'w') as f:
            json.dump(self.credentials,f)
             
def listen_users(server,connection,nickname,secret_key,is_login):
    while is_login:
        tic=time.perf_counter()
        message=connection.recv(1024)
        toc=time.perf_counter()
        while not message and toc-tic<120:
            message=connection.recv(1024)
            toc=time.perf_counter()
        if toc-tic<120:
            return_code=server.verify_message(connection,message,secret_key,nickname)
            if return_code==-1:
                is_login=0
                connection.close()
            #message=cbc_decrypt(secret_key,message)
            #server.send_mensage(eval(message.decode())['message'],nickname)
        else:
            is_login=0
            connection.close()#Timeout
    