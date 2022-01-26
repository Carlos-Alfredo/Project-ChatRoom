import json
import socket
from _thread import *
from cbc import cbc_encrypt,cbc_decrypt

class ChatServer():

    def __init__(self):

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_vector = [] #connection,nickname and secret key
        self.credentials = []
    
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

    def send_mensage(self,message,nickname):
        msg=json.dumps({'message':message,
                        'nickname':nickname}).encode()
        for connection in self.connection_vector:
            encrypted_msg=cbc_encrypt(connection[2],msg)
            connection[0].send(encrypted_msg)
    
    '''def list_nicknames(self,connection):

        connection.send(json.dumps(
                        {'message':str(self.nicknames),
                        'nickname':'Server'}
                        ).encode())'''
    
    def remove_user(self,connection_user):

        for i in range(len(self.connection_vector)):
            if self.connection_vector[i][0]==connection_user:
                self.connection_vector.pop(i)
                return 1
        return 0
    
    def verify_mensage(self,connection,message):

        msg=eval(message.decode())['message']
        
        if msg=='/USUARIOS':
            self.list_nicknames(connection)
            return 0
        
        if msg=='/SAIR':
            connection.send(json.dumps({
                            'message':'You have been disconnected from the chat room',
                            'nickname':'Server'}).encode())
            
            nickname = self.remove_user(connection)
            
            self.send_mensage(json.dumps({
                                'message':f'{nickname} left the chat room',
                                'nickname':'Server'}).encode())
            return 2
        
        return 1
             
    