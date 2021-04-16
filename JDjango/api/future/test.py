import wx
import wx.aui as aui


text = """\
Hello!

Welcome to this little demo of draggable tabs using the aui module.

To try it out, drag a tab from the top of the window all the way to the bottom.  After releasing the mouse, the tab will dock at the hinted position.  Then try it again with the remaining tabs in various other positions.  Finally, try dragging a tab to an existing tab ctrl.  You'll soon see that very complex tab layouts may be achieved.
"""

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self.nb = aui.AuiNotebook(self)
        page = wx.TextCtrl(self.nb, -1, text, style=wx.TE_MULTILINE)
        self.nb.AddPage(page, "Welcome")

        for num in range(1, 5):
            page = wx.TextCtrl(self.nb, -1, "This is page %d" % num ,
                               style=wx.TE_MULTILINE)
            self.nb.AddPage(page, "Tab Number %d" % num)
        sizer.Add(self.nb, 1, wx.EXPAND|wx.ALL, 5)
        
        wx.CallAfter(self.nb.SendSizeEvent)

class MainFrameGUI(wx.Frame):

    def __init__(self, parent = None):
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = "PyShell", pos = wx.DefaultPosition, size = wx.Size(960, 540), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
        self.panel = TestPanel(self)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(panelSizer)

class App(wx.App):

    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        self.frame = MainFrameGUI()
        self.frame.SetWindowStyle(wx.DEFAULT_FRAME_STYLE) #  | wx.FRAME_TOOL_WINDOW
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

    def OnExit(self):
        return super().OnExit()
     
if __name__ == '__main__':
    app = App(redirect=False) # 【指定filename将输出到文件】
    app.MainLoop()
