from .common import *

class SettingsPropertyPanel(wx.Panel):
    def __init__( self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.index1 = 1

        self._init_UI()

    def _init_UI(self):
        """初始化UI"""
        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)

        self.pgPanel = wxpg.PropertyGridManager(
            panel,
            style = wxpg.PG_SPLITTER_AUTO_CENTER
                | wxpg.PG_AUTO_SORT
                | wxpg.PG_TOOLBAR
        )

        self.pgPanel.ExtraStyle |= wxpg.PG_EX_HELP_AS_TOOLTIPS
        
        self._init_page1()
        
        topsizer.Add(self.pgPanel, 1, wx.EXPAND | wx.ALL, 5)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def _init_page1(self):
        """初始化第一个配置页"""
        self.pgPanel.AddPage("配置")

        self.AppendCategoryAuto("基本")
        self.pgPanel.Append(wxpg.StringProperty("SECRET_KEY", value="423f1sdf3%$#$gdfg#@!33"))
        self.pgPanel.Append(wxpg.ArrayStringProperty("ALLOWED_HOSTS", value=['*',]))
        self.pgPanel.Append(wxpg.BoolProperty("DEBUG", value=True))


        self.AppendCategoryAuto("语言")
        self.pgPanel.Append(wxpg.EnumProperty("LANGUAGE_CODE", "LANGUAGE_CODE",
                ['中文', '英文',],
                [0, 1], 0
        ))
        self.pgPanel.Append(wxpg.BoolProperty("USE_I18N", value=True))


        self.AppendCategoryAuto("时区")
        self.pgPanel.Append(wxpg.EnumProperty("TIME_ZONE", "TIME_ZONE",
                ['伦敦时区', '上海时区', '美国芝加哥'],
                [0, 1, 2], 0
        ))
        self.pgPanel.Append(wxpg.BoolProperty("USE_TZ", value=True))
        

        self.AppendCategoryAuto("静态文件")
        self.pgPanel.Append(wxpg.StringProperty("STATIC_URL", value="/static/"))
        self.pgPanel.Append(wxpg.StringProperty("MEDIA_URL", value="/media/"))
        self.pgPanel.Append(wxpg.StringProperty("STATIC_ROOT", value="os.path.join(BASE_DIR, 'static')"))
        self.pgPanel.Append(wxpg.StringProperty("MEDIA_ROOT", value="os.path.join(BASE_DIR, 'media')"))
        self.pgPanel.Append(wxpg.ArrayStringProperty("STATICFILES_DIRS", value=['A','B','C']))


        self.AppendCategoryAuto("路由")
        self.pgPanel.Append(wxpg.StringProperty("ROOT_URLCONF", value="Demo.urls"))


        self.AppendCategoryAuto("跨域")
        self.pgPanel.Append(wxpg.BoolProperty("CORS_ORIGIN_ALLOW_ALL", value=True))


        self.AppendCategoryAuto("其它")
        self.pgPanel.Append(wxpg.BoolProperty("USE_L10N", value=True))
        self.pgPanel.Append(wxpg.BoolProperty("IFRAME", value=True))

    def AppendCategoryAuto(self, cate_name):
        """二次封装，自动加序号"""
        self.pgPanel.Append(wxpg.PropertyCategory(f"{self.index1}、{cate_name}"))
        self.index1 += 1