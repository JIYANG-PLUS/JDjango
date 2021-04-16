from .common import *
from .PythonEditor import *

TREE_NODES = [
    ("按钮", ("普通按钮","渐变按钮","通用按钮")),
]

class WxPythonCtrlsPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self._init_UI()

    def _init_UI(self):

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.SetBackgroundColour(CON_COLOR_PURE_WHITE)

        self.panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(topsizer)
        topsizer.SetSizeHints(self.panel)
        sizer.Add(self.panel, 1, wx.EXPAND)

        # 分割面板（左右分割）
        self.splitWindow = wx.SplitterWindow(self.panel, -1, style = wx.SP_LIVE_UPDATE)
        topsizer.Add(self.splitWindow, 1, wx.EXPAND)
        self.leftPanel = wx.Panel(self.splitWindow, style=wx.SUNKEN_BORDER) # 左子面板
        self.rightPanel = wx.Panel(self.splitWindow, style=wx.SUNKEN_BORDER) # 右子面板
        self.splitWindow.Initialize(self.leftPanel)
        self.splitWindow.Initialize(self.rightPanel)
        self.splitWindow.SplitVertically(self.leftPanel, self.rightPanel, 180)

        self._init_leftWindow()
        self._init_rightWindow()

    def _init_leftWindow(self):
        """初始化左面板"""
        leftPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftPanel.SetSizer(leftPanelSizer)
        self.tree = wx.TreeCtrl(self.leftPanel, -1, wx.DefaultPosition, (-1, -1)) # , wx.TR_HAS_BUTTONS
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onClickTree, self.tree)
        leftPanelSizer.Add(self.tree, 1, wx.EXPAND | wx.ALL, 2)

        self._init_tree_data()

    def _init_rightWindow(self):
        """初始化右面板"""
        rightPanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.rightPanel.SetSizer(rightPanelSizer)

        self.py_editor = PythonEditor(self.rightPanel)
        rightPanelSizer.Add(self.py_editor, 1, wx.EXPAND | wx.ALL, 2)

        self._init_editor_data()

        # self.code_editor = editor.Editor(self.rightPanel, -1, style=wx.SUNKEN_BORDER)
        # rightPanelSizer.Add(self.code_editor, 1, wx.EXPAND | wx.ALL, 2)

    def _init_editor_data(self):
        """初始化编辑器的数据"""
        text = """\
def SayHi():
    print("Hello World!")
"""
        self.py_editor.SetText(text)
        self.py_editor.EmptyUndoBuffer()
        self.py_editor.Colourise(0, -1)

    def _init_tree_data(self):
        """初始化树控件的数据"""
        self.nodeRootName = "wxPython常用控件"
        self.root = self.tree.AddRoot(self.nodeRootName)
        for node in TREE_NODES:
            temp_node = self.tree.AppendItem(self.root, node[0])
            for _ in node[1]:
                self.tree.AppendItem(temp_node, _)
        self.tree.ExpandAll()

    def onClickTree(self, e):
        """"""
