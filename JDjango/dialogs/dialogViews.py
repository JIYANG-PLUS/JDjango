import wx, json, glob, os
import wx.lib.buttons as buttons
from wx.lib import scrolledpanel
from ..tools._tools import *
from ..tools._re import *
from ..settings import BASE_DIR, CONFIG_PATH, SETTINGSS
from ..tools import environment as env
from ..tools import models as toolModel
from ..miniCmd.djangoCmd import *
from ..constant import *

LABEL_COL_LEN = 200

class ViewGenerateDialog(wx.Dialog):

    def __init__(self, parent):

        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = '新增视图', size=(800, 600))

        # 一些控制容器
        self.labelStaticTexts = []

        self._init_UI()

        # 布局后，美化界面
        self._init_label_font()

    def _init_UI(self):
        """初始化界面布局"""
        # 总面板
        self.panel = wx.Panel(self)
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.panelSizer)

        # 分割面板（左右分割）
        self.splitWindow = wx.SplitterWindow(self.panel, -1)
        self.panelSizer.Add(self.splitWindow, 1, wx.EXPAND | wx.ALL, 2)

        # 左子面板
        self.leftPanel = wx.Panel(self.splitWindow, style=wx.SUNKEN_BORDER)
        self.leftPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftPanel.SetSizer(self.leftPanelSizer )
        
        # 右子面板
        self.rightPanel = wx.Panel(self.splitWindow, style=wx.SUNKEN_BORDER)
        self.rightPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.rightPanel.SetSizer(self.rightPanelSizer)
        
        self.splitWindow.Initialize(self.leftPanel)
        self.splitWindow.Initialize(self.rightPanel)
        self.splitWindow.SplitVertically(self.leftPanel, self.rightPanel, 500)

        self._init_left_panel()
        self._init_right_panel()

    def _init_left_panel(self):
        """初始化左子面板"""
        # 选择文件写入路径【此处更改为选择App】
        self.selectFilePanel = wx.Panel(self.leftPanel)
        selectFilePanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.selectFilePanel.SetSizer(selectFilePanelSizer)
        self.leftPanelSizer.Add(self.selectFilePanel, 0, wx.EXPAND | wx.ALL, 2)
        # self.selectFilePanel.SetBackgroundColour(CON_COLOR_BLACK) # CON_COLOR_PURE_WHITE

        self.labelSelectFile = wx.StaticText(self.selectFilePanel, -1, "选择视图所属的应用程序")
        self.choiceSelectFile = wx.Choice(self.selectFilePanel, -1, choices=[' ',]+get_all_apps_name())
        self.btnSubmit = buttons.GenButton(self.selectFilePanel, -1, '创建')
        selectFilePanelSizer.Add(self.labelSelectFile, 0, wx.EXPAND | wx.ALL, 2)
        selectFilePanelSizer.Add(self.choiceSelectFile, 1, wx.EXPAND | wx.ALL, 2)
        selectFilePanelSizer.Add(self.btnSubmit, 0, wx.EXPAND | wx.ALL, 2)
        self.labelSelectFile.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))


        # 视图名称
        self.inputViewNameStaticBox = wx.StaticBox(self.leftPanel, -1, '')
        self.inputViewNamePanel = wx.StaticBoxSizer(self.inputViewNameStaticBox, wx.HORIZONTAL)
        self.leftPanelSizer.Add(self.inputViewNamePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputViewName = wx.StaticText(self.leftPanel, -1, "视图名称：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_COL_LEN, -1))
        self.inputViewName = wx.TextCtrl(self.leftPanel, -1, style = wx.ALIGN_LEFT)
        self.inputViewNamePanel.Add(self.labelInputViewName, 0, wx.EXPAND | wx.ALL, 2)
        self.inputViewNamePanel.Add(self.inputViewName, 1, wx.EXPAND | wx.ALL, 2)

        # 路由反向解析名称【默认取 视图名称】
        self.inputReverseViewNameStaticBox = wx.StaticBox(self.leftPanel, -1, '')
        self.inputReverseViewNamePanel = wx.StaticBoxSizer(self.inputReverseViewNameStaticBox, wx.HORIZONTAL)
        self.leftPanelSizer.Add(self.inputReverseViewNamePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputReverseViewName = wx.StaticText(self.leftPanel, -1, "路由反向解析名称：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_COL_LEN, -1))
        self.inputReverseViewName = wx.TextCtrl(self.leftPanel, -1, style = wx.ALIGN_LEFT)
        self.inputReverseViewNamePanel.Add(self.labelInputReverseViewName, 0, wx.EXPAND | wx.ALL, 2)
        self.inputReverseViewNamePanel.Add(self.inputReverseViewName, 1, wx.EXPAND | wx.ALL, 2)

        # 路由路径指定
        self.inputUrlPathStaticBox = wx.StaticBox(self.leftPanel, -1, '')
        self.inputUrlPathPanel = wx.StaticBoxSizer(self.inputUrlPathStaticBox, wx.HORIZONTAL)
        self.leftPanelSizer.Add(self.inputUrlPathPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputUrlPath = wx.StaticText(self.leftPanel, -1, "路由路径指定：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_COL_LEN, -1))
        self.inputUrlPath = wx.TextCtrl(self.leftPanel, -1, style = wx.ALIGN_LEFT)
        self.inputUrlPathPanel.Add(self.labelInputUrlPath, 0, wx.EXPAND | wx.ALL, 2)
        self.inputUrlPathPanel.Add(self.inputUrlPath, 1, wx.EXPAND | wx.ALL, 2)

        # 路由预览
        self.inputUrlPreviewStaticBox = wx.StaticBox(self.leftPanel, -1, '')
        self.inputUrlPreviewPanel = wx.StaticBoxSizer(self.inputUrlPreviewStaticBox, wx.HORIZONTAL)
        self.leftPanelSizer.Add(self.inputUrlPreviewPanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputUrlPreview = wx.StaticText(self.leftPanel, -1, "路由预览：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_COL_LEN, -1))
        self.inputUrlPreview = wx.TextCtrl(self.leftPanel, -1, style = wx.ALIGN_LEFT)
        self.inputUrlPreviewPanel.Add(self.labelInputUrlPreview, 0, wx.EXPAND | wx.ALL, 2)
        self.inputUrlPreviewPanel.Add(self.inputUrlPreview, 1, wx.EXPAND | wx.ALL, 2)
        self.inputUrlPreview.Enable(False)

        # 选择视图类型
        self.choiceViewTypeStaticBox = wx.StaticBox(self.leftPanel, -1, '')
        self.viewTypePanel = wx.StaticBoxSizer(self.choiceViewTypeStaticBox, wx.HORIZONTAL)
        self.leftPanelSizer.Add(self.viewTypePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelChoiceViewType = wx.StaticText(self.leftPanel, -1, "选择要创建的视图类型：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_COL_LEN, -1))
        self.choiceViewType = wx.Choice(self.leftPanel, -1, choices=[' ',]+CON_VIEW_CHOICES)
        self.viewTypePanel.Add(self.labelChoiceViewType, 0, wx.EXPAND | wx.ALL, 2)
        self.viewTypePanel.Add(self.choiceViewType, 1, wx.EXPAND | wx.ALL, 2)

        # 代码预览面板
        self.codeReviewPanel = wx.Panel(self.leftPanel)
        self.codeReviewPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.codeReviewPanel.SetSizer(self.codeReviewPanelSizer)
        self.leftPanelSizer.Add(self.codeReviewPanel, 1, wx.EXPAND | wx.ALL, 2)

        self.inputCodeReview = wx.TextCtrl(self.codeReviewPanel, -1, style=wx.TE_MULTILINE)
        self.codeReviewPanelSizer.Add(self.inputCodeReview, 1, wx.EXPAND | wx.ALL, 2)

        # 标签美化
        self.labelStaticTexts.extend([
            self.labelChoiceViewType, self.labelInputUrlPath,
            self.labelInputViewName, self.labelInputReverseViewName,
            self.labelInputUrlPreview, 
        ])

        # 文本实时监听事件
        self.Bind(wx.EVT_TEXT, self.onInputViewName, self.inputViewName)

    def _init_right_panel(self):
        """初始化右子面板"""
        # 视图名称
        self.inputViewNameStaticBox = wx.StaticBox(self.leftPanel, -1, '')
        self.inputViewNamePanel = wx.StaticBoxSizer(self.inputViewNameStaticBox, wx.HORIZONTAL)
        self.leftPanelSizer.Add(self.inputViewNamePanel, 0, wx.EXPAND | wx.ALL, 2)

        self.labelInputViewName = wx.StaticText(self.leftPanel, -1, "视图名称：", style=wx.ALIGN_CENTRE_HORIZONTAL, size=(LABEL_COL_LEN, -1))
        self.inputViewName = wx.TextCtrl(self.leftPanel, -1, style = wx.ALIGN_LEFT)
        self.inputViewNamePanel.Add(self.labelInputViewName, 0, wx.EXPAND | wx.ALL, 2)
        self.inputViewNamePanel.Add(self.inputViewName, 1, wx.EXPAND | wx.ALL, 2)

        # 标签美化
        self.labelStaticTexts.extend([
            
        ])

    def onInputViewName(self, e):
        """视图名称监听实时输入"""
        self.inputReverseViewName.SetValue(self.inputViewName.GetValue().strip().lower())
        
    def _init_label_font(self):
        """标签提示信息字体初始化"""
        for _ in self.labelStaticTexts:
            _.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            _.SetForegroundColour(CON_COLOR_BLUE)

    def onRadiosClick(self, e):
        """"""
        # print(self.radiosPanel.GetSelection()) # 获取当前选中元素的下标
        pass

