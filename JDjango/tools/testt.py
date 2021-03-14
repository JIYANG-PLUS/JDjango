import wx
import wx.propgrid as wxpg

class TestPanel(wx.Panel):
    def __init__( self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)

        self.pgPanel = pgPanel = wxpg.PropertyGridManager(
            panel,
            style = wxpg.PG_SPLITTER_AUTO_CENTER
                | wxpg.PG_AUTO_SORT
                | wxpg.PG_TOOLBAR
        )
        pgPanel.ExtraStyle |= wxpg.PG_EX_HELP_AS_TOOLTIPS

        pgPanel.AddPage( "Page 1 - Testing All" )

        topsizer.Add(pgPanel, 1, wx.EXPAND | wx.ALL, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)


class MainFrameGUI(wx.Frame):

    def __init__(self, parent = None):
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = "testt", pos = wx.DefaultPosition, size = wx.Size(960, 540), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
        panel = TestPanel(self)

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