from .common import *

class SettingsPropertyPanel(wx.Panel):
    def __init__( self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.index1 = 1

        self._init_UI()
        self._init_data() # 初始化属性值

    def _init_UI(self):
        """初始化UI"""
        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)

        # 属性面板
        self.pgPanel = wxpg.PropertyGridManager(
            panel,
            style = wxpg.PG_BOLD_MODIFIED
                | wxpg.PG_SPLITTER_AUTO_CENTER
                | wxpg.PG_AUTO_SORT
                | wxpg.PG_TOOLBAR
                | wxpg.PG_DESCRIPTION
                | wxpg.PGMAN_DEFAULT_STYLE
        )
        topsizer.Add(self.pgPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.pgPanel.ExtraStyle |= wxpg.PG_EX_HELP_AS_TOOLTIPS
        self._init_pages() # 初始化第一个子面板
        # self.pgPanel.ShowHeader()
        self.pgPanel.SetDescBoxHeight(40)

        # 工具面板
        self.toolsPanel = wx.Panel(self.panel)
        self.toolsPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.toolsPanel.SetSizer(self.toolsPanelSizer)
        topsizer.Add(self.toolsPanel, 0, wx.EXPAND | wx.ALL, 5)

        self._init_tools()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def _init_data(self):
        """初始化属性值"""
        attrDatas = self.pgPanel.GetPropertyValues(inc_attributes=True)
        CONFIGS = get_configs(CONFIG_PATH)
        for k, v in CONFIGS.items():
            if k in attrDatas:
                attrDatas[k] = pros.transfer_value(k, v)
        self.pgPanel.SetPropertyValues(attrDatas)

    def _init_tools(self):
        """初始化工具面板"""
        self.btn_save_value = buttons.GenButton(self.toolsPanel, -1, label='保存修改')
        self.toolsPanelSizer.Add(self.btn_save_value, 1, wx.EXPAND | wx.ALL, 1)

        # 事件监听
        self.Bind(wx.EVT_BUTTON, self.onBtnSaveValue, self.btn_save_value)

    def onBtnSaveValue(self, e):
        """保存设置属性"""
        self.DIRSETTINGS = os.path.join(djangotools.SCONFIGS.dirname(), djangotools.SCONFIGS.project_name(), 'settings.py')
        DATA_SETTINGS = self.pgPanel.GetPropertyValues(inc_attributes=True)
        try:
            CONFIGS = get_configs(CONFIG_PATH)
            content_settings = read_file(self.DIRSETTINGS)
            temp = content_settings
            if None != DATA_SETTINGS.get('DEBUG'):
                temp = retools.patt_sub_only_capture_obj(retools.PATT_DEBUG, DATA_SETTINGS['DEBUG'], temp)
            if None != DATA_SETTINGS.get('USE_I18N'):
                temp = retools.patt_sub_only_capture_obj(retools.PATT_USE_I18N, DATA_SETTINGS['USE_I18N'], temp)
            if None != DATA_SETTINGS.get('USE_L10N'):
                temp = retools.patt_sub_only_capture_obj(retools.PATT_USE_L10N, DATA_SETTINGS['USE_L10N'], temp)
            if None != DATA_SETTINGS.get('USE_TZ'):
                temp = retools.patt_sub_only_capture_obj(retools.PATT_USE_TZ, DATA_SETTINGS['USE_TZ'], temp)
            if None != DATA_SETTINGS.get('CORS_ORIGIN_ALLOW_ALL'):
                temp = retools.patt_sub_only_capture_obj(retools.PATT_CORS_ORIGIN_ALLOW_ALL, DATA_SETTINGS['CORS_ORIGIN_ALLOW_ALL'], temp)
            if None != DATA_SETTINGS.get('X_FRAME_OPTIONS'):
                if DATA_SETTINGS['X_FRAME_OPTIONS']: # 开启
                    if not CONFIGS['X_FRAME_OPTIONS']: # 且原文件不存在
                        write_file(self.DIRSETTINGS, temp) # 即时写入
                        append_file(self.DIRSETTINGS, ["X_FRAME_OPTIONS = 'ALLOWALL'"])
                        temp = read_file(self.DIRSETTINGS) # 刷新
                else: # 关闭（删除）
                    temp = retools.PATT_X_FRAME_OPTIONS.sub('', temp)
            if None != DATA_SETTINGS.get('LANGUAGE_CODE'):
                re_str = pros.get_realname_by_readname('LANGUAGE_CODE', DATA_SETTINGS['LANGUAGE_CODE'])
                temp = retools.patt_sub_only_capture_obj(retools.PATT_LANGUAGE_CODE, re_str, temp)
            if None != DATA_SETTINGS.get('TIME_ZONE'):
                re_str = pros.get_realname_by_readname('TIME_ZONE', DATA_SETTINGS['TIME_ZONE'])
                temp = retools.patt_sub_only_capture_obj(retools.PATT_TIME_ZONE, re_str, temp)
            # 写入SECRET_KEY和HOST
            host_contents = [f"'{_}'" for _ in DATA_SETTINGS['ALLOWED_HOSTS'] if _]
            temp = retools.patt_sub_only_capture_obj_obtain_double(retools.PATT_ALLOWED_HOSTS, ','.join(host_contents), temp)

            write_file(self.DIRSETTINGS, temp) # 更新settings.py文件

            # 跨域中间件介入
            if 'True' == DATA_SETTINGS.get('CORS_ORIGIN_ALLOW_ALL'): # 开启时写入中间件
                # 检测是否正确配置虚拟环境
                if not self._check_env_exist:
                    wx.MessageBox(f'虚拟环境未绑定，或绑定失败！（仅跨域请求更新失败）', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
                    return
                djangotools.add_oneline_to_listattr(self.DIRSETTINGS, retools.PATT_MIDDLEWARE, COR_MIDDLEWARE)
                
                module_name = 'django-cors-headers'
                import subprocess
                env_python3_pip = os.path.join(os.path.dirname(env.getPython3Env()), 'pip')
                subprocess.Popen(f'{env_python3_pip} install {module_name}', shell=True) # 开进程，安装必须库
            else:
                djangotools.pop_oneline_to_listattr(self.DIRSETTINGS, retools.PATT_MIDDLEWARE, COR_MIDDLEWARE)

            djangotools.refresh_config() # 更新配置文件【重要且必须！！！】

            DATA_SETTINGS = {} # 防止重复确定，重要！！！
        except Exception as e:
            print(e)
            wx.MessageBox(f'错误，配置文件已损坏。', '错误', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(f'修改成功！', '成功', wx.OK | wx.ICON_INFORMATION)

    def _init_pages(self):
        """初始化所有配置页"""
        for thispage in pros.PROPERTY_CONFIGS:
            page = self.pgPanel.AddPage(thispage["page-name"])
            for category in thispage["categorys"]:
                self.AppendCategoryAuto(page, category["name"])
                for obj in category["objs"]:
                    self._append_category_obj(page, obj)

    def _append_category_obj(self, page, obj):
        """添加选项"""
        pro_type = obj["type"].lower()
        if 'EnumProperty'.lower() == pro_type: # 枚举类型
            page.Append(wxpg.EnumProperty(obj["key"], obj["key"],
                obj["labels"], obj["choices"], obj["default"]
            ))
        elif 'StringProperty'.lower() == pro_type: # 字符类型
            page.Append(wxpg.StringProperty(obj["key"], value=obj["default"]))
        elif 'ArrayStringProperty'.lower() == pro_type: # 字符数组类型
            page.Append(wxpg.ArrayStringProperty(obj["key"], value=obj["default"]))
        elif 'BoolProperty'.lower() == pro_type: # 布尔类型
            page.Append(wxpg.BoolProperty(obj["key"], value=obj["default"]))
        elif 'IntProperty'.lower() == pro_type: # 整型
            page.Append(wxpg.IntProperty(obj["key"], value=obj["default"]))
        elif 'FileProperty'.lower() == pro_type: # 文件路径
            page.Append(wxpg.FileProperty(obj["key"], value=obj["default"]))
            page.SetPropertyAttribute(obj["key"], wxpg.PG_FILE_SHOW_FULL_PATH, 0) # 显示全路径
            page.SetPropertyAttribute(obj["key"], wxpg.PG_FILE_INITIAL_PATH, r".") # 文件选择初始路径

    def AppendCategoryAuto(self, page, cate_name):
        """二次封装，自动加序号"""
        page.Append(wxpg.PropertyCategory(f"{self.index1}、{cate_name}"))
        self.index1 += 1

    @property
    def _check_env_exist(self)->bool:
        """检测虚拟环境是否存在"""
        env_path = env.getPython3Env()
        if '' == env_path.strip() or not os.path.exists(env_path):
            return False
        return True
