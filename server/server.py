#сокет датаграммный IPv4
import socket                                               #подключаем библиотеку с сокетами

import sqlite3
conn = sqlite3.connect("DB.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS messages (PID INTEGER PRIMARY KEY AUTOINCREMENT, 
            text VARCHAR(100))""")

def sql():
    cursor.execute("SELECT text FROM messages")
    rows = cursor.fetchall()
    for row in rows:
        for col in row:
            print(col)
            yield col


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      #создаём объект сокета (AF_INET - означает тип сокета IPv4, SOCK_DGRAM - означает, что сокет будет датаграммный)
sock.bind(('',5000))                                        #привязываем сокет к адрессу и порту(если нужно потестить на одном компе, то ip сделай 127.0.0.1)
clients = []                                                #массив где храним адреса клиентов`

print('____Start Server____')                               #сообщение об успешном создании сокета
while 1:                                                    #бесконечный цикл
    data, addres = sock.recvfrom(1024)                      #выделяем 1024байта памяти для нашего сокета и заносим в переменные данные
    cursor.execute(f"""INSERT INTO messages (text) VALUES('{data.decode("utf-8").replace("'", '"')}')""")
    #print(addres[0], addres[1])                      #выводим на сервере адреса и идентификаторы пользователей
    if addres not in clients:                              #если пользователя ещё не было, то мы заносим его в список
        clients.append(addres)                              #добавление addres в список clients
        messages = list(sql())[:-1]
        #print(messages)
        for client in clients:
            if client != addres: continue
            if messages[:-1]:
                message = "\n".join(list(map(lambda x: str(x),messages)))
                sock.sendto(bytes(message, 'utf-8'), client)
                #print(f"Отправил : '{messages}'")
    for client in clients:                                  #перебираем всех пользователей
        if client == addres:                                #если при переборе мы попали на пользователя, то ничего не делаем
            continue                                        #continue пропускает одну иттерацию цикла
        sock.sendto(data, client)                           #во всех остальных случаях мы выводим сообщение