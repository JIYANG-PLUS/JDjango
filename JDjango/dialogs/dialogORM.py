import wx
import wx.html2
from .dialogTips import *
from ..tools._tools import *
from ..miniCmd import djangoCmd as djcmd
from ..settings import CONFIG_PATH

class ORMDialog(wx.Dialog):
    
    def __init__(self, parent, **kwargs):
        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = "ORM一键生成系统", size=(660, 350))

        self._init_UI()

        self._init_tree()

    def _init_UI(self):
        """初始化界面布局"""
        self.mainPanel = wx.Panel(self)
        mainPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainPanel.SetSizer(mainPanelSizer)

        self.splitWindow = wx.SplitterWindow(self.mainPanel, -1)
        self.leftPanel = wx.Panel(self.splitWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanel = wx.Panel(self.splitWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitWindow.Initialize(self.leftPanel)
        self.splitWindow.Initialize(self.rightPanel)
        self.splitWindow.SplitVertically(self.leftPanel, self.rightPanel, 200)
        mainPanelSizer.Add(self.splitWindow, 1, wx.EXPAND | wx.ALL, 0)

        self._init_left_panel()
        self._init_right_panel()

    def _init_left_panel(self):
        """左子面板"""
        leftPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftPanel.SetSizer(leftPanelSizer)

        self.tree = wx.TreeCtrl(self.leftPanel, -1, wx.DefaultPosition, (-1, -1)) # , wx.TR_HAS_BUTTONS
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnClickTree, self.tree)
        leftPanelSizer.Add(self.tree, 1, wx.EXPAND | wx.ALL, 2)

    def _init_right_panel(self):
        """右子面板"""
        rightPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rightPanel.SetSizer(rightPanelSizer)

        self.browser = wx.html2.WebView.New(self.rightPanel) # style=wx.html.HW_NO_SelectION 不可选中文本
        rightPanelSizer.Add(self.browser, 1, wx.EXPAND | wx.ALL, 2)

    def OnClickTree(self, e):
        """双击树节点事件"""
        clickNodeName = self.tree.GetItemText(e.GetItem())
        if "应用程序" == clickNodeName:
            return

        parentNode = self.tree.GetItemParent(e.GetItem())
        nodeName = self.tree.GetItemText(parentNode)
        if clickNodeName not in self.untouched:
            html_string = ''.join(djcmd.get_orm_code(
                mode = clickNodeName
                , model_name = nodeName
                , all_args = ''
            ))
            self.browser.SetPage(html_string, "") # 加载字符串

    def _init_tree(self):
        """构建左-左目录树"""
        self.untouched = []

        self.root = self.tree.AddRoot("应用程序")
        app_names = get_configs(CONFIG_PATH)['app_names'] # 取所有的应用程序名

        if app_names:
            self.untouched.extend(app_names)
            types = ['SELECT', 'INSERT', 'DELETE', 'UPDATE', 'JOIN']
            for app_name in app_names:
                temp = self.tree.AppendItem(self.root, app_name)
                models = djcmd.get_models_by_appname(app_name) # 通过应用程序名获取所有的模型名称
                if models:
                    self.untouched.extend(models)
                    for model in models:
                        temp_model = self.tree.AppendItem(temp, model)
                        for _ in types:
                            self.tree.AppendItem(temp_model, _)

        self.untouched.extend([
            "应用程序",
        ])

        self.tree.Expand(self.root)
        