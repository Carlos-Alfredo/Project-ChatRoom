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
        generated_key_server=eval(self.client_socket.recv(1024).decode())['generated_key_server']
        return int(pow(generated_key_server,self.private_key,self.public_prime))
    
    def login(self,nickname,password):
        message=json.dumps({'operation':'LOGIN',
                            'nickname':nickname,
                            'password':password}).encode()
        encrypted_message=cbc_encrypt(self.secret_key,message)
        self.client_socket.send(encrypted_message)
    
    def rec_message(self):
        message=self.client_socket.recv(1024).decode()
        return message
    
    def send_message(self,message):
        self.client_socket.send(json.dumps({'message':message,
                                            'nickname':self.client.nickname}).encode())

    