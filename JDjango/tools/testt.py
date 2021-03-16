import wx
import wx.adv
import wx.propgrid as wxpg

class TestPanel(wx.Panel):
    def __init__( self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)

        self.pgPanel = pgPanel = wxpg.PropertyGridManager(
            panel,
            style = wxpg.PG_SPLITTER_AUTO_CENTER
                | wxpg.PG_AUTO_SORT
                | wxpg.PG_TOOLBAR
        )

        pgPanel.ExtraStyle |= wxpg.PG_EX_HELP_AS_TOOLTIPS

        pgPanel.AddPage( "第一页" )

        ### 常用属性
        pgPanel.Append(wxpg.PropertyCategory("1 - 常用属性"))
        # 添加简单文本属性
        txtProp = pgPanel.Append(wxpg.StringProperty("文本", value="默认名称"))
        # 添加密码属性
        pwdProp = pgPanel.Append(wxpg.StringProperty('密码', value='请输入密码'))
        pwdProp.SetAttribute('Hint', 'This is a hint')
        pwdProp.SetAttribute('Password', True)
        # 添加整型属性
        intProp = pgPanel.Append(wxpg.IntProperty("整数", value=100))
        # 添加浮点型属性
        floatProp = pgPanel.Append(wxpg.FloatProperty("浮点型", value=123.456))
        # 添加布尔属性
        boolProp = pgPanel.Append(wxpg.BoolProperty("布尔", value=True))
        # 布尔属性复选框
        checkboxProp = pgPanel.Append(wxpg.BoolProperty("复选框", value=True))
        pgPanel.SetPropertyAttribute(checkboxProp, "UseCheckbox", True)
        # pgPanel.SetPropertyAttribute("复选框", "UseCheckbox", True) # 效果等同于上一句


        ### 更多属性
        pgPanel.Append(wxpg.PropertyCategory("2 - 更多属性"))
        # 多行长文本属性
        longstrProp = pgPanel.Append(wxpg.LongStringProperty("长文本", value="This is a\nmulti-line string\nwith\ttabs\nmixed\tin."))
        # 目录选择属性
        dirProp = pgPanel.Append(wxpg.DirProperty("目录", value=r""))
        # 文件选择属性
        fileProp = pgPanel.Append(wxpg.FileProperty("文件", value=r""))
        pgPanel.SetPropertyAttribute("文件", wxpg.PG_FILE_SHOW_FULL_PATH, 0) # 显示全路径
        pgPanel.SetPropertyAttribute("文件", wxpg.PG_FILE_INITIAL_PATH, r".") # 文件选择初始路径
        # 数组字符串属性
        arraystrProp = pgPanel.Append( wxpg.ArrayStringProperty("数组字符串", value=['A','B','C']) )
        # 枚举属性
        enumProp = pgPanel.Append(
            wxpg.EnumProperty("枚举", "枚举",
                [
                    '枚举1',
                    '枚举2',
                    '枚举3'
                ],
                [10, 11, 12],
                0
            )
        )
        # 可编辑枚举属性
        editenumProp = pgPanel.Append(
            wxpg.EditEnumProperty("可编辑枚举", "可编辑枚举",
                ['A', 'B', 'C'],
                [0, 1, 2],
                "文本不在列表中"
            )
        )


        ### 高级属性
        pgPanel.Append(wxpg.PropertyCategory("3 - 高级属性"))
        pgPanel.Append(wxpg.DateProperty("日期", value=wx.DateTime.Now()))
        pgPanel.SetPropertyAttribute("日期", wxpg.PG_DATE_PICKER_STYLE, wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY)
        pgPanel.Append(wxpg.FontProperty("字体", value=panel.GetFont()))
        pgPanel.Append(wxpg.ColourProperty("颜色", value=panel.GetBackgroundColour()))
        pgPanel.Append(wxpg.SystemColourProperty("系统颜色"))
        pgPanel.Append(wxpg.ImageFileProperty("图片"))
        pgPanel.Append(wxpg.MultiChoiceProperty("多选", choices=['多选1', '多选2', '多选+']))


        ### 附加属性
        pgPanel.Append(wxpg.PropertyCategory("4 - 附加属性"))
        pgPanel.Append(wxpg.IntProperty("整数上下调整", value=256))
        pgPanel.SetPropertyEditor("整数上下调整", "SpinCtrl")


        topsizer.Add(pgPanel, 1, wx.EXPAND | wx.ALL, 5)

        # 注册监听界面值改变事件
        pgPanel.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        pgPanel.Bind( wxpg.EVT_PG_PAGE_CHANGED, self.OnPropGridPageChange )
        pgPanel.Bind( wxpg.EVT_PG_SELECTED, self.OnPropGridSelect )
        pgPanel.Bind( wxpg.EVT_PG_RIGHT_CLICK, self.OnPropGridRightClick )

        # 适应主窗口
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def OnPropGridChange(self, event):
        """单元格值更新"""
        p = event.GetProperty()

    def OnPropGridPageChange(self, event):
        """页面值更新"""
        index = self.pgPanel.GetSelectedPage()

    def OnPropGridSelect(self, event):
        """单元格选中事件"""
        p = event.GetProperty()

    def OnPropGridRightClick(self, event):
        """单元格右击事件"""
        p = event.GetProperty()


class MainFrameGUI(wx.Frame):

    def __init__(self, parent = None):
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = "testt", pos = wx.DefaultPosition, size = wx.Size(960, 540), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
        panel = TestPanel(self)

class App(wx.App):

    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        self.frame = MainFrameGUI()
        self.frame.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

    def OnExit(self):
        return super().OnExit()

if __name__ == "__main__":
    app = App(redirect=False)
    app.MainLoop()