from .common import *

class DirsProperty(wxpg.ArrayStringProperty):
    """ Sample of a custom custom ArrayStringProperty.

        Because currently some of the C++ helpers from wxArrayStringProperty
        and wxProperytGrid are not available, our implementation has to quite
        a bit 'manually'. Which is not too bad since Python has excellent
        string and list manipulation facilities.
    """
    def __init__(self, label, name = wxpg.PG_LABEL, value=[]):
        wxpg.ArrayStringProperty.__init__(self, label, name, value)
        self.m_display = ''
        # Set default delimiter
        self.SetAttribute("Delimiter", ',')


    # NOTE: In the Classic version of the propgrid classes, all of the wrapped
    # property classes override DoGetEditorClass so it calls GetEditor and
    # looks up the class using that name, and hides DoGetEditorClass from the
    # usable API. Jumping through those hoops is no longer needed in Phoenix
    # as Phoenix allows overriding all necessary virtual methods without
    # special support in the wrapper code, so we just need to override
    # DoGetEditorClass here instead.
    def DoGetEditorClass(self):
        return wxpg.PropertyGridInterface.GetEditorByName("TextCtrlAndButton")


    def ValueToString(self, value, flags):
        # let's just use the cached display value
        return self.m_display


    def OnSetValue(self):
        self.GenerateValueAsString()


    def DoSetAttribute(self, name, value):
        retval = super(DirsProperty, self).DoSetAttribute(name, value)

        # Must re-generate cached string when delimiter changes
        if name == "Delimiter":
            self.GenerateValueAsString(delim=value)

        return retval


    def GenerateValueAsString(self, delim=None):
        """ This function creates a cached version of displayed text
            (self.m_display).
        """
        if not delim:
            delim = self.GetAttribute("Delimiter")
            if not delim:
                delim = ','

        ls = self.GetValue()
        if delim == '"' or delim == "'":
            text = ' '.join(['%s%s%s'%(delim,a,delim) for a in ls])
        else:
            text = ', '.join(ls)
        self.m_display = text


    def StringToValue(self, text, argFlags):
        """ If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        delim = self.GetAttribute("Delimiter")
        if delim == '"' or delim == "'":
            # Proper way to call same method from super class
            return super(DirsProperty, self).StringToValue(text, 0)
        v = [a.strip() for a in text.split(delim)]
        return (True, v)


    def OnEvent(self, propgrid, primaryEditor, event):
        if event.GetEventType() == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            dlg = wx.DirDialog(propgrid,
                               "Select a directory to be added to "
                                 "the list:")

            if dlg.ShowModal() == wx.ID_OK:
                new_path = dlg.GetPath()
                old_value = self.m_value
                if old_value:
                    new_value = list(old_value)
                    new_value.append(new_path)
                else:
                    new_value = [new_path]
                self.SetValueInEvent(new_value)
                retval = True
            else:
                retval = False

            dlg.Destroy()
            return retval

        return False
