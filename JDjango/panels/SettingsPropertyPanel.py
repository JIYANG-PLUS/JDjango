from .common import *

class SettingsPropertyPanel(wx.Panel):
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

        ### 常用属性（默认值后期读取）
        pgPanel.Append(wxpg.PropertyCategory("1 - 常用配置（功能重整，项目当前不可用）"))
        pgPanel.Append(wxpg.ArrayStringProperty("ALLOWED_HOSTS", value=['*',]))
        pgPanel.Append(wxpg.BoolProperty("DEBUG", value=True))
        pgPanel.Append(wxpg.EnumProperty("LANGUAGE_CODE", "LANGUAGE_CODE",
                ['中文', '英文',],
                [0, 1], 0
        ))
        pgPanel.Append(wxpg.EnumProperty("TIME_ZONE", "TIME_ZONE",
                ['伦敦时区', '上海时区', '美国芝加哥'],
                [0, 1, 2], 0
        ))
        pgPanel.Append(wxpg.BoolProperty("USE_I18N", value=True))
        pgPanel.Append(wxpg.BoolProperty("USE_L10N", value=True))
        pgPanel.Append(wxpg.BoolProperty("USE_TZ", value=True))

        # 适配
        topsizer.Add(pgPanel, 1, wx.EXPAND | wx.ALL, 5)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)