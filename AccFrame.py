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

        ac1 = AccCurve(panel, 1)


    def __del__(self):
        self.ChangeStat('Acc')


class AccCurve():
    '''Paint a matplot curve and a combobox
    '''

    chtypes = {1: ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11'], 2: ['ch12', 'ch13', 'ch14', 'ch15', 'ch16', 'ch17', 'ch18', 'ch19', 'ch20', 'ch21', 'ch22'], 3: ['ch22', 'ch23', 'ch24', 'ch25', 'ch26', 'ch27', 'ch28', 'ch29', 'ch30', 'ch31', 'ch32', 33], 4: ['ch32', 'ch33', 'ch34', 'ch35', 'ch36', 'ch37', 'ch38', 'ch39', 'ch40', 'ch41', 'ch42', 43, 44]}

    def __init__(self, panel, posid):
        '''init
        '''

        self.DisplayTitle(panel)
        self.DisplayCombox(panel, posid)
        self.DisplayCurve(panel, posid)

    def DisplayTitle(self, panel):
        '''Display Title
        '''

        title = wx.StaticText(panel, -1, u'加速度实时监控系统', (433, 50), (-1, -1), wx.ALIGN_CENTER)
        title.SetForegroundColour('#0969A2')
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD, underline = False, faceName = 'Microsoft YaHei')
        title.SetFont(font)

        print title.GetBestSize()

    def DisplayCombox(self, panel, posid):
        '''Display combobox
        '''

        chselect = wx.StaticText(panel, -1, u'请选择一个通道', (15, 120), (-1, -1), wx.ALIGN_CENTER)
        chselect.SetForegroundColour('#006D4C')
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, underline = False, faceName = 'Microsoft YaHei')
        chselect.SetFont(font)

        cb = wx.ComboBox(panel, -1, self.chtypes[posid][0], (15, 150), 
                         (80, -1), self.chtypes[posid],
                         wx.CB_DROPDOWN)

    def DisplayCurve(self, panel, posid):
        pass

