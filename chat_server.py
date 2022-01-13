import json
import socket
from _thread import *

class ChatServer():

    def __init__(self):

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_vector = []
        self.login = []
    
    def check_login(self,nickname,password):
        for credentials in self.login:
            if(credentials[0]==nickname and credentials[1]==password):
                return 1
        return 0

    def create_account(self,nickname,password):
        for credentials in self.login:
            if(credentials[0]==nickname):
                return 0
        self.login.append([nickname,password])
        return 1

    def send_mensage(self,message):

        for connection in self.connection_vector:
            connection.send(message)
    
    def list_nicknames(self,connection):

        connection.send(json.dumps(
                        {'message':str(self.nicknames),
                        'nickname':'Server'}
                        ).encode())
    
    def remove_user(self,connection_user):

        for i in range(len(self.connection_vector)):
            if self.connection_vector[i]==connection_user:
                self.connection_vector.pop(i)
                nickname = self.nicknames.pop(i)
                return nickname
    
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
             
    