from .common import *

class BatchExcelPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self._init_UI()

    def _init_UI(self):

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.SetBackgroundColour(CON_COLOR_MAIN)

        self.panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(topsizer)
        topsizer.SetSizeHints(self.panel)
        sizer.Add(self.panel, 1, wx.EXPAND)
