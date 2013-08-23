# -*- coding: utf-8 -*- 
import wx

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
import numpy as np

class CableFrame(wx.Frame):
    '''docstring for CableFrame
    '''
    def __init__(self, parent, id, stat):
        wx.Frame.__init__(self, parent, id, u'索力实时监控', size = (1083, 720), style = wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.ChangeStat = stat

    def __del__(self):
        self.ChangeStat('Cable')