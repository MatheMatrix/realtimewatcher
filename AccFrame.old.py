# -*- coding: utf-8 -*- 

import wx

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
import numpy as np
import pylab
import random

class AccFrame(wx.Frame):
    '''docstring for AccFrame
    '''

    def __init__(self, parent, id, stat):
        '''Build Acc Frame
        '''

        wx.Frame.__init__(self, parent, id, u'加速度实时监控', size = (1083, 720), style = wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.ChangeStat = stat

        self.panel = self.Display()

    def Display(self):
        '''Display all elements
        '''

        panel = wx.Panel(self, -1, pos = (0, 0), style = wx.NO_FULL_REPAINT_ON_RESIZE)
        fig = Figure((9.0, 6.92), dpi = 100)
        rect = fig.patch
        rect.set_facecolor('#f0f0f0')

        self.accplots = []
        for i in range(4):
            self.accplots.append(AccPlot(panel, i + 1, fig))

        # self.DisplayTitle(panel)

    def DisplayTitle(self, panel):
        '''Display Title
        '''

        title = wx.StaticText(panel, -1, u'加速度实时监控系统', (433, 50), (-1, -1), wx.ALIGN_CENTER)
        title.SetForegroundColour('#0969A2')
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD, underline = False, faceName = 'Microsoft YaHei')
        title.SetFont(font)

    def __del__(self):
        self.ChangeStat('Acc')
        for accplot in self.accplots:
            accplot.redraw_timer.Stop()


class AccPlot():
    '''Paint a matplot curve and a combobox
    '''

    chtypes = {1: ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11'], 2: ['ch12', 'ch13', 'ch14', 'ch15', 'ch16', 'ch17', 'ch18', 'ch19', 'ch20', 'ch21', 'ch22'], 3: ['ch22', 'ch23', 'ch24', 'ch25', 'ch26', 'ch27', 'ch28', 'ch29', 'ch30', 'ch31', 'ch32', 'ch33'], 4: ['ch32', 'ch33', 'ch34', 'ch35', 'ch36', 'ch37', 'ch38', 'ch39', 'ch40', 'ch41', 'ch42', 'ch43', 'ch44']}

    def __init__(self, panel, posid, fig):
        '''init
        '''

        self.fig = fig

        self.datagen = DataGen()
        self.data = [self.datagen.next()]

        self.DisplayCombobox(panel, posid)
        self.DisplayCurve(panel, posid)

        self.redraw_timer = wx.Timer()
        self.redraw_timer.Bind(wx.EVT_TIMER, self.on_redraw_timer)
        self.redraw_timer.Start(100)

    def DisplayCombobox(self, panel, posid):
        '''Display combobox
        '''

        chselect = wx.StaticText(panel, -1, u'请选择一个通道', (955 , 70 + (posid - 1) * 140), (-1, -1), wx.ALIGN_CENTER)
        chselect.SetForegroundColour('#006D4C')
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, underline = False, faceName = 'Microsoft YaHei')
        chselect.SetFont(font)

        cb = wx.ComboBox(panel, -1, self.chtypes[posid][0], (957, 90 + (posid - 1) * 140), 
                         (80, -1), self.chtypes[posid],
                         wx.CB_DROPDOWN)

        cb.Bind(wx.EVT_COMBOBOX, self.EvtComboBox)

    def EvtComboBox(self, evt):
        '''Get event when user change the comboxbox's value
        '''

        cb = evt.GetEventObject()
        # help(cb)
        # data = cb.GetClientData(evt.GetSelection())
        # data = cb.GetCurrentSelection()
        data = cb.GetStringSelection()
        print data[2:]

    def DisplayCurve(self, panel, posid):
        self.initplot(panel, posid)
        self.canvas = FigCanvas(panel, -1, self.fig)

    def initplot(self, panel, posid):
        '''Init plot environment
        '''

        # self.fig = Figure((9.0, 6.92), dpi = 100)
        # rect = self.fig.patch
        # # rect.set_facecolor('#f0f0f0')

        self.axes = self.fig.add_subplot(411 + posid -1)
        self.axes.set_position([0.03, 0.75 - (posid - 1) * (0.17 + 0.04 ), 0.95, 0.17])
        self.axes.set_axis_bgcolor('white')

        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)

        # plot the data as a line series, and save the reference 
        # to the plotted line series
        self.plot_data = self.axes.plot(
            self.data, 
            linewidth=1,
            color=(0, 0, 0),
            )[0]

    def drawplot(self):
        '''Draw plot
        '''

        xmax = len(self.data) if len(self.data) > 100 else 100
        xmin = xmax - 100
        ymin = round(min(self.data), 0) - 1
        ymax = round(max(self.data), 0) + 1

        self.axes.set_xbound(lower=xmin, upper=xmax)
        self.axes.set_ybound(lower=ymin, upper=ymax)

        # self.axes.grid(True, color='gray')

        # pylab.setp(self.axes.get_xticklabels(),  visible = True)
        
        self.plot_data.set_xdata(np.arange(len(self.data)))
        self.plot_data.set_ydata(np.array(self.data))
        
        self.canvas.draw()

    def on_redraw_timer(self, event):
        # if paused do not add data, but still redraw the plot
        # (to respond to scale modifications, grid change, etc.)
        #
        self.data.append(self.datagen.next())
        
        self.drawplot()


class DataGen(object):
    """ A silly class that generates pseudo-random data for
        display in the plot.
    """
    def __init__(self, init=50):
        self.data = self.init = init

    def next(self):
        self._recalc_data()
        return self.data

    def _recalc_data(self):
        # delta = random.uniform(-0.5, 0.5)
        # r = random.random()

        # if r > 0.9:
        #     self.data += delta * 15
        # elif r > 0.8: 
        #     # attraction to the initial value
        #     delta += (0.5 if self.init > self.data else -0.5)
        #     self.data += delta
        # else:
        #     self.data += delta
        self.data = random.randint(10, 90)