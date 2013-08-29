# -*- coding: utf-8 -*- 
import wx
import wx.lib.layoutf  as layoutf
import random


class ObliFrame(wx.Frame):
    """docstring for ObliFrame
    """

    def __init__(self, parent, id, stat):

        """Init ObliFrame

        :param parent: parent to write on
        :param id: wxPython's id
        :param stat: stat change function
        """

        wx.Frame.__init__(
            self,
            parent,
            id,
            u'倾角仪实时监控',
            size=(1280, 720),
            # style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        )

        self.ChangeStat = stat

        self.SetAutoLayout(True)
        self.SetBackgroundColour('#d4d0c8')

        self.panelA = wx.Window(self, -1, style=wx.SIMPLE_BORDER)
        self.panelA.SetConstraints(
            layoutf.Layoutf('t=t20#1;l=l20#1;w%w96#1;h%h10#1', (self,))
        )

        self.panelB = wx.Window(self, -1, style=wx.SIMPLE_BORDER)
        self.panelB.SetConstraints(
            layoutf.Layoutf('t=t115#1;l=l20#1;w%w50#1;h%h80#1', (self,))
        )

        self.panelC = wx.Window(self, -1, style=wx.SIMPLE_BORDER)
        self.panelC.SetConstraints(
            layoutf.Layoutf('t=t115#1;r=r40#1;w%w42#1;h%h42#1', (self,))
        )

        self.panelD = wx.Window(self, -1, style=wx.SIMPLE_BORDER)
        self.panelD.SetConstraints(
            layoutf.Layoutf('b=b25#1;r=r40#1;w%w42#1;h%h34#1', (self,))
        )

        self.texts = []

        self.timer = wx.Timer()
        self.timer.Bind(wx.EVT_TIMER, self.Change)
        self.timer.Start(1000)

        self.DisplayTitle()
        self.DisplayImage()
        self.DisplayData1()
        self.DisplayData2()


    def DisplayTitle(self):

        """Display Title
        """

        title = wx.StaticText(self.panelA, -1, u'倾角仪实时监控')
        title.SetForegroundColour('#0969A2')
        font = wx.Font(22, wx.SWISS, wx.NORMAL, wx.BOLD,
                       underline=False, faceName='Microsoft YaHei')
        title.SetFont(font)

        title.SetConstraints(layoutf.Layoutf('X=X#1;Y=Y#1;h*;w%w30#1', (self.panelA,)))

    def DisplayImage(self):

        """Display Image
        """

        jpg = wx.Image('BridgeImage_Resize_1.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(self.panelB, -1, jpg)

    def DisplayData1(self):

        """Dsiplay Data on panelC
        """

        gbs = wx.GridBagSizer(18, 10)

        sensers = []

        title = wx.StaticText(self.panelC, -1, u'钢箱梁', (
            0, 0), (-1, -1), wx.ALIGN_CENTER)

        title.SetForegroundColour('#0969A2')
        font = wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD,
                       underline=False, faceName='Microsoft YaHei')
        title.SetFont(font)

        gbs.Add(title,
                (0, 0), (1, 11), wx.ALIGN_CENTER | wx.ALL, 5)

        font = wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD,
                       underline=False, faceName='Microsoft YaHei')

        for i in range(18):
            pos = {0: [(1, 2 * (i % 4)), (1, 2 * (i % 4) + 1)],
                   1: [(2, 2 * (i % 4)), (2, 2 * (i % 4) + 1)],
                   2: [(3, 2 * (i % 4)), (3, 2 * (i % 4) + 1)],
                   3: [(4, 2 * (i % 4)), (4, 2 * (i % 4) + 1)],
                   4: [(5, 2 * (i % 4)), (5, 2 * (i % 4) + 1)]}

            sensers.append(wx.StaticText(self.panelC, -1, u'传感器{0}'.format(i + 1)))
            sensers[-1].SetForegroundColour('#64A8D1')
            sensers[-1].SetFont(font)
            self.texts.append(wx.TextCtrl(self.panelC, -1, "0.000", size=(50, -1)))
            gbs.Add(sensers[-1], pos[i / 4][0], flag=wx.ALIGN_CENTER)
            gbs.Add(self.texts[-1], pos[i / 4][1], flag=wx.ALIGN_CENTER)

        box = wx.BoxSizer()
        box.Add(
            gbs, 0, wx.ALL, 10)
        self.panelC.SetSizerAndFit(box)

    def DisplayData2(self):

        """Display data on panelD
        """

        gbs = wx.GridBagSizer(25, 20)

        sensers = []

        title = wx.StaticText(self.panelD, -1, u'主塔', (
            0, 0), (-1, -1), wx.ALIGN_CENTER)

        title.SetForegroundColour('#0969A2')
        font = wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD,
                       underline=False, faceName='Microsoft YaHei')
        title.SetFont(font)

        gbs.Add(title,
                (0, 0), (1, 8), wx.ALIGN_CENTER | wx.ALL, 5)

        font = wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD,
                       underline=False, faceName='Microsoft YaHei')

        for i in range(6):
            pos = {0: [(1, 2 * (i % 3)), (1, 2 * (i % 3) + 1)],
                   1: [(2, 2 * (i % 3)), (2, 2 * (i % 3) + 1)]}

            sensers.append(wx.StaticText(self.panelD, -1, u'传感器{0}'.format(i + 1 + 18)))
            sensers[-1].SetForegroundColour('#64A8D1')
            sensers[-1].SetFont(font)
            self.texts.append(wx.TextCtrl(self.panelD, -1, "0.000", size=(70, -1)))
            gbs.Add(sensers[-1], pos[i / 3][0], flag=wx.ALIGN_CENTER)
            gbs.Add(self.texts[-1], pos[i / 3][1], flag=wx.ALIGN_CENTER)

        box = wx.BoxSizer()
        box.Add(
            gbs, 0, wx.ALL, 10)
        self.panelD.SetSizerAndFit(box)

    def Change(self, event):
        a = random.random() * 10
        for text in self.texts:
            text.SetValue(str(a)[:7])

    def __del__(self):
        self.ChangeStat('Obli')
        self.timer.Stop()


# if __name__ == '__main__':
#     app = wx.PySimpleApp()
#     frame = ObliFrame(parent=None, id=-1)
#     frame.Show()
#     app.MainLoop()