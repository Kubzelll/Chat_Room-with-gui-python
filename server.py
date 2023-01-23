import requests
import threading
import socket

host = '127.0.0.1'
port = 55555


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)
    

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
            #print(message)#debug line
            
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break


def recive():
    while True:
        client, address = server.accept()
        #print(f"client var {client}")#debug line
        #print(f"address var {address}")#debug line
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        client.send(f'\nConnected to the server Your adress: {str(address)}'.encode('ascii'))
        handle_bug = threading.Thread(target=handle, args=(client,))
        handle_bug.start()



print(f'Server is listening on port: {port}')



recive()

