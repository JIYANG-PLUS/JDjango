import wx

__all__ = [
    'TipsMessageOKBox',
]

def TipsMessageOKBox(parent, msg, title):
    """提示信息"""
    dlg = wx.MessageDialog(parent, msg, title, wx.OK)
    dlg.ShowModal()
    dlg.Destroy()