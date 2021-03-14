from .common import *

class PropertyPanel(wx.Panel):
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