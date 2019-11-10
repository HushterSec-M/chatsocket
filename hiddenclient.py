import socket
server = '192.168.43.3', 5000
sok = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sok.bind(('', 0))
while 1:
    data = sok.recv(1024)
    print(data.decode('utf-8'))