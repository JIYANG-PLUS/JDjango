#!/usr/bin/env python
import wx

from .frames.mainFrame import Main

class App(wx.App):

    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        self.frame = Main()
        self.frame.SetWindowStyle(wx.DEFAULT_FRAME_STYLE | wx.FRAME_TOOL_WINDOW)
        self.frame.Show(True) # frame.Hide() 等价于 frame.Show(False) 
        self.SetTopWindow(self.frame)
        return True

    def OnExit(self):
        # wx.Exit() // 强制关闭窗口（不推荐使用）
        # OnExit无论以何种方式退出，终会被触发
        # 这里可进行资源释放的工作
        return super().OnExit()


def main():
    # app = App()
    app = App(redirect=True) # 输出重定向到框架（调试用）【指定filename将输出到文件】
    app.MainLoop()


if __name__ == "__main__":
    main()