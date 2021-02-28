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

    def _set_fonts(self, e):
        """统一设置字体"""
        '''
            统一设置字体
        '''
        font = wx.Font(env.getFontSize(), wx.SWISS, wx.NORMAL, wx.BOLD, False)
        for _ in self.needFonts:
            _.SetFont(font)

        '''
            单独控制的字体
        '''
        self.cmdTip.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False))

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

    def _init_config(self):
        """初始化配置文件"""
        configs = {} # 全局配置文件待写入
        # 必要前缀赋值
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

        settings = {}
        with open(self.path_settings, 'r', encoding='utf-8') as f:
            text = PATT_BASE_DIR.sub('', f.read())
            exec(f"BASE_DIR = r'{self.dirname}'", {}, settings)
            exec(text, {}, settings)

        configs['DATABASES'] = settings.get('DATABASES') # 数据库
        configs['DEBUG'] = settings.get("DEBUG") # 调试状态
        configs['LANGUAGE_CODE'] = settings.get("LANGUAGE_CODE") # 语言环境
        configs['TIME_ZONE'] = settings.get("TIME_ZONE") # 时区
        configs['USE_I18N'] = settings.get("USE_I18N") # 全局语言设置
        configs['USE_L10N'] = settings.get("USE_L10N")
        configs['USE_TZ'] = settings.get("USE_TZ") # 是否使用标准时区
        configs['STATIC_URL'] = settings.get("STATIC_URL") # 静态文件路径
        configs['ALLOWED_HOSTS'] = settings.get("ALLOWED_HOSTS") # 允许连接ip
        configs['X_FRAME_OPTIONS'] = settings.get("X_FRAME_OPTIONS") # 是否开启iframe
        configs['SECRET_KEY'] = settings.get("SECRET_KEY") # SECRET_KEY
        configs['CORS_ORIGIN_ALLOW_ALL'] = settings.get("CORS_ORIGIN_ALLOW_ALL") # 跨域
        temp_templates_app = settings.get("TEMPLATES")
        if temp_templates_app and len(temp_templates_app) > 0:
            try:
                configs['TEMPLATES_APP_DIRS'] = temp_templates_app[0]['APP_DIRS'] # 是否开启应用程序模板文件路径
                configs['TEMPLATES_DIRS'] = temp_templates_app[0]['DIRS'] # 默认模板路径
            except:
                configs['TEMPLATES_APP_DIRS'] = None
                configs['TEMPLATES_DIRS'] = None # 默认模板路径
        else:
            configs['TEMPLATES_APP_DIRS'] = None
            configs['TEMPLATES_DIRS'] = None # 默认模板路径

        
        dump_json(CONFIG_PATH, configs)  # 写入配置文件
