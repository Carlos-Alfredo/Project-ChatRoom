from chat_server import ChatServer
from _thread import *
import threading 
import json
  
def add_users(server):
    print("Conectando Usuarios")
    while True:
        connection,address=server.server_socket.accept()
        server.connection_vector.append(connection)
        mensagem=connection.recv(1024)
        nickname = eval(mensagem.decode())['nickname']
        print(f"User({nickname})(Address): ",address)
        server.nicknames.append(nickname)
        start_new_thread(listen_users,(server,connection))
        server.send_mensage(json.dumps({'mensagem':f'{nickname} entrou no servidor',
                        'nickname':'Server'}).encode())
        
def listen_users(server,connection):
    while True:
        mensagem=connection.recv(1024)
        if not mensagem:
            connection.close()
        else:
            value = server.verify_mensage(connection,mensagem)
            if value==1:
                server.send_mensage(mensagem)
            if value==2:
                connection.close()
                break

server = ChatServer()

server.server_socket.bind(('127.0.0.1',65432))
server.server_socket.listen(1)

t_1 = threading.Thread(target = add_users(server))

t_1.start()
