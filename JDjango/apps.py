#!/usr/bin/env python
import wx

from .frames.mainFrame import MainFrameFinalGUI
from .frames.sqliteFrame import SQLiteManageFrame
from .frames.digitsRecognitionFrame import DigitRecognitionFrame
from .frames.encryptionFrame import EncryptionFrame

class App(wx.App):

    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        self.frame = MainFrameFinalGUI()
        self.frame.SetWindowStyle(wx.DEFAULT_FRAME_STYLE) #  | wx.FRAME_TOOL_WINDOW
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

    def OnExit(self):
        return super().OnExit()

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

class RecognitionApp(wx.App):

    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        self.frame = DigitRecognitionFrame(None)
        self.frame.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

    def OnExit(self):
        return super().OnExit()

class EncryptionApp(wx.App):

    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        self.frame = EncryptionFrame(None)
        self.frame.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

    def OnExit(self):
        return super().OnExit()

def main():
    """主界面"""
    app = App(redirect=False) # 【指定filename将输出到文件】
    app.MainLoop()

def startSQLiteApp():
    """SQLite3辅助工具界面"""
    app = SQLiteApp(redirect=False)
    app.MainLoop()

def startRecognitionApp():
    """数字图片识别工具"""
    app = RecognitionApp(redirect=False)
    app.MainLoop()

def startEncryptionApp():
    """加解密工具"""
    app = EncryptionApp(redirect=False)
    app.MainLoop()
