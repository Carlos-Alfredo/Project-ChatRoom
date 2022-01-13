from chat_user import ChatUser
import json
import socket

class ChatClient():
    def __init__(self,nickname,server_ip,server_port):
        self.client = ChatUser(nickname,server_ip,server_port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, server_port))
        self.send_mensage('')
        
    def rec_mensage(self):
        mensagem=self.client_socket.recv(1024).decode()
        return mensagem
    
    def send_mensage(self,mensagem):
        self.client_socket.send(json.dumps({'mensagem':mensagem,
                                            'nickname':self.client.nickname}).encode())
    