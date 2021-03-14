from .common import *

class LargeImageEditor(wxpg.PGEditor):
    """
    Double-height text-editor with image in front.
    """
    def __init__(self):
        wxpg.PGEditor.__init__(self)

    def CreateControls(self, propgrid, property, pos, sz):
        try:
            x, y = pos
            w, h = sz
            h = 64 + 6

            # Make room for button
            bw = propgrid.GetRowHeight()
            w -= bw

            self.property = property

            self.RefreshThumbnail()
            self.statbmp = wx.StaticBitmap(propgrid.GetPanel(), -1, self.bmp, (x,y))
            self.tc = wx.TextCtrl(propgrid.GetPanel(), -1,  "",
                                  (x+h,y), (2048,h), wx.BORDER_NONE)

            btn = wx.Button(propgrid.GetPanel(), wx.ID_ANY, '...',
                            (x+w, y),
                            (bw, h), wx.WANTS_CHARS)

            # When the textctrl is destroyed, destroy the statbmp too
            def _cleanupStatBmp(evt):
                if self.statbmp:
                    self.statbmp.Destroy()
            self.tc.Bind(wx.EVT_WINDOW_DESTROY, _cleanupStatBmp)

            return wxpg.PGWindowList(self.tc, btn)
        except:
            import traceback
            print(traceback.print_exc())


    def GetName(self):
        return "LargeImageEditor"


    def UpdateControl(self, property, ctrl):
        s = property.GetDisplayedString()
        self.tc.SetValue(s)
        self.RefreshThumbnail()
        self.statbmp.SetBitmap(self.bmp)


    def DrawValue(self, dc, rect, property, text):
        if not property.IsValueUnspecified():
            dc.DrawText(property.GetDisplayedString(), rect.x+5, rect.y)


    def OnEvent(self, propgrid, property, ctrl, event):
        """ Return True if modified editor value should be committed to
            the property. To just mark the property value modified, call
            propgrid.EditorsValueWasModified().
        """
        if not ctrl:
            return False

        evtType = event.GetEventType()

        if evtType == wx.wxEVT_COMMAND_TEXT_ENTER:
            if propgrid.IsEditorsValueModified():
                return True
        elif evtType == wx.wxEVT_COMMAND_TEXT_UPDATED:
            #
            # Pass this event outside wxPropertyGrid so that,
            # if necessary, program can tell when user is editing
            # a textctrl.
            event.Skip()
            event.SetId(propgrid.GetId())

            propgrid.EditorsValueWasModified()
            return False

        return False

    def GetValueFromControl(self, property, ctrl):
        """ Return tuple (wasSuccess, newValue), where wasSuccess is True if
            different value was acquired successfully.
        """
        textVal = self.tc.GetValue()

        if property.UsesAutoUnspecified() and not textVal:
            return (None, True)

        res, value = property.StringToValue(textVal,
                                            wxpg.PG_EDITABLE_VALUE)

        # Changing unspecified always causes event (returning
        # True here should be enough to trigger it).
        if not res and value is None:
            res = True

        return (res, value)


    def SetValueToUnspecified(self, property, ctrl):
        ctrl.Remove(0, len(ctrl.GetValue()))
        self.RefreshThumbnail()
        self.statbmp.SetBitmap(self.bmp)


    def SetControlStringValue(self, property, ctrl, txt):
        self.tc.SetValue(txt)
        self.RefreshThumbnail()
        self.statbmp.SetBitmap(self.bmp)


    def CanContainCustomImage(self):
        return True


    def RefreshThumbnail(self):
        """
        We use here very simple image scaling code.
        """
        def _makeEmptyBmp():
            bmp = wx.Bitmap(64,64)
            dc = wx.MemoryDC()
            dc.SelectObject(bmp)
            dc.SetPen(wx.Pen(wx.BLACK))
            dc.SetBrush(wx.WHITE_BRUSH)
            dc.DrawRectangle(0, 0, 64, 64)
            return bmp

        if not self.property:
            self.bmp = _makeEmptyBmp()
            return

        path = self.property.DoGetValue()

        if not os.path.isfile(path):
            self.bmp = _makeEmptyBmp()
            return

        image = wx.Image(path)
        image.Rescale(64, 64)
        self.bmp = wx.Bitmap(image)
