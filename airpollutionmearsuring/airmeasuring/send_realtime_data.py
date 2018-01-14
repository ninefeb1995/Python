import http.client
from random import uniform
import time


while True:
    co_a = uniform(2.5, 5)
    co_b = uniform(2.5, 5)
    co_c = uniform(2.5, 5)
    try:
        nodea = http.client.HTTPConnection('192.168.1.112', 8001).request('GET', '/dashboard/rawdata/?co=%s&node=nodea' % co_a)
        nodeb = http.client.HTTPConnection('192.168.1.112', 8001).request('GET', '/dashboard/rawdata/?co=%s&node=nodeb' % co_b)
        nodec = http.client.HTTPConnection('192.168.1.112', 8001).request('GET', '/dashboard/rawdata/?co=%s&node=nodec' % co_c)
    except:
        print('There is an error!')
        break
    time.sleep(5)
