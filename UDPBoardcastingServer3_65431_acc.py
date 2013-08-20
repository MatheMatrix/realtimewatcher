#coding: utf-8

import socket
import time
import datetime
import random
import pickle

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)

while 1:

    a = random.random() / 10

    print a

    s.sendto(str(a),('255.255.255.255', 65431))
    time.sleep(0.05)

s.close()
