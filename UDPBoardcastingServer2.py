import socket
import time
import datetime
import random
import pickle

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)

while 1:

    a = random.Random()

    # vehtype = 1 + a.randint(1, 3)
    # speed = 62 + a.randint(-10, 10)
    # acc = 939 + a.randint(-50, 50)
    # lane = 1 + a.randint(0, 1)
    # weight = (790 + a.randint(-50, 50), 770 + a.randint(-50, 50))
    # space = 2564 + a.randint(-200, 200)
    # dt = datetime.datetime.today().strftime('%Y.%m.%d %H:%M:%S')

    # data = [vehtype, speed, acc, lane, weight, space, dt]
    # data = pickle.dumps(data)
    data = str(a.randint(-1, 1))
    print data

    s.sendto(data,('255.255.255.255', 65432))
    time.sleep(0.02)

s.close()