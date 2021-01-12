#!/usr/bin/env python
import wx

from .frames.mainFrame import Main
from .frames.sqliteFrame import SQLiteManageFrame

class App(wx.App):

    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        self.frame = Main()
        self.frame.SetWindowStyle(wx.DEFAULT_FRAME_STYLE) #  | wx.FRAME_TOOL_WINDOW
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

    def OnExit(self):
        # wx.Exit() # 强制关闭窗口（不推荐使用）
        return super().OnExit()

def main():
    app = App(redirect=False) # 【指定filename将输出到文件】
    app.MainLoop()

class SQLiteApp(wx.App):

    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        self.frame = SQLiteManageFrame(None)
        self.frame.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

    def OnExit(self):
        return super().OnExit()

def startSQLiteApp():
    app = SQLiteApp(redirect=False)
    app.MainLoop()
