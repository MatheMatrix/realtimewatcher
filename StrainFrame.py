# -*- coding: utf-8 -*-

import wx
import random


class StrainFrame(wx.Frame):

    """docstring for StrainFrame
    """

    def __init__(self, parent, id, stat):
        """

        :param parent:
        :param id:
        """
        wx.Frame.__init__(self, parent, id, u'光栅光纤实时监控', size=(1083, 720))
        self.ChangeStat = stat
        panel = wx.Panel(self, -1, style=wx.TAB_TRAVERSAL
                         | wx.CLIP_CHILDREN
                         | wx.FULL_REPAINT_ON_RESIZE
                         )

        chs = {
            'ch12': [45, 46, 47, 48], 'ch13': [49, 50, 51, 52], 'ch10': [37, 38, 39, 40],
            'ch11': [41, 42, 43, 44], 'ch16': [59, 60], 'ch14': [53, 54, 55, 56], 'ch15': [57, 58],
            'ch1': [1, 2, 3, 4, 5, 6], 'ch2': [7, 8, 9, 10, 11, 12], 'ch3': [13, 14, 15, 16],
            'ch4': [17, 18, 19, 20], 'ch5': [21, 22, 23, 24], 'ch6': [25, 26, 27, 28], 'ch7': [29, 30],
            'ch8': [31, 32], 'ch9': [33, 34, 35, 36]}
        gbs = wx.GridBagSizer(10, 10)
        self.texts = []
        title = wx.StaticText(panel, -1, u'光栅光纤实时监控', (
            0, 0), (-1, -1), wx.ALIGN_CENTER)

        self.timer = wx.Timer()
        self.timer.Bind(wx.EVT_TIMER, self.Change)
        self.timer.Start(1000)

        self.DisplayTitle(title, gbs)
        self.Display(chs, gbs, panel)

        box = wx.BoxSizer()
        box.Add(
            gbs, 0, wx.ALL, 10)
        panel.SetSizerAndFit(box)
        self.SetClientSize((panel.GetSize()[0] + 10, panel.GetSize()[1] + 10))

    def DisplayTitle(self, title, gbs):
        """Display Title
        """

        title.SetForegroundColour('#0969A2')
        font = wx.Font(22, wx.SWISS, wx.NORMAL, wx.BOLD,
                       underline=False, faceName='Microsoft YaHei')
        title.SetFont(font)

        gbs.Add(title,
                (0, 0), (1, 17), wx.ALIGN_CENTER | wx.ALL, 5)

    def Display(self, chs, gbs, panel):
        """Display the table
        """

        for i in range(1, 9):
            gbs.Add(wx.StaticText(panel, -1, u'通道{0}'.format(i)),
                    (1, 2 * i - 1), flag=wx.ALIGN_CENTER)
            for j in chs['ch' + str(i)]:
                gbs.Add(wx.StaticText(panel, -1, u'传感器{0}'.format(j)),
                        (chs['ch' + str(i)].index(j) + 2, (i - 1) * 2),
                        flag=wx.ALIGN_CENTER)
                self.texts.append(
                    wx.TextCtrl(panel, -1, "0.000", size=(50, -1)))
                gbs.Add(self.texts[-1], (chs['ch' + str(i)]
                        .index(j) + 2, 2 * i - 1), flag=wx.ALIGN_CENTER)

        for i in range(9, 17):
            gbs.Add(wx.StaticText(panel, -1, u'通道{0}'.format(i)),
                    (1 + 8, 2 * (i - 8) - 1), flag=wx.ALIGN_CENTER)
            for j in chs['ch' + str(i)]:
                gbs.Add(wx.StaticText(panel, -1, u'传感器{0}'.format(j)),
                        (chs['ch' + str(i)].index(j) + 2 + 8, (i - 8 - 1) * 2),
                        flag=wx.ALIGN_CENTER)
                self.texts.append(
                    wx.TextCtrl(panel, -1, "0.000", size=(50, -1)))
                gbs.Add(self.texts[-1], (chs['ch' + str(i)].index(j)
                        + 2 + 8, 2 * (i - 8) - 1), flag=wx.ALIGN_CENTER)

    def Change(self, event):
        a = random.random() * 10
        for text in self.texts:
            text.SetValue(str(a)[:7])

    def __del__(self):
        self.ChangeStat('Strain')
        self.timer.Stop()
