import socket
import threading
import logging
from dashboard.models import RawData
from manage_devices.models import Node
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import datetime


logger = logging.getLogger(__name__)


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        print("Server is listening on (%s, %s) !" % (self.host, self.port))
        logger.info("Server is listening on (%s, %s) !" % (self.host, self.port))
        self.sock.listen(10)
        self.sock.settimeout(180)
        while True:
            client, address = self.sock.accept()
            client.settimeout(10)
            threading.Thread(target=self.listen_to_client, args=(client, address)).start()

    def listen_to_client(self, client, address):
        print("Client with ip %s is connected...\n\n" % str(address))
        logger.info("Client with ip %s is connected...\n\n" % str(address))
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # # Set the response to echo back the recieved data
                    print(data)
                    # response = data
                    # client.send(response)
                    # handle data here
                    try:
                        node, co = str(data, "ascii").split('-')
                        node_id = Node.objects.get(node_identification=node)
                        new_data = RawData(co=co,
                                           node=node_id,
                                           node_identification=node_id.node_identification,
                                           measuring_date=datetime.now())
                        new_data.save(force_insert=True)
                    except:
                        logger.exception("Error when adding data to database !\n")
                else:
                    client.close()
            except:
                logger.exception("There is an error !\n")
                client.close()
                return False


class Command(BaseCommand):
    help = 'Starting listening on tcp socket to receive data from nodes'

    def handle(self, *args, **options):
        # ThreadedServer('localhost', 1995).listen()
        ThreadedServer('192.168.1.112', 8001).listen()

