# coding: utf-8

import wx
import AccFrame


class AccDlg(wx.Frame):

    '''choose chs to display
    '''
    def __init__(self, parent, id, stat):
        wx.Frame.__init__(self, parent, id, u'加速度通道选择', size=(
            500, 280), style = wx.CAPTION | wx.CLOSE_BOX)
        self.panel = wx.Panel(self, -1, pos=(
            0, 0), style = wx.NO_FULL_REPAINT_ON_RESIZE)

        self.DlgStat = stat
        self.framestat = 0

        title = wx.StaticText(self.panel, -1, u'请选择四个通道来显示', (
            100, 20), (-1, -1), wx.ALIGN_CENTER)
        title.SetForegroundColour('#0969A2')
        font = wx.Font(22, wx.SWISS, wx.NORMAL, wx.BOLD,
                       underline=False, faceName='Microsoft YaHei')
        title.SetFont(font)

        self.chs = []
        self.Display()

    def Display(self):
        for i in range(4):
            self.chs.append(ChChosse(self.panel, i + 1))

        self.DisplayButton()

    def DisplayButton(self):

        bmp = wx.Image(
            'GenerateAccPlot_Resize_2.png',
            wx.BITMAP_TYPE_PNG).ConvertToBitmap()

        butStart = wx.Button(self.panel, -1, u'生成图像', (130, 170))
        butStart.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL,
                         wx.BOLD, underline=False, faceName='Microsoft YaHei'))
        butStart.SetBitmap(bmp, wx.LEFT)
        butStart.SetBitmapMargins((2, 2))
        butStart.SetInitialSize()

        butStart.Bind(wx.EVT_BUTTON, self.RunAccFrame)

    def RunAccFrame(self, event):

        names = []
        for ch in self.chs:
            names.append(ch.data)
        print names

        if self.framestat == 0:
            self.FrameStat()
            AccFrame.AccFrame(names, self.FrameStat)
        else:
            AccFrame.AccFrame(names, self.FrameStat)
            # self.DontRepeat()

    def FrameStat(self):
        '''Change Frame Stats
        '''

        print self.framestat

        if self.framestat == 0:
            self.framestat = 1
        else:
            self.framestat = 0

    def DontRepeat(self):
        '''Show Dont't DontRepeat dlg
        '''

        dlg = wx.MessageDialog(
            None, u'请不要重复打开窗口', u'警告', wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def __del__(self):
        self.DlgStat('Acc')


class ChChosse(object):

    '''docstring for ChChosse
    '''

    chtypes = {1: ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7',
                   'ch8', 'ch9', 'ch10', 'ch11'],
               2: ['ch12', 'ch13', 'ch14', 'ch15', 'ch16', 'ch17', 'ch18',
                   'ch19', 'ch20', 'ch21', 'ch22'],
               3: ['ch23', 'ch24', 'ch25', 'ch26',
                   'ch27', 'ch28', 'ch29', 'ch30', 'ch31', 'ch32', 'ch33'],
               4: ['ch34', 'ch35', 'ch36', 'ch37', 'ch38',
                   'ch39', 'ch40', 'ch41', 'ch42', 'ch43', 'ch44']}

    def __init__(self, panel, posid):
        self.DisplayCombobox(panel, posid)
        self.data = int(self.chtypes[posid][0][2:])

    def DisplayCombobox(self, panel, posid):
        '''Display combobox
        '''

        chselect = wx.StaticText(
            panel, -1, u'请选择一个通道', (20 + (posid - 1) * 120, 90), (-1, -1),
            wx.ALIGN_CENTER)
        chselect.SetForegroundColour('#006D4C')
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD,
                       underline=False, faceName='Microsoft YaHei')
        chselect.SetFont(font)

        cb = wx.ComboBox(panel, -1, self.chtypes[posid][0],
                        (22 + (posid - 1) * 120, 110),
                        (80, -1), self.chtypes[posid],
                         wx.CB_DROPDOWN)

        cb.Bind(wx.EVT_COMBOBOX, self.EvtComboBox)

    def EvtComboBox(self, evt):
        '''Get event when user change the comboxbox's value
        '''

        cb = evt.GetEventObject()
        self.data = cb.GetStringSelection()
        print self.data[2:]
        self.data = int(self.data[2:])
