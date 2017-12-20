import time
import socket
import random

TCP_IP = '171.227.31.131'
TCP_PORT = 1995
BUFFER_SIZE = 1024

# MESSAGE = '12-11-3309A7363'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while True:
    MESSAGE = ''
    MESSAGE += 'nodea' + '-'
    MESSAGE += str(random.uniform(2.5, 5))
    # MESSAGE += str(random.uniform(2.5, 5)) + '-'
    data = bytes(MESSAGE, "ascii")
    s.send(data)
    # data = s.recv(BUFFER_SIZE)
    # print("Received data: ", data)
    time.sleep(5)


