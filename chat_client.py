from chat_user import ChatUser
import json
import socket
import random
from cbc import cbc_encrypt,cbc_decrypt

class ChatClient():
    def __init__(self,server_ip,server_port):
        self.client = ChatUser('',server_ip,server_port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, server_port))
        self.public_prime=17
        self.public_primitive=7
        self.private_key=random.randint(1,20)
        self.secret_key=self.set_secret()

    def set_secret(self):
        generated_key_user = int(pow(self.public_primitive,self.private_key,self.public_prime))
        self.client_socket.send(json.dumps({'public_prime':self.public_prime,
                                            'public_primitive':self.public_primitive,
                                            'generated_key_user':generated_key_user}).encode())
        message=self.client_socket.recv(1024)
        while not message:
            message=connection.recv(1024)
        generated_key_server=eval(message.decode())['generated_key_server']
        return int(pow(generated_key_server,self.private_key,self.public_prime))
    
    def login(self,nickname,password):
        message=json.dumps({'operation':'LOGIN',
                            'nickname':nickname,
                            'password':password}).encode()
        encrypted_message=cbc_encrypt(self.secret_key,message)
        self.client_socket.send(encrypted_message)
        response=self.client_socket.recv(1024)
        while not response:
            response=connection.recv(1024)
        response=cbc_decrypt(secret_key,response)
        if eval(response.decode())['response']=='You are logged in':
            return 1
        else:
            return 0

    def create_account(self,nickname,password):
        message=json.dumps({'operation':'SIGNUP',
                            'nickname':nickname,
                            'password':password}).encode()
        encrypted_message=cbc_encrypt(self.secret_key,message)
        self.client_socket.send(encrypted_message)
        response=self.client_socket.recv(1024)
        while not response:
            response=connection.recv(1024)
        response=cbc_decrypt(self.secret_key,response)
        if eval(response.decode())['response']=='Your account has been created':
            return 1
        else:
            return 0
    
    def rec_message(self):
        message=self.client_socket.recv(1024)
        while not message:
            message=connection.recv(1024)
        message=cbc_decrypt(self.secret_key,message).decode()
        return message
    
    def send_message(self,message):
        msg=json.dumps({'message':message}).encode()
        encrypted_message=cbc_encrypt(self.secret_key,msg)
        self.client_socket.send(encrypted_message)

    