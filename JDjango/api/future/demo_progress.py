import wx

class MainFrameGUI(wx.Frame):

    def __init__(self, parent = None):
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = "PyShell", pos = wx.DefaultPosition, size = wx.Size(960, 540), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
        self.panel = wx.Panel(self)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(panelSizer)
        self.panel.SetBackgroundColour("#456789")

        self.process = None

        prompt = wx.StaticText(self.panel, -1, '命令行：')
        prompt.SetForegroundColour(wx.WHITE)
        self.cmd = wx.TextCtrl(self.panel, -1, 'pip freeze')
        self.btnExec = wx.Button(self.panel, -1, '执行')

        self.out = wx.TextCtrl(self.panel, -1, '', style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2)

        self.inputCmd = wx.TextCtrl(self.panel, -1, '', style=wx.TE_PROCESS_ENTER)
        self.btnSend = wx.Button(self.panel, -1, '向进程发送数据')
        self.btnCloseStream = wx.Button(self.panel, -1, '关闭数据流')

        self.inputCmd.Enable(False)
        self.btnSend.Enable(False)
        self.btnCloseStream.Enable(False)


        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(prompt, 0, wx.EXPAND|wx.ALL, 5)
        box1.Add(self.cmd, 1, wx.EXPAND|wx.ALL, 5)
        box1.Add(self.btnExec, 0)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.Add(self.inputCmd, 1, wx.ALIGN_CENTER)
        box2.Add(self.btnSend, 0, wx.LEFT, 5)
        box2.Add(self.btnCloseStream, 0, wx.LEFT, 5)

        panelSizer.Add(box1, 0, wx.EXPAND|wx.ALL, 10)
        panelSizer.Add(self.out, 1, wx.EXPAND|wx.ALL, 10)
        panelSizer.Add(box2, 0, wx.EXPAND|wx.ALL, 10)


        self.Bind(wx.EVT_IDLE, self.onIdle)
        self.Bind(wx.EVT_END_PROCESS, self.onProcessEnded)

        self.Bind(wx.EVT_BUTTON, self.onExecuteBtn, self.btnExec)
        self.Bind(wx.EVT_BUTTON, self.onSendText, self.btnSend)
        self.Bind(wx.EVT_BUTTON, self.onCloseStream, self.btnCloseStream)
        self.Bind(wx.EVT_TEXT_ENTER, self.onSendText, self.inputCmd)

    def onExecuteBtn(self, e):
        """"""
        cmd = self.cmd.GetValue()

        self.process = wx.Process(self)
        self.process.Redirect()
        pid = wx.Execute(cmd, wx.EXEC_ASYNC, self.process)
        # self.log.write('OnExecuteBtn: "%s" pid: %s\n' % (cmd, pid))

        self.inputCmd.Enable(True)
        self.btnSend.Enable(True)
        self.btnCloseStream.Enable(True)
        self.cmd.Enable(False)
        self.btnExec.Enable(False)
        self.inputCmd.SetFocus()

    def onSendText(self, e):
        """向进程发送数据"""
        text = self.inputCmd.GetValue()
        self.inputCmd.SetValue('')
        # self.log.write('OnSendText: "%s"\n' % text)
        text += '\n'
        self.process.GetOutputStream().write(text.encode('utf-8'))
        self.inputCmd.SetFocus()

    def onCloseStream(self, e):
        """关闭进程的输出数据流"""
        self.process.CloseOutput()

    def onIdle(self, e):
        """实时显示命令执行后的输出内容"""
        if self.process is not None:

            stream = self.process.GetInputStream()

            if stream.CanRead():
                text = stream.read()
                self.out.AppendText(text)

        
    def onProcessEnded(self, e):
        """进程终止时触发操作"""
        stream = self.process.GetInputStream()

        if stream.CanRead():
            text = stream.read()
            self.out.AppendText(text)

        self.process.Destroy()
        self.process = None
        self.inputCmd.Enable(False)
        self.btnSend.Enable(False)
        self.btnCloseStream.Enable(False)
        self.cmd.Enable(True)
        self.btnExec.Enable(True)

    def ShutdownDemo(self):
        """完全终止"""
        if self.process is not None:
            self.process.CloseOutput()
            wx.MilliSleep(250)
            wx.Yield()
            self.process = None

class App(wx.App):

    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        self.frame = MainFrameGUI()
        self.frame.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

    def OnExit(self):
        return super().OnExit()


if __name__ == "__main__":
    app = App(redirect=False)
    app.MainLoop()

