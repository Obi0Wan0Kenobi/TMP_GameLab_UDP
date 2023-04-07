import socket


if __name__ == '__main__':
    host = 'localhost'
    port = 12345
    address = (host, port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    game=True
    while game:
        print("===========================================")
        message = input('rock - 1; cisors - 2; paper - 3 : ')
        ok=True
        while ok:
            try:
                int(message)
                ok=False
            except:
                message = input('rock - 1; cisors - 2; paper - 3 : ')
        client_socket.sendto(("start:"+message).encode(), address)

        data, addr = client_socket.recvfrom(1024)
        while data.decode().split(":")[0] != "win" and data.decode().split(":")[0] != "lose" and data.decode().split(":")[0] != "draw":
            print(data.decode())
            if data.decode().split(":")[0]=="id":
                print(f"Ваш айди: "+data.decode().split(":")[1])
            if data.decode().split(":")[0]=="wait":
                print(f"Ищем противника")
            data, addr = client_socket.recvfrom(1024)



        if data.decode().split(":")[0] == "win":
            print("Вы выиграли игрока с id: "+data.decode().split(":")[1])
        elif data.decode().split(":")[0] == "lose":
            print("Вы проиграли игроку с id: " + data.decode().split(":")[1])
        elif data.decode().split(":")[0] == "draw":
            print("У вас ничья с игроком id: " + data.decode().split(":")[1])

        restart=input("0 - выйти, 1 - сыграть еще : ")
        if restart=="0":
            game=False
    client_socket.close()