# -*- coding: utf-8 -*- 
import wx

class ObliFrame(wx.Frame):

    """docstring for ObliFrame
    """

    def __init__(self, parent, id, stat):
        wx.Frame.__init__(self, parent, id, u'倾角仪实时监控', size = (1083, 720), style = wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.ChangeStat = stat

    def __del__(self):
        self.ChangeStat('Oblie')