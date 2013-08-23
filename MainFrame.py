#coding: utf-8

import wx
import AccDlg
import VehFrame
import CableFrame
import StrainFrame
import ObliFrame

class MainFrame(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, u'潮白河大桥实时监控系统', size = (1083, 720), style = wx.CAPTION)#wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.CLOSE_BOX))

        panel = self.Display()

    def AddButton(self, bid, pngs, label, name, panel):
        '''Add button in main page
        '''

        postions = [(40, 350), (381, 350), (722, 350), (40, 492), (381, 492), (722, 492)]
        tipstrings = [u'点击进入加速度实时监控', u'点击进入车速车载实时监控', u'点击进入索力实时监控', u'点击进入光栅光纤实时监控', u'点击进入倾角仪实时监控', u'点击退出']

        bmp = wx.Image(pngs[name], wx.BITMAP_TYPE_PNG).ConvertToBitmap()

        b = wx.Button(panel, -1, label, postions[bid - 1])
        b.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD, underline = False, faceName = 'Microsoft YaHei'))
        b.SetToolTipString(tipstrings[bid - 1])
        b.SetBitmap(bmp, wx.LEFT)
        b.SetBitmapMargins((2,2))
        b.SetInitialSize()

        return b

    def Display(self):
        '''Display elements on the frame
        '''
        
        panel = wx.Panel(self, -1, pos = (0, 0), style = wx.NO_FULL_REPAINT_ON_RESIZE)  # , size = (1083, 720)
        # panel.SetBackgroundColour('white')
        
        title = self.DisplayTitle(panel)
        subtitle = self.DisplaySubtitle(panel)
        design = wx.StaticText(panel, -1, u'Design for Miyun Chaobaihe Bridge', (840, 650), (-1, -1), wx.ALIGN_RIGHT)

        self.buttons = self.DisplayButtons(panel)

        return panel
    
    def DisplayTitle(self, panel):
        '''Display Title
        '''
        
        title = wx.StaticText(panel, -1, u'欢迎使用潮白河大桥实时监控系统', (255, 100), (-1, -1), wx.ALIGN_CENTER)
        title.SetForegroundColour('#0969A2')
        font = wx.Font(25, wx.SWISS, wx.NORMAL, wx.BOLD, underline = False, faceName = 'Microsoft YaHei')
        title.SetFont(font)
        
        return title
    
    def DisplaySubtitle(self, panel):
        '''DisplaySubTitle
        '''
        
        subtitle = wx.StaticText(panel, -1, u'北京工业大学防灾减灾研究所', (700, 200), (-1, -1), wx.ALIGN_RIGHT)
        subtitle.SetForegroundColour('#64A8D1')
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD, underline = False, faceName = 'Microsoft YaHei')
        subtitle.SetFont(font)
        
        return subtitle

    def DisplayButtons(self, panel):
        '''Display buttons
        '''

        pngs = {'Acc': 'Acc_Resize_1.png', 'Exit': 'Exit_Resize_1.png', 'Cable': 'Cable3_Resize_1.png', 'Obli': 'Obli_Resize_1.png', 'Strain': 'Strain_Resize_1.png', 'Veh': 'VenSpeedAndWeight_Resize_1.png'}
        labels = [u'加速度\n实时监控', u'车速车载\n实时监控', u'索力\n实时监控', u'光栅光纤\n实时监控', u'倾角仪\n实时监控', u'退出系统']
        names = ['Acc', 'Veh', 'Cable', 'Strain', 'Obli', 'Exit']
        buttons = []

        for i in range(1, 6 + 1):
            buttons.append(self.AddButton(i, pngs, labels[i - 1], names[i - 1], panel))

        self.framestats = {'Acc': 0, 'Strain': 0, 'Veh': 0, 'Obli': 0, 'Cable': 0}

        self.BindButtons(buttons)
        self.Bind(wx.EVT_BUTTON, self.Exit, buttons[-1])

    def Exit(self, event):
        '''Exit
        '''

        dlg = wx.MessageDialog(None, u'确定退出么？（退出前请关闭所有模块）', u'确认', wx.YES_NO | wx.ICON_EXCLAMATION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_YES:
            self.Close(True)
            wx.Exit()
        else:
            pass

    def BuildAccFrame(self, event):
        if self.framestats['Acc'] == 0:
            accdlg = AccDlg.AccDlg(parent = None, id = -1, stat = self.FrameStats)
            accdlg.Show()
            self.framestats['Acc'] = 1
        else:
            self.DontRepeat()

    def BuildVehFrame(self, event):
        if self.framestats['Veh'] == 0:
            vehframe = VehFrame.VehFrame(parent = None, id = -1, stat = self.FrameStats)
            vehframe.Show()
        else:
            self.DontRepeat()

    def BuildCableFrame(self, event):
        if self.framestats['Cable'] == 0:
            cableframe = CableFrame.CableFrame(parent = None, id = -1, stat = self.FrameStats)
            cableframe.Show()
            self.framestats['Cable'] = 1
        else:
            self.DontRepeat()

    def BuildStrainFrame(self, event):
        if self.framestats['Strain'] == 0:
            strainframe = StrainFrame.StrainFrame(parent = None, id = -1, stat = self.FrameStats)
            strainframe.Show()
            self.framestats['Strain'] = 1
        else:
            self.DontRepeat()

    def BuildObliFrame(self, event):
        if self.framestats['Obli'] == 0:
            obliframe = ObliFrame.ObliFrame(parent = None, id = -1, stat = self.FrameStats)
            obliframe.Show()
            self.framestats['Obli'] = 1
        else:
            self.DontRepeat()

    def FrameStats(self, name):
        '''Change Frame Stats
        '''

        if self.framestats[name] == 0:
            self.framestats[name] = 1
        else:
            self.framestats[name] = 0

    def BindButtons(self, buttons):
        '''Binf buttons with events
        '''

        events = [self.BuildAccFrame, self.BuildVehFrame, self.BuildCableFrame, self.BuildStrainFrame, self.BuildObliFrame]
        for i in range(len(buttons) - 1):
            self.Bind(wx.EVT_BUTTON, events[i], buttons[i])


    def DontRepeat(self):
        '''Show Dont't DontRepeat dlg
        '''

        dlg = wx.MessageDialog(None, u'请不要重复打开窗口', u'警告', wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()