#coding: utf-8
#!/usr/bin/env python

import wx
import MainFrame

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MainFrame.MainFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()