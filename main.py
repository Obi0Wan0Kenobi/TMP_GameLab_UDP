import random
import socket
import threading
import time

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server address and port
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))


usermas={}
for i in usermas.values():
    id = random.randint(1, 200)

    while id in usermas.keys():
        id = random.randint(1, 200)
    if i.id != id and i.busy == False:
        usermas[i.id].playwith = id
        usermas[i.id].busy = True
        busy = True
        playwith = i.id
class Player:
    def __init__(self,addr,selected,id):
        self.id = id
        self.busy = False
        self.addr = addr

        self.selected=selected
        self.checked=False

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

while True:
    data, addr = server_socket.recvfrom(1024)
    datafromuser = data.decode().split(":")
    if datafromuser[0] == "start":
        selected = int(datafromuser[1])
        id = random.randint(1, 200)
        while id in usermas.keys():
            id = random.randint(1, 200)
        enemy=None
        server_socket.sendto(("id:" + str(id)).encode(), addr)
        for i in usermas.values():
            if i.busy==False:
                enemy = i
                del usermas[i.id]
                break



        if not enemy is None:
            if enemy.selected == selected:
                server_socket.sendto(("draw:" + str(id)).encode(), enemy.addr)
                server_socket.sendto(("draw:" + str(enemy.id)).encode(), addr)
            else:
                playerwin = False
                if enemy.selected == 1 and selected == 3:
                    playerwin=True
                if enemy.selected == 2 and selected == 1:
                    playerwin=True
                if enemy.selected == 3 and selected == 2:
                    playerwin=True

                if playerwin:
                    server_socket.sendto(("lose:"+str(id)).encode(),enemy.addr)
                    server_socket.sendto(("win:" + str(enemy.id)).encode(), addr)
                else:
                    server_socket.sendto(("win:" + str(id)).encode(), enemy.addr)
                    server_socket.sendto(("lose:" + str(enemy.id)).encode(), addr)

        else:
            usermas[id]=Player(addr,selected,id)
            server_socket.sendto(("wait:" + str(id)).encode(), addr)





    print(f'Accepted connection from {addr,data.decode()}')