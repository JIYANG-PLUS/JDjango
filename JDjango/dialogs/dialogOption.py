import wx, json, glob, os, re
import wx.lib.buttons as buttons
from ..tools._tools import *
from .. settings import BASE_DIR

PATT_CHARS = re.compile(r'^[a-zA-Z_].*$')

class ConfigDialog(wx.Dialog):
    def __init__(self, parent, id, **kwargs):
        self.configs = get_configs(os.path.join(BASE_DIR, 'config.json'))
        self.DIRNAME = self.configs["dirname"]
        
        wx.Dialog.__init__(self, parent, id, '选项配置', size=(600, 400))

        panel = wx.Panel(self)
        vertical_box = wx.BoxSizer(wx.VERTICAL)
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)

        nm = wx.StaticBox(panel, -1, 'Django项目：')
        static_config_box = wx.StaticBoxSizer(nm, wx.VERTICAL)

        fn = wx.StaticText(panel, -1, "您的项目名称：") # 项目名称
        self.nm1 = wx.TextCtrl(panel, -1, style=wx.ALIGN_LEFT) # 输入框
        project_name = self.configs['project_name']
        self.nm1.SetValue(f"{project_name}")

        # 按钮
        self.first = wx.StaticText(panel, -1, "请先关闭所有占用此Django项目的程序。（否则会遇到修改权限问题）")
        self.modify = buttons.GenButton(panel, -1, label='修改（修改前请提前做好备份）')
        self.tip = wx.StaticText(panel, -1, "请确保您的项目名称在您整个项目中是独一无二的，否则本功能会严重破坏您的项目")

        horizontal_box.Add(fn, 0, wx.ALL | wx.CENTER, 5)
        horizontal_box.Add(self.nm1, 0, wx.ALL | wx.CENTER, 5)

        static_config_box.Add(horizontal_box, 0, wx.ALL | wx.CENTER, 10)

        vertical_box.Add(static_config_box, 0, wx.ALL | wx.CENTER, 5)
        vertical_box.Add(self.first, 0, wx.ALL | wx.CENTER, 5)
        vertical_box.Add(self.tip, 0, wx.ALL | wx.CENTER, 5)
        vertical_box.Add(self.modify, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(vertical_box)

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

class AppsCreateDialog(wx.Dialog):
    def __init__(self, parent, id, **kwargs):
        wx.Dialog.__init__(self, parent, id, '站点注册(简单配置)', size=(600, 400))

        self.font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False)

        # 面板
        panel = wx.Panel(self) # 最外层容器
        pathPanel = wx.Panel(panel) # 选择文件路径
        panel.SetBackgroundColour('#ededed')  # 最外层容器颜色

        # 按钮
        btn_select_file_path = buttons.GenButton(pathPanel, -1, label='选择admin.py文件')
        text_path = wx.TextCtrl(pathPanel, -1)
        text_path.SetFont(self.font)
        text_path.SetEditable(False)

        # 垂直布局 和 水平布局
        

    def ButtonClick(self, e):
        bId = e.GetId()
        