from .common import *

class SingleChoiceDialogAdapter(wxpg.PGEditorDialogAdapter):
    """ This demonstrates use of wxpg.PGEditorDialogAdapter.
    """
    def __init__(self, choices):
        wxpg.PGEditorDialogAdapter.__init__(self)
        self.choices = choices

    def DoShowDialog(self, propGrid, property):
        s = wx.GetSingleChoice("Message", "Caption", self.choices)

        if s:
            self.SetValue(s)
            return True

        return False
