import wx, json, glob, os, re
import wx.lib.buttons as buttons
from wx.lib import scrolledpanel
import wx.html2
from ..tools._tools import *
from ..tools._re import *
from .. settings import BASE_DIR, CONFIG_PATH, CONFIG_PATH, DJANGO_DOCS_URL, LOCAL_DOCS_PATH
from ..tools import environment as env
from ..tools import models as toolModel
from ..miniCmd.djangoCmd import *

class DocumentationDialog(wx.Dialog):
    def __init__(self, parent, id, **kwargs):
        wx.Dialog.__init__(self, parent, id, '帮助文档', size=(1200, 800))
        labels = wx.Notebook(self)
        self.officialdocs = wx.Panel(labels) # 官方文档
        self.modelsPanel = wx.Panel(labels) # 模型
        self.viewsPanel = wx.Panel(labels) # 视图
        self.urlsPanel = wx.Panel(labels) # 路由
        self.templatesPanel = wx.Panel(labels) # 模板
        self.formsPanel = wx.Panel(labels) # 表单
        self.adminsPanel = wx.Panel(labels) # 管理中心
        self.databasesPanel = wx.Panel(labels) # 数据库

        self._init_officialdocs()
        self._init_modelsPanel()
        self._init_viewsPanel()
        self._init_urlsPanel()
        self._init_templatesPanel()
        self._init_formsPanel()
        self._init_adminsPanel()
        self._init_databasesPanel()

        labels.AddPage(self.officialdocs, '官方文档')
        labels.AddPage(self.modelsPanel, '模型')
        labels.AddPage(self.viewsPanel, '视图')
        labels.AddPage(self.urlsPanel, '路由')
        labels.AddPage(self.templatesPanel, '模板')
        labels.AddPage(self.formsPanel, '表单')
        labels.AddPage(self.adminsPanel, '管理中心')
        labels.AddPage(self.databasesPanel, '数据库')

    def _init_officialdocs(self):
        """官方文档初始化"""
        self.splitOfficialdocs = wx.SplitterWindow(self.officialdocs, -1)
        self.leftPanelOfficialdocs = wx.Panel(self.splitOfficialdocs, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelOfficialdocs = wx.Panel(self.splitOfficialdocs, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitOfficialdocs.Initialize(self.leftPanelOfficialdocs)
        self.splitOfficialdocs.Initialize(self.rightPanelOfficialdocs)
        self.rightPanelOfficialdocs.SetBackgroundColour("gray")
        self.splitOfficialdocs.SplitVertically(self.leftPanelOfficialdocs, self.rightPanelOfficialdocs, 133)

        self.leftPanelOfficialdocsSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftPanelOfficialdocsSizer.Add(self.splitOfficialdocs, 1, wx.EXPAND | wx.ALL, 0)
        self.officialdocs.SetSizer(self.leftPanelOfficialdocsSizer)

        # 左子面板  树控件
        leftPanelOfficialdocsSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftPanelOfficialdocsTree = wx.TreeCtrl(self.leftPanelOfficialdocs, -1, wx.DefaultPosition, (-1, -1))
        leftPanelOfficialdocsSizer.Add(self.leftPanelOfficialdocsTree, 1, wx.EXPAND | wx.ALL, 2)
        self.leftPanelOfficialdocs.SetSizer(leftPanelOfficialdocsSizer)
        self._init_officialdocs_tree()

        # 右子面板  HTML控件
        rightPanelOfficialdocsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.browser = wx.html2.WebView.New(self.rightPanelOfficialdocs)
        self.browser.LoadURL(DJANGO_DOCS_URL['31']) # 加载页面
        # html_string = read_file(DJANGO_DOCS_PATH)
        # self.browser.SetPage(html_string, "") # 加载字符串
        rightPanelOfficialdocsSizer.Add(self.browser, 1, wx.EXPAND | wx.ALL, 2)
        self.rightPanelOfficialdocs.SetSizer(rightPanelOfficialdocsSizer)

        # 事件绑定
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnClickOfficalDocsTree, self.leftPanelOfficialdocsTree)

    def _init_officialdocs_tree(self):
        """构建左-左目录树"""
        self.leftPanelOfficialdocsRoot = self.leftPanelOfficialdocsTree.AddRoot(f'稳定版本')
        self.leftPanelOfficialdocsTree.AppendItem(self.leftPanelOfficialdocsRoot, "3.1版本")
        self.leftPanelOfficialdocsTree.AppendItem(self.leftPanelOfficialdocsRoot, "2.2版本")

    def OnClickOfficalDocsTree(self, e):
        """双击官方文档树控件事件"""
        nodeName = self.leftPanelModelsTree.GetItemText(e.GetItem())
        temp = {
            '3.1版本' : '31',
            '2.2版本' : '22',
        }
        if nodeName != f'选择版本':
            self.browser.LoadURL(DJANGO_DOCS_URL[temp[nodeName]])

    def _init_modelsPanel(self):
        """模型界面初始化"""
        self.splitModelsWindow = wx.SplitterWindow(self.modelsPanel, -1)
        self.leftPanelModels = wx.Panel(self.splitModelsWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelModels = wx.Panel(self.splitModelsWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitModelsWindow.Initialize(self.leftPanelModels)
        self.splitModelsWindow.Initialize(self.rightPanelModels)
        self.rightPanelModels.SetBackgroundColour("gray")
        self.splitModelsWindow.SplitVertically(self.leftPanelModels, self.rightPanelModels, 133)

        self.modelsPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.modelsPanelSizer.Add(self.splitModelsWindow, 1, wx.EXPAND | wx.ALL, 0)
        self.modelsPanel.SetSizer(self.modelsPanelSizer)

        # 左子面板  树控件
        leftPanelModelsSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftPanelModelsTree = wx.TreeCtrl(self.leftPanelModels, -1, wx.DefaultPosition, (-1, -1))
        leftPanelModelsSizer.Add(self.leftPanelModelsTree, 1, wx.EXPAND | wx.ALL, 2)
        self.leftPanelModels.SetSizer(leftPanelModelsSizer)
        self._init_modelsPanel_tree()

        # 右子面板  HTML控件
        rightPanelModelsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.browserModels = wx.html2.WebView.New(self.rightPanelModels)
        # self.browser.LoadURL(DJANGO_DOCS_URL['31']) # 加载页面
        # html_string = read_file(DJANGO_DOCS_PATH)
        # self.browser.SetPage(html_string, "") # 加载字符串
        rightPanelModelsSizer.Add(self.browserModels, 1, wx.EXPAND | wx.ALL, 2)
        self.rightPanelModels.SetSizer(rightPanelModelsSizer)

        # 事件绑定
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnClickModelsTree, self.leftPanelModelsTree)

    def _init_modelsPanel_tree(self):
        """构建左-左目录树"""
        self.leftPanelModelsRoot = self.leftPanelModelsTree.AddRoot(f'模型-文档')
        self.leftPanelModelsTree.AppendItem(self.leftPanelModelsRoot, "创建模型")
        self.leftPanelModelsTree.AppendItem(self.leftPanelModelsRoot, "创建模型管理器")
        self.leftPanelModelsTree.AppendItem(self.leftPanelModelsRoot, "使用模型")
    
    def OnClickModelsTree(self, e):
        """双击树节点事件"""
        temp = {
            '创建模型' : 'models_create.html',
            '创建模型管理器' : 'models_controller.html',
            '使用模型' : 'models_user.html',
        }
        nodeName = self.leftPanelModelsTree.GetItemText(e.GetItem())
        if nodeName != f'模型-文档':
            self.browserModels.SetPage(read_file(os.path.join(LOCAL_DOCS_PATH, temp[nodeName])), "")

    def _init_viewsPanel(self):
        """视图界面初始化"""
        self.splitViewsWindow = wx.SplitterWindow(self.viewsPanel, -1)
        self.leftPanelViews = wx.Panel(self.splitViewsWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelViews = wx.Panel(self.splitViewsWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitViewsWindow.Initialize(self.leftPanelViews)
        self.splitViewsWindow.Initialize(self.rightPanelViews)
        self.rightPanelViews.SetBackgroundColour("gray")
        self.splitViewsWindow.SplitVertically(self.leftPanelViews, self.rightPanelViews, 133)

        self.viewsPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.viewsPanelSizer.Add(self.splitViewsWindow, 1, wx.EXPAND | wx.ALL, 0)
        self.viewsPanel.SetSizer(self.viewsPanelSizer)

    def _init_urlsPanel(self):
        """路由界面初始化"""
        self.splitUrlsWindow = wx.SplitterWindow(self.urlsPanel, -1)
        self.leftPanelUrls = wx.Panel(self.splitUrlsWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelUrls = wx.Panel(self.splitUrlsWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitUrlsWindow.Initialize(self.leftPanelUrls)
        self.splitUrlsWindow.Initialize(self.rightPanelUrls)
        self.rightPanelUrls.SetBackgroundColour("gray")
        self.splitUrlsWindow.SplitVertically(self.leftPanelUrls, self.rightPanelUrls, 133)

        self.urlsPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.urlsPanelSizer.Add(self.splitUrlsWindow, 1, wx.EXPAND | wx.ALL, 0)
        self.urlsPanel.SetSizer(self.urlsPanelSizer)

    def _init_templatesPanel(self):
        """模板界面初始化"""
        self.splitTemplatesWindow = wx.SplitterWindow(self.templatesPanel, -1)
        self.leftPanelTemplates = wx.Panel(self.splitTemplatesWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelTemplates = wx.Panel(self.splitTemplatesWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitTemplatesWindow.Initialize(self.leftPanelTemplates)
        self.splitTemplatesWindow.Initialize(self.rightPanelTemplates)
        self.rightPanelTemplates.SetBackgroundColour("gray")
        self.splitTemplatesWindow.SplitVertically(self.leftPanelTemplates, self.rightPanelTemplates, 133)

        self.templatesPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.templatesPanelSizer.Add(self.splitTemplatesWindow, 1, wx.EXPAND | wx.ALL, 0)
        self.templatesPanel.SetSizer(self.templatesPanelSizer)

    def _init_formsPanel(self):
        """表单界面初始化"""
        self.splitFormsWindow = wx.SplitterWindow(self.formsPanel, -1)
        self.leftPanelForms = wx.Panel(self.splitFormsWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelForms = wx.Panel(self.splitFormsWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitFormsWindow.Initialize(self.leftPanelForms)
        self.splitFormsWindow.Initialize(self.rightPanelForms)
        self.rightPanelForms.SetBackgroundColour("gray")
        self.splitFormsWindow.SplitVertically(self.leftPanelForms, self.rightPanelForms, 133)

        self.formsPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.formsPanelSizer.Add(self.splitFormsWindow, 1, wx.EXPAND | wx.ALL, 0)
        self.formsPanel.SetSizer(self.formsPanelSizer)

    def _init_adminsPanel(self):
        """管理中心界面初始化"""
        self.splitAdminsWindow = wx.SplitterWindow(self.adminsPanel, -1)
        self.leftPanelAdmins = wx.Panel(self.splitAdminsWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelAdmins = wx.Panel(self.splitAdminsWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitAdminsWindow.Initialize(self.leftPanelAdmins)
        self.splitAdminsWindow.Initialize(self.rightPanelAdmins)
        self.rightPanelAdmins.SetBackgroundColour("gray")
        self.splitAdminsWindow.SplitVertically(self.leftPanelAdmins, self.rightPanelAdmins, 133)

        self.adminsPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.adminsPanelSizer.Add(self.splitAdminsWindow, 1, wx.EXPAND | wx.ALL, 0)
        self.adminsPanel.SetSizer(self.adminsPanelSizer)

    def _init_databasesPanel(self):
        """数据库界面初始化"""
        self.splitDatabasesWindow = wx.SplitterWindow(self.databasesPanel, -1)
        self.leftPanelDatabases = wx.Panel(self.splitDatabasesWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanelDatabases = wx.Panel(self.splitDatabasesWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitDatabasesWindow.Initialize(self.leftPanelDatabases)
        self.splitDatabasesWindow.Initialize(self.rightPanelDatabases)
        self.rightPanelDatabases.SetBackgroundColour("gray")
        self.splitDatabasesWindow.SplitVertically(self.leftPanelDatabases, self.rightPanelDatabases, 133)

        self.databasesPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.databasesPanelSizer.Add(self.splitDatabasesWindow, 1, wx.EXPAND | wx.ALL, 0)
        self.databasesPanel.SetSizer(self.databasesPanelSizer)
