# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import socket
import threading

class AccFrame():

    def __init__(self, chs, stat):

        colors = ['#FF8E00', '#00B25C', '#1921B1', '#0A67A3']

        self.stat = stat

        self.fig = plt.figure("加速度实时监控")
        self.fig.set_frameon(False)

        self.ax1 = self.fig.add_subplot(411, ylim = (-0.1, 0.1))
        self.ax2 = self.fig.add_subplot(412, ylim = (-0.1, 0.1))
        self.ax3 = self.fig.add_subplot(413, ylim = (-0.1, 0.1))
        self.ax4 = self.fig.add_subplot(414, ylim = (-0.1, 0.1))

        self.ax1.get_xaxis().set_visible(False)
        self.ax2.get_xaxis().set_visible(False)
        self.ax3.get_xaxis().set_visible(False)
        self.ax4.get_xaxis().set_visible(False)

        self.line1, = self.ax1.plot([], [], lw=1, color = colors[0])
        self.line2, = self.ax2.plot([], [], lw=1, color = colors[1])
        self.line3, = self.ax3.plot([], [], lw=1, color = colors[2])
        self.line4, = self.ax4.plot([], [], lw=1, color = colors[3])

        data = [0 for i in range(200)]

        global v
        v = AccReceiveThread(data)
        v.start()

        self.ax1.set_title('ch' + str(chs[0]))
        self.ax2.set_title('ch' + str(chs[1]))
        self.ax3.set_title('ch' + str(chs[2]))
        self.ax4.set_title('ch' + str(chs[3]))

        anim1 = animation.FuncAnimation(self.fig, self.animate1, init_func=self.init1,
                                       frames=1, interval=100, blit=True)
        anim2 = animation.FuncAnimation(self.fig, self.animate2, init_func=self.init2,
                                       frames=1, interval=100, blit=True)
        anim3 = animation.FuncAnimation(self.fig, self.animate3, init_func=self.init3,
                                       frames=1, interval=100, blit=True)
        anim4 = animation.FuncAnimation(self.fig, self.animate4, init_func=self.init4,
                                       frames=1, interval=100, blit=True)

        plt.show()

    def init1(self):
        self.line1.set_data([], [])
        return self.line1,

    def animate1(self, i):
        x = np.linspace(0, 1, 200)
        y = v.data
        self.line1.set_data(x, y)
        return self.line1,

    def init2(self):
        self.line2.set_data([], [])
        return self.line2,

    def animate2(self, i):
        x = np.linspace(0, 1, 200)
        y = v.data
        self.line2.set_data(x, y)
        return self.line2,

    def init3(self):
        self.line3.set_data([], [])
        return self.line3,

    def animate3(self, i):
        x = np.linspace(0, 1, 200)
        y = v.data
        self.line3.set_data(x, y)
        return self.line3,

    def init4(self):
        self.line4.set_data([], [])
        return self.line4,

    def animate4(self, i):
        x = np.linspace(0, 1, 200)
        y = v.data
        self.line4.set_data(x, y)
        return self.line4,


class AccReceiveThread(threading.Thread):

    def __init__(self, data):
        threading.Thread.__init__(self)

        self.s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.IP=socket.gethostbyname(socket.gethostname())
        self.s.bind((self.IP, 65431))

        self.daemon = True

        self.data = data

    def run(self):
        while True:
            d, a = self.s.recvfrom(20)
            self.data.append(d)
            if len(self.data) >= 200:
                del self.data[0]