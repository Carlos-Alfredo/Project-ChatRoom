from chat_client import ChatClient
from _thread import *
import threading
import random
import string

server_ip = '127.0.0.1'
server_port = 65432

for i in range(0,1):
	client = ChatClient(server_ip,server_port)
	nickname=''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
	password=''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
	client.create_account(nickname,password)