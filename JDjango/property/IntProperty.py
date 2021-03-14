from .common import *

class IntProperty2(wxpg.PGProperty):
    """
    This is a simple re-implementation of wxIntProperty.
    """
    def __init__(self, label, name = wxpg.PG_LABEL, value=0):
        wxpg.PGProperty.__init__(self, label, name)
        self.SetValue(value)

    def GetClassName(self):
        """
        This is not 100% necessary and in future is probably going to be
        automated to return class name.
        """
        return "IntProperty2"

    def DoGetEditorClass(self):
        return wxpg.PropertyGridInterface.GetEditorByName("TextCtrl")

    def ValueToString(self, value, flags):
        return str(value)

    def StringToValue(self, s, flags):
        """
        If failed, return False or (False, None). If success, return tuple
        (True, newValue).
        """
        try:
            v = int(s)
            if self.GetValue() != v:
                return (True, v)
        except (ValueError, TypeError):
            if flags & wxpg.PG_REPORT_ERROR:
                wx.MessageBox("Cannot convert '%s' into a number."%s, "Error")
        return (False, None)

    def IntToValue(self, v, flags):
        """
        If failed, return False or (False, None). If success, return tuple
        (True, newValue).
        """
        if (self.GetValue() != v):
            return (True, v)
        return False

    def ValidateValue(self, value, validationInfo):
        """ Let's limit the value to range -10000 and 10000.
        """
        # Just test this function to make sure validationInfo and
        # wxPGVFBFlags work properly.
        oldvfb__ = validationInfo.GetFailureBehavior()

        # Mark the cell if validation failed
        validationInfo.SetFailureBehavior(wxpg.PG_VFB_MARK_CELL)

        if value is None or value < -10000 or value > 10000:
            return False

        return True