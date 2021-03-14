from .common import *

class SizeProperty(wxpg.PGProperty):
    """ Demonstrates a property with few children.
    """
    def __init__(self, label, name = wxpg.PG_LABEL, value=wx.Size(0, 0)):
        wxpg.PGProperty.__init__(self, label, name)

        value = self._ConvertValue(value)

        self.AddPrivateChild( wxpg.IntProperty("X", value=value.x) )
        self.AddPrivateChild( wxpg.IntProperty("Y", value=value.y) )

        self.m_value = value

    def GetClassName(self):
        return self.__class__.__name__

    def DoGetEditorClass(self):
        return wxpg.PropertyGridInterface.GetEditorByName("TextCtrl")

    def RefreshChildren(self):
        size = self.m_value
        self.Item(0).SetValue( size.x )
        self.Item(1).SetValue( size.y )

    def _ConvertValue(self, value):
        """ Utility convert arbitrary value to a real wx.Size.
        """
        import collections
        if isinstance(value, collections.Sequence) or hasattr(value, '__getitem__'):
            value = wx.Size(*value)
        return value

    def ChildChanged(self, thisValue, childIndex, childValue):
        size = self._ConvertValue(self.m_value)
        if childIndex == 0:
            size.x = childValue
        elif childIndex == 1:
            size.y = childValue
        else:
            raise AssertionError

        return size
