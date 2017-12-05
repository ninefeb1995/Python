import socket
import threading
# from dashboard.models import RawData
# from manage_devices.models import Node
# from datetime import datetime
# import os
# import django


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        print("Server is listening !")
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target=self.listen_to_client, args=(client, address)).start()

    def listen_to_client(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # # Set the response to echo back the recieved data
                    # print(data)
                    # response = data
                    # client.send(response)
                    # # handle data here
                    # co, oxi, node = data.split(';')
                    # node_id = Node.objects.get(node)
                    # new_data = RawData(oxi=oxi,
                    #                    co=co,
                    #                    node=node_id,
                    #                    node_name=node_id.name,
                    #                    measuring_date=datetime.now())
                    # new_data.save(force_insert=True)
                    print('Adding successfully !')
                else:
                    print('Client disconnected')
            except:
                client.close()
                return False
ThreadedServer('localhost', 1995).listen()


