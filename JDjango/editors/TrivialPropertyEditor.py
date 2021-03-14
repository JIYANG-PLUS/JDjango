from .common import *

class TrivialPropertyEditor(wxpg.PGEditor):
    """ 简单自定义 TextCtrl + Button """

    def __init__(self):
        wxpg.PGEditor.__init__(self)

    def CreateControls(self, propgrid, property, pos, sz):
        """ 为填写属性值创建控件
            必须使用：propgrid.GetPanel() 作为控件的父面板
            返回值可以是单个文本控件或(文本控件，按钮控件)组成的元组
        """
        x, y = pos # 空间坐标
        width, height = sz # 宽、高
        height = 64 + 6 # 预留一定的高度

        btn_width = propgrid.GetRowHeight() # 为按钮腾出宽度
        width -= btn_width # 文本显示区域

        s_value = property.GetDisplayedString() # 获取当前的属性值

        tc = wx.TextCtrl(
            propgrid.GetPanel(), 
            wx.ID_ANY, 
            s_value,
            (x, y), 
            (width, height),
            wx.TE_PROCESS_ENTER
        )
        btn = wx.Button(
            propgrid.GetPanel(), 
            wx.ID_ANY, 
            '...',
            (x+width, y),
            (btn_width, height), 
            wx.WANTS_CHARS
        )
        return wxpg.PGWindowList(tc, btn)

    def UpdateControl(self, property, ctrl):
        """更新控件值"""
        ctrl.SetValue(property.GetDisplayedString())

    def DrawValue(self, dc, rect, property, text):
        """画值"""
        if not property.IsValueUnspecified():
            dc.DrawText(property.GetDisplayedString(), rect.x+5, rect.y)

    def OnEvent(self, propgrid, property, ctrl, event):
        """ 将修改器的值提交给属性时返回 True
            仅判断是否更改：propgrid.EditorsValueWasModified()
        """
        if not ctrl:
            return False

        evtType = event.GetEventType() # 获取事件类型

        if evtType == wx.wxEVT_COMMAND_TEXT_ENTER: # 输入
            if propgrid.IsEditorsValueModified():
                return True
        elif evtType == wx.wxEVT_COMMAND_TEXT_UPDATED: # 更新
            # 编辑输入框时将事件传递到 wxPropertyGrid 之外
            event.Skip()
            event.SetId(propgrid.GetId())
            propgrid.EditorsValueWasModified()
            return False

        return False

    def GetValueFromControl(self, property, ctrl):
        """ 返回元组类型 (wasSuccess, newValue), 
            成功获取不同的值时 wasSuccess 返回 True
        """
        textVal = ctrl.GetValue() # 获取控件值

        if property.UsesAutoUnspecified() and not textVal:
            return (True, None)

        res, value = property.StringToValue(textVal, wxpg.PG_FULL_VALUE)

        if not res and value is None:
            res = True

        return (res, value)

    def SetValueToUnspecified(self, property, ctrl):
        """为未指明的对象赋值"""
        ctrl.Remove(0, len(ctrl.GetValue()))

    def SetControlStringValue(self, property, ctrl, text):
        """设置控件值"""
        ctrl.SetValue(text)

    def OnFocus(self, property, ctrl):
        """获取焦点"""
        ctrl.SetSelection(-1,-1)
