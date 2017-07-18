import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 1995
BUFFER_SIZE = 1024
MESSAGE = 'Hello, server'

data = bytes(MESSAGE, "ascii")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(data)
data = s.recv(BUFFER_SIZE)
s.close()

print("Received data: ", data)