# -*- coding: utf-8 -*-

import datetime
import socket
import pickle
import threading

class VehReceiveThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.IP=socket.gethostbyname(socket.gethostname())
        # self.IP = '192.168.1.12'
        self.s.bind((self.IP, 65432))

        self.daemon = True

        self.data = []

    def run(self):
        while True:
            d, a = self.s.recvfrom(75)
            d = pickle.loads(d)
            d[6] = datetime.datetime.strptime(d[6], '%Y.%m.%d %H:%M:%S')
            self.data.append(d)