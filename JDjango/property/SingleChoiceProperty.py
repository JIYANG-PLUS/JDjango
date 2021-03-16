from .common import *

class SingleChoiceDialogAdapter(wxpg.PGEditorDialogAdapter):
    """ 构建属性编辑器对话框
    """
    def __init__(self, choices):
        wxpg.PGEditorDialogAdapter.__init__(self)
        self.choices = choices

    def DoShowDialog(self, propGrid, property):
        s = wx.GetSingleChoice("选择语言", "语言选项", self.choices)

        if s:
            self.SetValue(s)
            return True

        return False

class SingleChoiceProperty(wxpg.StringProperty):
    """单选框对话框"""
    def __init__(self, label, name=wxpg.PG_LABEL, value='', choices=None):
        wxpg.StringProperty.__init__(self, label, name, value)

        if None == choices:
            self.choices = []
        else:
            self.choices = choices

    def DoGetEditorClass(self):
        return wxpg.PropertyGridInterface.GetEditorByName("TextCtrlAndButton")

    def GetEditorDialog(self):
        return SingleChoiceDialogAdapter(self.choices)
