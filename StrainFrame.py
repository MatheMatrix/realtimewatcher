# -*- coding: utf-8 -*- 

import wx
import wx.grid


class StrainFrame(wx.Frame):
    """docstring for StrainFrame
    """

    def __init__(self, parent, id):  # , stat):
        """

        :param parent:
        :param id:
        """
        wx.Frame.__init__(self, parent, id, u'光栅光纤实时监控', size=(1083, 720))
        # , style = wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        # self.ChangeStat = stat
        # grid = wx.grid.Grid(self)
        # grid.CreateGrid(50, 50)
        p = wx.Panel(self, -1, style=wx.TAB_TRAVERSAL
                                     | wx.CLIP_CHILDREN
                                     | wx.FULL_REPAINT_ON_RESIZE
        )

        chs = {'ch12': [45, 46, 47, 48], 'ch13': [49, 50, 51, 52], 'ch10': [37, 38, 39, 40],
               'ch11': [41, 42, 43, 44], 'ch16': [59, 60], 'ch14': [53, 54, 55, 56], 'ch15': [57, 58],
               'ch1': [1, 2, 3, 4, 5, 6], 'ch2': [7, 8, 9, 10, 11, 12], 'ch3': [13, 14, 15, 16],
               'ch4': [17, 18, 19, 20], 'ch5': [21, 22, 23, 24], 'ch6': [25, 26, 27, 28], 'ch7': [29, 30],
               'ch8': [31, 32], 'ch9': [33, 34, 35, 36]}

        gbs = wx.GridBagSizer(5, 5)
        gbs.Add(wx.StaticText(p, -1, u'光栅光纤实时监控'),
                (0, 5), (1, 10), wx.ALIGN_CENTER | wx.ALL, 5)
        gbs.Add(wx.StaticText(p, -1, u'通道1'), (1, 1), flag=wx.ALIGN_CENTER)
        gbs.Add(wx.StaticText(p, -1, u'传感器1'), (2, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        gbs.Add(wx.TextCtrl(p, -1, "1.37528", size=(50, -1)), (2, 1))
        gbs.Add(wx.StaticText(p, -1, u'传感器2'), (3, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        gbs.Add(wx.TextCtrl(p, -1, "1.37528", size=(50, -1)), (3, 1))
        gbs.Add(wx.StaticText(p, -1, u'通道2'), (1, 3), flag=wx.ALIGN_CENTER)
        gbs.Add(wx.StaticText(p, -1, u'传感器3'), (2, 2), flag=wx.ALIGN_CENTER_VERTICAL)
        gbs.Add(wx.TextCtrl(p, -1, "1.37528", size=(50, -1)), (2, 3))
        gbs.Add(wx.StaticText(p, -1, u'传感器4'), (3, 2), flag=wx.ALIGN_CENTER_VERTICAL)
        gbs.Add(wx.TextCtrl(p, -1, "1.37528", size=(50, -1)), (3, 3))
        box = wx.BoxSizer()
        box.Add(gbs, 0, wx.ALL, 10)
        p.SetSizerAndFit(box)
        # self.SetClientSize(p.GetSize())

    def __del__(self):
        pass
        # self.ChangeStat('Strain')


if __name__ == '__main__':
    app = wx.PySimpleApp()
    StrainFrame(None, -1).Show()
    app.MainLoop()