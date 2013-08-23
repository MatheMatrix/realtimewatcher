#coding: utf-8

import socket
import time
import random
import pickle

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)

while 1:

    data = {}

    for i in range(24):
        a = random.random()
        data['ch'+str(i)] = [6000 + a * 10, 30 + a]
    print data
    data = pickle.dumps(data)


    s.sendto(str(data),('255.255.255.255', 65434))
    time.sleep(3)

s.close()
