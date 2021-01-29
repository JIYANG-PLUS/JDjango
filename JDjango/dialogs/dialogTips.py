import wx

__all__ = [
    'TipsMessageOKBox',
    'CodePreviewBox',
]

def TipsMessageOKBox(parent, msg, title):
    """提示信息"""
    dlg = wx.MessageDialog(parent, msg, title, wx.OK)
    dlg.ShowModal()
    dlg.Close(True)

def CodePreviewBox(parent, code):
    """代码预览窗口"""
    dlg = CodePreviewDialog(parent, code)
    dlg.ShowModal()
    dlg.Close(True)

class CodePreviewDialog(wx.Dialog):
    def __init__(self, parent, code):
        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = '代码预览', size=(800, 500))
        
        self._init_UI(code)

    def _init_UI(self, code):
        """初始化界面布局"""
        # 最外层布局
        self.panel = wx.Panel(self)
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.panelSizer)

        self.inputCode = wx.TextCtrl(self.panel, -1, style=wx.TE_MULTILINE)
        self.panelSizer.Add(self.inputCode, 1, wx.EXPAND | wx.ALL, 2)
        self.inputCode.SetValue(code)
        self.inputCode.SetEditable(False)
