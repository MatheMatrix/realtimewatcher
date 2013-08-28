# -*- coding: utf-8 -*-

import wx
import matplotlib

matplotlib.use('WXAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas
import numpy as np
import pickle
import threading
import socket


class CableFrame(wx.Frame):

    """docstring for CableFrame
    """

    def __init__(self, parent, id, stat):
        wx.Frame.__init__(self, parent, id, u'索力实时监控', size=(1083, 720),
                          style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.ChangeStat = stat

        self.panel = self.Display()

    def Display(self):

        panel = wx.Panel(
            self, -1, pos=(0, 0), style=wx.NO_FULL_REPAINT_ON_RESIZE)
        fig = Figure((9.0, 6.92), dpi=100)
        rect = fig.patch
        rect.set_facecolor('#f0f0f0')

        self.DisplayCheckBoxes(panel)
        self.plot = CablePlot(panel, fig)
        self.DisplayButton(panel)

    def DisplayCheckBoxes(self, panel):

        """Display CheckBoxes for channels

        panel is the panel which provided by wx to display on
        Display 24 checkboxes to choose
        """

        self.checkboxes = []

        pos = [(910, 60), (990, 60), (910, 90), (990, 90),
               (910, 120), (990, 120), (910, 150), (990, 150),
               (910, 180), (990, 180), (910, 210), (990, 210),
               (910, 240), (990, 240), (910, 270), (990, 270),
               (910, 300), (990, 300), (910, 330), (990, 330),
               (910, 360), (990, 360), (910, 390), (990, 390)]

        # for i in range(24):
        #     if i % 2 == 0:
        #         pos.append((910, 60 + i/2*30))
        #     else:
        #         pos.append((990, 60 + (i-1)/2*30))

        for i in range(24):
            self.checkboxes.append(
                wx.CheckBox(panel, -1, u'第' + str(i + 1) + u'通道', pos[i]))

        for i in range(8):
            self.checkboxes[i].SetValue(True)

    def DisplayButton(self, panel):

        """Display 'Draw' button to draw bar graph
        """

        bmp = wx.Image(
            'GenerateCablePlot_Resize_1.png',
            wx.BITMAP_TYPE_PNG).ConvertToBitmap()

        butStart = wx.Button(panel, -1, u'生成图像', (914, 420))
        butStart.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL,
                                 wx.BOLD, underline=False, faceName='Microsoft YaHei'))
        butStart.SetBitmap(bmp, wx.LEFT)
        butStart.SetBitmapMargins((2, 2))
        butStart.SetInitialSize()

        butStart.Bind(wx.EVT_BUTTON, self.OnStart)

    def OnStart(self, event):

        """Find checked in checkbox and draw bat graph

        :param event:
        """

        stat = []

        for i in range(24):
            if self.checkboxes[i].GetValue():
                stat.append(i)

        self.plot.ChChoose(stat)

    def __del__(self):
        self.ChangeStat('Cable')
        self.plot.redrawtimer.Stop()


class CablePlot():

    """Paint cable which contain Force and Temperature
    """

    def __init__(self, panel, fig):

        """init the class

        :param panel: panel to plot on
        :param fig: fig to make subplot
        """

        self.fig = fig
        self.axes = []

        self.cabledata = CableReceiveThread()
        self.cabledata.start()

        self.DisplayBar(panel)
        self.stat = [0, 1, 2, 3, 4, 5, 6, 7]

        self.redrawtimer = wx.Timer()
        self.redrawtimer.Bind(wx.EVT_TIMER, self.ReDraw)
        self.redrawtimer.Start(2000)
        # self.timer = self.fig.canvas.new_timer(interval=1000)
        # self.timer.add_callback(self.ReDraw, 0)
        # self.timer.start()

    def DisplayBar(self, panel):
        self.InitPlot(panel, 0)
        self.InitPlot(panel, 1)

    def InitPlot(self, panel, sub):

        """Init self.axes and self.canvas

        :param panel: panel to plot on
        :param sub: 0 for Force, 1 for Temperature
        """

        self.axes.append(self.fig.add_subplot(211 + sub))
        self.axes[sub].set_ylabel(u'索力' if sub == 0 else u'温度', fontproperties='Microsoft YaHei')

        self.canvas = FigCanvas(panel, -1, self.fig)

    def DrawPlot(self, sub):

        """Draw Plot

        :param sub: 0 for Force 1 for Temperature
        """

        self.axes[sub].clear()

        self.axes[sub].bar(
            left=np.arange(len(self.data[sub])),
            height=self.data[sub],
            width=0.4 if len(self.data[sub]) <= 12 else 0.6,
            align='center',
            alpha=0.44,
            color='r' if sub == 1 else 'b',
            picker=5
        )

        self.axes[sub].set_xticks(
            np.arange(len(self.data[sub]))
        )
        self.axes[sub].set_xticklabels(
            ['ch' + str(i+1) for i in self.stat]
        )
        self.axes[sub].set_ybound(
            lower=min(self.data[sub])*0.7 if sub == 1 else min(self.data[sub])*0.95,
            upper=max(self.data[sub])*1.1 if sub == 1 else max(self.data[sub])*1.01)

        for i in range(len(self.data[sub])):
            self.axes[sub].text(
                x=i-0.4 if len(self.data[sub]) <= 12 else i-0.6,
                y=self.data[sub][i]*1.003 if sub == 0 else self.data[sub][i]*1.04,
                s='%6.2f' % self.data[sub][i] if len(self.data[sub]) <= 12 else '%6.0f' % self.data[sub][i])

    def ChChoose(self, stat):

        """Get stat of user's channel choose

        :param stat: like [1, 3, 11, ..., 24]
            means ch1, ch3, ... ch24 are open
            others close

        :return self.data's structure:
            [
                [872.36, 123.0, ..., 982.1]  # Force
                [31.2, 30.6, ..., 27.2]  # Temperature
            ]
        """

        self.stat = stat

        self.ReDraw(0)

    def ReDraw(self, event):

        """ReDraw Bar Chart
        """

        self.data = [[], []]

        for i in self.stat:
            self.data[0].append(
                self.cabledata.data['ch' + str(i)][0])
            self.data[1].append(
                self.cabledata.data['ch' + str(i)][1])

        self.DrawPlot(0)
        self.DrawPlot(1)

        self.canvas.draw()


class CableReceiveThread(threading.Thread):

    """Receive cable data

    self.data is a data buff which contains 48 at most
    assume data(dict)'s structure:
    {
        'ch0':  [ch1Force,  ch1Temp],
        'ch1':  [ch2Force,  ch2Temp],
        ...
        'ch23': [ch24Force, ch24Temp]
    }
    """

    def __init__(self):
        threading.Thread.__init__(self)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.IP = socket.gethostbyname(socket.gethostname())
        self.s.bind((self.IP, 65434))

        self.daemon = True

        self.data = {}

        for i in range(24):
            self.data['ch' + str(i)] = [0, 0]

    def run(self):

        """Get cable data from 65434 port

        Assume the structure of data which receive from LAN:
        [chNum, Force, Temp]
        """

        while True:
            d, a = self.s.recvfrom(1500)
            real = pickle.loads(d)
            # print real
            self.data = real
            # self.data['ch' + str(real[0])] = [real[1], real[2]]


# if __name__ == '__main__':
#     app = wx.PySimpleApp()
#     CableFrame(None, -1).Show()
#     app.MainLoop()
