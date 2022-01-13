import json
import socket
from _thread import *

class ChatServer():

    def __init__(self):

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_vector = []
        self.nicknames = []
        
    def send_mensage(self,mensagem):

        for connection in self.connection_vector:
            connection.send(mensagem)
    
    def list_nicknames(self,connection):

        connection.send(json.dumps(
                        {'mensagem':str(self.nicknames),
                        'nickname':'Server'}
                        ).encode())
    
    def remove_user(self,connection_user):

        for i in range(len(self.connection_vector)):
            if self.connection_vector[i]==connection_user:
                self.connection_vector.pop(i)
                nickname = self.nicknames.pop(i)
                return nickname
    
    def verify_mensage(self,connection,mensagem):

        msg=eval(mensagem.decode())['mensagem']
        
        if msg=='/USUARIOS':
            self.list_nicknames(connection)
            return 0
        
        if msg=='/SAIR':
            connection.send(json.dumps({
                            'mensagem':'Você foi desconectado da sala de chat',
                            'nickname':'Server'}).encode())
            
            nickname = self.remove_user(connection)
            
            self.send_mensage(json.dumps({
                                'mensagem':f'{nickname} saiu do chat',
                                'nickname':'Server'}).encode())
            return 2
        
        return 1
             
    