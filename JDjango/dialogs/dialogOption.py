import wx, json, glob, os, re
import wx.lib.buttons as buttons
from ..tools._tools import *
from .. settings import BASE_DIR, CONFIG_PATH, CONFIG_PATH

PATT_CHARS = re.compile(r'^[a-zA-Z_].*$')

class ConfigDialog(wx.Dialog):
    def __init__(self, parent, id, **kwargs):
        self.configs = get_configs(os.path.join(BASE_DIR, 'config.json'))
        self.DIRNAME = self.configs["dirname"]
        
        wx.Dialog.__init__(self, parent, id, '选项配置', size=(600, 400))

        self.panel = wx.Panel(self)
        vertical_box = wx.BoxSizer(wx.VERTICAL)
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)

        nm = wx.StaticBox(self.panel, -1, 'Django项目：') # 带边框的盒子
        static_config_box = wx.StaticBoxSizer(nm, wx.VERTICAL) # 垂直布局

        fn = wx.StaticText(self.panel, -1, "您的项目名称：") # 项目名称
        self.nm1 = wx.TextCtrl(self.panel, -1, style=wx.ALIGN_LEFT) # 输入框
        project_name = self.configs['project_name']
        self.nm1.SetValue(f"{project_name}")

        # 按钮
        self.first = wx.StaticText(self.panel, -1, "请先关闭所有占用此Django项目的程序。（否则会遇到修改权限问题）")
        self.modify = buttons.GenButton(self.panel, -1, label='修改（修改前请提前做好备份）')
        self.tip = wx.StaticText(self.panel, -1, "请确保您的项目名称在您整个项目中是独一无二的，否则本功能会严重破坏您的项目")

        horizontal_box.Add(fn, 0, wx.ALL | wx.CENTER, 5)
        horizontal_box.Add(self.nm1, 0, wx.ALL | wx.CENTER, 5)

        static_config_box.Add(horizontal_box, 0, wx.ALL | wx.CENTER, 10)

        vertical_box.Add(static_config_box, 0, wx.ALL | wx.CENTER, 5)
        vertical_box.Add(self.first, 0, wx.ALL | wx.CENTER, 5)
        vertical_box.Add(self.tip, 0, wx.ALL | wx.CENTER, 5)
        vertical_box.Add(self.modify, 0, wx.ALL | wx.CENTER, 5)

        self.panel.SetSizer(vertical_box)

        # 事件绑定
        self.Bind(wx.EVT_BUTTON, self.ButtonClick, self.modify)

    def ButtonClick(self, e):
        bId = e.GetId()
        if bId == self.modify.GetId():
            # 获取新的名称
            old_name = self.configs['project_name']
            new_name = self.nm1.GetValue().strip()

            if old_name == new_name:
                dlg = wx.MessageDialog( self, "未做任何修改", "警告", wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
                return

            if not PATT_CHARS.match(new_name):
                dlg = wx.MessageDialog( self, "请使用字母+下划线的方式命名", "错误", wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
                return

            # 重命名项目（先文件，后目录）
            search_path = os.path.join(self.DIRNAME, '**', '*')
            alls = glob.glob(search_path, recursive=True)

            # 分类文件和文件夹
            files, floders = [], []
            for _ in alls:
                if os.path.isfile(_): files.append(_)
                else: floders.append(_)

            for p in files:
                # 先读后写
                if '.py' == os.path.splitext(p)[1]:
                    content = read_file(p)
                    content = content.replace(old_name.strip(), new_name)
                    write_file(p, content)

            for P in floders:
                if old_name.strip().lower() == os.path.basename(P).strip().lower():
                    temp = os.path.join(os.path.dirname(P), new_name)
                    os.rename(P, temp)

            # 修改根目录名称
            os.rename(self.DIRNAME, os.path.join(os.path.dirname(self.DIRNAME), new_name))
            
            dlg = wx.MessageDialog( self, "修改成功，请退出所有窗口后重新打开，进行后续操作。", "成功", wx.OK)
            if dlg.ShowModal() == wx.ID_OK:
                self.Close(True)
            dlg.ShowModal()
            dlg.Destroy()

class AdminCreateSimpleDialog(wx.Dialog):
    def __init__(self, parent, id, **kwargs):
        wx.Dialog.__init__(self, parent, id, '站点注册(简单配置)', size=(600, 400))

        self.font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False)
        self.hideObjs = []

        # 面板
        self.panel = wx.Panel(self) # 最外层容器
        self.pathPanel = wx.Panel(self.panel) # 选择应用程序app
        self.panel.SetBackgroundColour('#ededed')  # 最外层容器颜色
        self.pathPanel.SetBackgroundColour('#ededed')
        # self.scroller = wx.ScrolledWindow(self.panel, -1)
        # self.scroller.SetScrollbars(1, 1, 600, -1)
        self.modelPanel = wx.Panel(self.panel) # 选择模型列表

        # 向 self.pathPanel 填充控件
        # self.btn_select_file_path = buttons.GenButton(self.pathPanel, -1, label='选择admin.py文件')
        # self.text_path = wx.TextCtrl(self.pathPanel, -1)
        # self.text_path.SetFont(self.font)
        # self.text_path.SetEditable(False)
        apps = get_configs(CONFIG_PATH)['app_names']
        self.infoChoiceApp = wx.StaticText(self.pathPanel, -1, "选择要注册的应用程序：")
        self.infoChoiceApp.SetFont(self.font)
        self.choiceApp = wx.Choice(self.pathPanel, -1, choices = apps, style = wx.CB_SORT) # 复选框

        # 静态框里的复选框
        self.checkbox1 = wx.CheckBox(self.modelPanel, -1, "全选")
        self.checkbox2 = wx.CheckBox(self.modelPanel, -1, "选项1")
        self.checkbox3 = wx.CheckBox(self.modelPanel, -1, "选项2")
        self.checkbox4 = wx.CheckBox(self.modelPanel, -1, "选项3")
        self.hideObjs.extend([
            self.checkbox1
            , self.checkbox2
            , self.checkbox3
            , self.checkbox4
        ])

        # 区域静态框
        staticBox = wx.StaticBox(self.modelPanel, -1, '选择在后台显示的模型对象：') # 带边框的盒子

        # 确认注册按钮
        self.btn_register = buttons.GenButton(self.panel, -1, label='确认注册')
        self.btn_register.Enable(False)
        
        # 垂直布局 和 水平布局
        panelBox = wx.BoxSizer(wx.VERTICAL)
        pathPanelBox = wx.BoxSizer(wx.HORIZONTAL) # 选择app布局
        self.staticAreaBox = wx.StaticBoxSizer(staticBox, wx.VERTICAL) # 中间实线括起部分布局
        self.staticAreaBox_1 = wx.BoxSizer(wx.HORIZONTAL) # 存放 Models


        # 复选框 【后期从真正的model文件中读取】
        self.staticAreaBox_1.Add(self.checkbox1, 0, wx.LEFT, 5)
        self.staticAreaBox_1.Add(self.checkbox2, 0, wx.LEFT, 5)
        self.staticAreaBox_1.Add(self.checkbox3, 0, wx.LEFT, 5)
        self.staticAreaBox_1.Add(self.checkbox4, 0, wx.LEFT, 5)
        self.staticAreaBox_1.Add(wx.CheckBox(self.modelPanel, -1, "选项"), 0, wx.LEFT, 5)
        self.staticAreaBox_1.Add(wx.CheckBox(self.modelPanel, -1, "选项"), 0, wx.LEFT, 5)
        self.staticAreaBox_1.Add(wx.CheckBox(self.modelPanel, -1, "选项"), 0, wx.LEFT, 5)
        self.staticAreaBox_1.Add(wx.CheckBox(self.modelPanel, -1, "选项"), 0, wx.LEFT, 5)
        self.staticAreaBox_1.Add(wx.CheckBox(self.modelPanel, -1, "选项"), 0, wx.LEFT, 5)
        self.staticAreaBox_1.Add(wx.CheckBox(self.modelPanel, -1, "选项"), 0, wx.LEFT, 5)
        self.staticAreaBox_1.Add(wx.CheckBox(self.modelPanel, -1, "选项"), 0, wx.LEFT, 5)
        self.staticAreaBox_1.Add(wx.CheckBox(self.modelPanel, -1, "选项"), 0, wx.LEFT, 5)
        self.staticAreaBox_1.Add(wx.CheckBox(self.modelPanel, -1, "选项"), 0, wx.LEFT, 5)
        self.staticAreaBox_1.Add(wx.CheckBox(self.modelPanel, -1, "选项"), 0, wx.LEFT, 5)
        self.staticAreaBox_1.Add(wx.CheckBox(self.modelPanel, -1, "选项"), 0, wx.LEFT, 5)
        self.staticAreaBox_1.Add(wx.CheckBox(self.modelPanel, -1, "选项nnn"), 0, wx.LEFT, 5)
        self.staticAreaBox.Add(self.staticAreaBox_1, 0, wx.LEFT, 10)

        # 路径选择填充
        # pathPanelBox.Add(self.text_path, 1, wx.EXPAND | wx.ALL, 2)
        # pathPanelBox.Add(self.btn_select_file_path, 0, wx.EXPAND | wx.ALL, 2)
        pathPanelBox.Add(self.infoChoiceApp, 0, wx.EXPAND | wx.ALL, 6)
        pathPanelBox.Add(self.choiceApp, 1, wx.EXPAND | wx.ALL, 6)

        # 最外层容器填充（从上往下）
        panelBox.Add(self.pathPanel, 0, wx.EXPAND | wx.ALL, 3)
        panelBox.Add(self.modelPanel, 0, wx.EXPAND | wx.ALL, 3)
        panelBox.Add(self.btn_register, 0, wx.EXPAND | wx.ALL, 3)

        # 面板绑定布局
        self.pathPanel.SetSizer(pathPanelBox)
        self.modelPanel.SetSizer(self.staticAreaBox)
        self.panel.SetSizer(panelBox)

        # 注册事件
        self.Bind(wx.EVT_CHOICE, self.ChoiceClick, self.choiceApp) # 下拉列表值更新
        # self.Bind(wx.EVT_BUTTON, self.ButtonClick, self.btn_select_file_path)
        self.Bind(wx.EVT_BUTTON, self.ButtonClick, self.btn_register) # 注册按钮

        # 初始化控件状态
        self._hide_all()

    def ChoiceClick(self, e):
        key = e.GetString()
        self.checkbox2.Enable(True)
        self.modelPanel.Refresh()
        self.pathPanel.Refresh()
        self.panel.Refresh()

    def _hide_all(self):
        for _ in self.hideObjs:
            # _.Hide()
            _.Enable(False)

    def ButtonClick(self, e):
        """界面按钮点击事件"""
        bId = e.GetId()
        # if bId == self.btn_select_file_path.GetId(): # 选择admin.py所在路径
        #     self.select_adminpy(e)
        if bId == self.btn_register.GetId():
            self.onRegister(e)

    def onRegister(self, e):
        ...


    def select_adminpy(self, e):
        """获取admin.py文件所在路径"""
        path = get_configs(CONFIG_PATH)['dirname']
        dlg = wx.FileDialog(self, "选择admin.py文件", path, "", "*.py", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            # 待校验：是否是当前项目下的admin.py文件
            self.dirname = dlg.GetDirectory()
            if 'admin.py' == filename:
                self.text_path.SetValue(f'{self.dirname}')
            else:
                pass
        else:
            pass
        dlg.Destroy()
