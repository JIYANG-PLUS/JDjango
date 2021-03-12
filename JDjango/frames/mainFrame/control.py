from .gui import *

"""
作用：实现控件可见性可用性的控制
"""

class MainFrameGUIControl(MainFrameGUI):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._disable_all_btn() # 统一设置按钮不可用状态
        self._set_fonts(None) # 字体控制
        self._control_able() # 可见性、可用性控制

    def _disable_all_btn(self):
        """关闭所有按钮权限"""
        for a in self.allInitBtns:
            for b in self.allInitBtns[a]:
                for _ in self.allInitBtns[a][b]:
                    _.Enable(False)

    def _control_able(self):
        """可见性、可用性控制"""
        self.infos.SetEditable(False)
        self.path.SetEditable(False)
        self.portProgressRun.Enable(False)
        self.portProgressStop.Enable(False)

        # 锁定 工具栏 停止按钮
        self.sys_toolbar.EnableTool(self.shotcut_run.GetId(), False)
        self.sys_toolbar.EnableTool(self.shotcut_stop.GetId(), False)

    def _set_fonts(self, e):
        """统一设置字体"""
        font = wx.Font(env.getFontSize(), wx.SWISS, wx.NORMAL, wx.BOLD, False)
        for _ in self.needFonts:
            _.SetFont(font)

    def _open_all_check_btn(self):
        """ 开启所有检测按钮权限 """
        for a in self.allInitBtns:
            for _ in self.allInitBtns[a]["check"]:
                _.Enable(True)

    def _open_checked_fix_btn(self, model, f_type = 'open'):
        """开启通过检测的修复按钮"""
        if 'open' == f_type:
            self.needfix.add(model)
        switch = True if 'open' == f_type else False
        for _ in self.allInitBtns[model][CON_CONTROL_FIX]:
            _.Enable(switch)
        # 开启/关闭全局的修复按钮【一键修复】
        if len(self.needfix) > 0:
            for _ in self.allInitBtns['global'][CON_CONTROL_FIX]:
                _.Enable(True) # 需要修复时开启，否则关闭
        else:
            for _ in self.allInitBtns['global'][CON_CONTROL_FIX]:
                _.Enable(False)

    def _open_part_necessary_btns(self):
        """开启部分必要的、控制流程之外的按钮"""
        for a in self.allInitBtns:
            for _ in self.allInitBtns[a][CON_CONTROL_CREATE]:
                _.Enable(True) # 开启所有的创建按钮
                
        self.modelsProxyGenerate.Enable(False) # 代理模型 功能暂未实现，待实现后去掉此行代码
        self.btn_config_project.Enable(True) # 选项
        self.menusSettings.Enable(True) # Settings

        if self.platform_name.lower() in env.getSupportEnvPlatform(): # 平台限制
            self.portProgressRun.Enable(True) # 运行
            self.sys_toolbar.EnableTool(self.shotcut_run.GetId(), True)

    def _init_config(self):
        """初始化配置文件"""
        configs = {} # 全局配置文件待写入

        configs['dirname'] = self.dirname # 项目路径
        configs['project_name'] = os.path.basename(self.dirname) # 项目名称
        apps = os.listdir(self.dirname) # 所有的应用程序（包含主程序）

        try:
            apps.remove(configs['project_name']) # 移除主程序
        except:
            self.infos.AppendText(out_infos('项目残缺，无法校验。请检查本项目是否为Django项目。', level=3))
            return

        configs['app_names'] = [_ for _ in apps if os.path.exists(os.path.join(self.dirname, _, 'migrations'))] # 以迁移目录为依据进行筛选
        self.path_settings = os.path.join(self.dirname, configs['project_name'], 'settings.py')

        try:
            assert os.path.exists(self.path_settings)
        except Exception as e:
            self.infos.AppendText(out_infos('项目残缺，无法校验。请检查本项目是否为Django项目。', level=3))
            return
        else:
            set_configs(self.path_settings, configs) # 第三个参数测试用
            dump_json(CONFIG_PATH, configs)  # 写入配置文件
