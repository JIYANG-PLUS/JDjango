from .common import *
from .ShowEnvPipListPanel import *

class PipListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID=-1,  pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

class PipListCtrlPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.datas = None # 全局数据索引
        self.cmdCodes = [] # 指令容器

        self._init_UI()
        self._init_listener()

        # 开启定时器
        self.timer = wx.PyTimer(self.onNotify)
        self.timer.Start(1000, wx.TIMER_CONTINUOUS)
        self.onNotify()

    def onNotify(self):
        """定时器，每隔一秒检测"""
        # 监听指令
        for i, t_code in enumerate(self.cmdCodes[::-1]):
            try:
                if (None != t_code[1].poll()):
                    op_str = ""
                    if "U" == t_code[0]: op_str = "更新"
                    elif "UI" == t_code[0]: op_str = "卸载"
                    else: op_str = "安装"

                    self.infoBar.ShowMessage(f"{t_code[2]}{op_str}成功，请刷新状态查看最新的安装包状态。", wx.ICON_INFORMATION)
                    self.cmdCodes.pop(i) # 已经完成的命令进行移除
                    if "U" == t_code[0]: # 如果是更新状态，将本地文件顺带更新
                        # 只要是本地文件列表有的，均更新
                        p = subprocess.Popen(f'{env.getPipOrderArgs(mode="freeze")}', shell=True, stdout=subprocess.PIPE)
                        out, err = p.communicate()
                        if err:
                            self.infoBar.ShowMessage("环境异常，请稍后再试。", wx.ICON_ERROR)
                            return
                        with open(PIPS_PATH, encoding="utf-8") as f:
                            pips = json.load(f)
                            for o in out.splitlines():
                                temp = o.decode(encoding='utf-8').strip().split('==')
                                pip_name, version = temp[0], temp[-1]
                                for pip in pips:
                                    if pip_name.lower() == pip["name"].lower():
                                        pip["version"] = version # 版本更新
                                        pip["freeze_name"] = [f"{temp[0]}=={temp[-1]}",]
                                        break
                        with open(PIPS_PATH, "w", encoding="utf-8") as f:
                            json.dump(pips, f, indent=4, ensure_ascii=False)
            except:
                self.infoBar.ShowMessage("异常错误，请联系作者解决。", wx.ICON_ERROR)

    def _init_UI(self):

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.SetBackgroundColour(CON_COLOR_MAIN)

        self.panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(topsizer)
        topsizer.SetSizeHints(self.panel)
        sizer.Add(self.panel, 1, wx.EXPAND)

        '''
            简单工具栏
        '''
        self.toolPanel = wx.Panel(self.panel)
        toolPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.toolPanel.SetSizer(toolPanelSizer)
        topsizer.Add(self.toolPanel, 0, wx.EXPAND | wx.ALL, 0)

        self.btnShowAllPips = buttons.GenButton(self.toolPanel, -1, label='查看虚拟环境所有安装包', name='newView')
        toolPanelSizer.Add(self.btnShowAllPips, 0, wx.EXPAND | wx.ALL, 0)

        self.btnSelectEnv = buttons.GenButton(self.toolPanel, -1, label='绑定虚拟环境')
        toolPanelSizer.Add(self.btnSelectEnv, 0, wx.EXPAND | wx.ALL, 0)

        self.btnRefresh = buttons.GenButton(self.toolPanel, -1, label='状态刷新')
        toolPanelSizer.Add(self.btnRefresh, 0, wx.EXPAND | wx.ALL, 0)

        '''
            列表控件
        '''
        self.imageList = wx.ImageList(24, 24) # 图像
        self.idx1 = self.imageList.Add(wx.Icon(BITMAP_LIST_FIT_PATH))
        self.pipListCtrl = PipListCtrl(self.panel,
            style=wx.LC_REPORT
            | wx.BORDER_SUNKEN
            # | wx.BORDER_NONE
            | wx.LC_EDIT_LABELS
            # | wx.LC_SORT_ASCENDING
            # | wx.LC_NO_HEADER
            | wx.LC_VRULES
            | wx.LC_HRULES
            # | wx.LC_SINGLE_SEL
        )
        # self.pipListCtrl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        topsizer.Add(self.pipListCtrl, 1, wx.EXPAND | wx.ALL, 0)
        self.pipListCtrl.SetImageList(self.imageList, wx.IMAGE_LIST_SMALL)
        # self.pipListCtrl.EnableCheckBoxes()

        self._init_list_column_name()
        self._init_list_data()

        '''
            通知栏
        '''
        self.infoBar = wx.InfoBar(self.panel)
        topsizer.Add(self.infoBar, 0, wx.EXPAND)

        '''
            简单的提示信息
        '''
        staticText = wx.StaticText(self.panel, -1, "（右击操作三方库）任何更新操作，将从本地抓取已安装的库，刷新本界面所有版本号。", size=(-1, -1))
        staticText.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        staticText.SetForegroundColour(wx.WHITE)
        topsizer.Add(staticText, 0, wx.EXPAND | wx.ALL, 0)

    def _init_listener(self):
        """注册监听"""
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected, self.pipListCtrl)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onItemDeselected, self.pipListCtrl)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onItemActivated, self.pipListCtrl)
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.onItemDelete, self.pipListCtrl)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.onColClick, self.pipListCtrl)
        self.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.onColRightClick, self.pipListCtrl)
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.onColBeginDrag, self.pipListCtrl)
        self.Bind(wx.EVT_LIST_COL_DRAGGING, self.onColDragging, self.pipListCtrl)
        self.Bind(wx.EVT_LIST_COL_END_DRAG, self.onColEndDrag, self.pipListCtrl)
        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.onBeginEdit, self.pipListCtrl)
        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.onEndEdit, self.pipListCtrl)
        self.pipListCtrl.Bind(wx.EVT_LEFT_DCLICK, self.onDoubleClick)
        self.pipListCtrl.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
        self.pipListCtrl.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.onRightClick)
        self.pipListCtrl.Bind(wx.EVT_RIGHT_UP, self.onRightClick)

        '''
            按钮监听
        '''
        self.Bind(wx.EVT_BUTTON, self.onBtnRefresh, self.btnRefresh)
        self.Bind(wx.EVT_BUTTON, self.onBtnSelectEnv, self.btnSelectEnv)
        self.Bind(wx.EVT_BUTTON, self.onBtnShowAllPips, self.btnShowAllPips)

    def _init_list_column_name(self):
        """初始化列表页标题"""
        columns = [
            ("三方库名", wx.LIST_FORMAT_LEFT, 260),
            ("版本号", wx.LIST_FORMAT_CENTRE, 100),
            ("安装状态", wx.LIST_FORMAT_CENTRE, 150),
            ("检测安装依据", wx.LIST_FORMAT_LEFT, 200),
            ("描述说明", wx.LIST_FORMAT_LEFT, wx.LIST_AUTOSIZE),
        ]

        for i, _ in enumerate(columns):
            self._insert_column(i, *_)

    def _insert_column(self, index, name, style=wx.LIST_FORMAT_CENTRE, width=wx.LIST_AUTOSIZE):
        """自动插入列"""
        temp_items = wx.ListItem()
        if 0 == index:
            temp_items.Mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
            temp_items.Image = -1
        temp_items.Align = style
        temp_items.Width = width
        temp_items.Text = name
        self.pipListCtrl.InsertColumn(index, temp_items)

        # self.pipListCtrl.InsertColumn(index, name, style)
        # self.pipListCtrl.SetColumnWidth(index, width)

    def _init_list_data(self):
        """初始化列表数据"""
        with open(PIPS_PATH, encoding='utf-8') as f:
            datas = json.load(f)
        
        self.datas = datas # 后备使用

        for i, data in enumerate(datas):
            item = self.pipListCtrl.InsertItem(self.pipListCtrl.GetItemCount(), data['name'], self.idx1)
            self.pipListCtrl.SetItem(item, 1, data['version'])
            self.pipListCtrl.SetItem(item, 2, "installed" if data['ispip'] else "uninstall")
            self.pipListCtrl.SetItem(item, 3, '、'.join(data['freeze_name']))
            self.pipListCtrl.SetItem(item, 4, data['description'])
            self.pipListCtrl.SetItemData(item, i)
            self.pipListCtrl.SetItemFont(item, wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD, False))
            if data['ispip']: # 安装过的三方库高亮显示
                self.pipListCtrl.SetItemTextColour(item, wx.BLUE)

    def onItemSelected(self, e):
        """分录点击事件"""
        self.currentItem = e.Index # 记录点击行

    def onItemActivated(self, e):
        """行激活"""
        self.currentItem = e.Index

    @VirtualEnvMustExistDecorator()
    def onBtnShowAllPips(self, e):
        """展示出所有的虚拟环境安装列表"""
        subFrame = wx.Frame(None, title="虚拟环境安装包列表", size=(600,400))
        ShowEnvPipListPanel(subFrame)
        # btn = subFrame.FindWindowByName("newView")
        # btn.Disable()
        subFrame.Show()

    def onBtnSelectEnv(self, e):
        """选择虚拟环境"""
        dlg = wx.FileDialog(self, "选择虚拟环境下的python.exe文件", "", "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            env.setPython3Env(os.path.join(dlg.GetDirectory(), dlg.GetFilename()))
            wx.MessageBox(f'虚拟环境绑定成功！', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
        dlg.Close(True)

    @VirtualEnvMustExistDecorator()
    def onBtnRefresh(self, e):
        """刷新状态"""
        
        p = subprocess.Popen(f'{env.getPipOrderArgs(mode="freeze")}', shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()
        if err:
            RichMsgDialog.showOkMsgDialog(self, "发生未知错误，请稍后重试", '错误')
            return

        with open(PIPS_PATH, encoding='utf-8') as f:
            PIPS_DATA = json.load(f)
            freeze_datas = set([_.decode(encoding='utf-8').strip().lower() for _ in out.splitlines()])
            for _ in PIPS_DATA:
                check_str = f'{_["name"]}=={_["version"]}'
                if check_str.lower() in freeze_datas:
                    _["ispip"] = True
                else:
                    _["ispip"] = False

        with open(PIPS_PATH, 'w', encoding='utf-8') as f:
            json.dump(PIPS_DATA, f, indent=4, ensure_ascii=False)

        self.pipListCtrl.DeleteAllItems()
        self._init_list_data()

        RichMsgDialog.showOkMsgDialog(self, "当前列表状态已刷新", '成功')

    def onRightClick(self, e):
        """右击行事件"""
        x, y = e.GetX(), e.GetY() # 列、行
        item, flags = self.pipListCtrl.HitTest((x, y))
        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
            self.pipListCtrl.Select(item) # 此处触发 onItemSelected 事件

        if -1 == item:
            return

        try:
            col, row, width, height = self.pipListCtrl.GetItemRect(item)
        except:
            return
        else:
            col_min, col_max = col, col+width
            row_min, row_max = row, row+height
            if not ((col_min <= x <= col_max) and (row_min <= y <= row_max)):
                return # 空白处不允许右击

        self.popup_install_ID = wx.NewIdRef()
        self.popup_uninstall_ID = wx.NewIdRef()
        self.popup_install_upgrade_ID = wx.NewIdRef()
        self.popup_install_info_ID = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.onPopupInstall, id=self.popup_install_ID)
        self.Bind(wx.EVT_MENU, self.onPopupUnInstall, id=self.popup_uninstall_ID)
        self.Bind(wx.EVT_MENU, self.onPopupInstallUpgrade, id=self.popup_install_upgrade_ID)
        self.Bind(wx.EVT_MENU, self.onPopupInstallInfo, id=self.popup_install_info_ID)

        menu = wx.Menu()
        menu.Append(self.popup_install_ID, "安装/注册（pip install）")
        menu.Append(self.popup_uninstall_ID, "卸载（pip uninstall）")
        menu.Append(self.popup_install_upgrade_ID, "更新（pip install --upgrade）") # 更新操作会用实际版本号刷新当前系统预置的版本号
        menu.AppendSeparator()
        menu.Append(self.popup_install_info_ID, "详细信息")
        self.PopupMenu(menu)
        menu.Destroy()

    @VirtualEnvMustExistDecorator()
    def onPopupInstallUpgrade(self, e):
        """更新 三方库"""
        name = self.pipListCtrl.GetItemText(self.currentItem, 0)
        cmd = subprocess.Popen(f'{env.getPipOrderArgs(mode="install --upgrade")} {name}', shell=True)
        self.cmdCodes.append(["U", cmd, name,])

    @VirtualEnvMustExistDecorator()
    @RegisterOriginOrderDecorator()
    def onPopupInstall(self, e):
        """弹出选项 -- 安装事件"""
        name = self.pipListCtrl.GetItemText(self.currentItem, 0)
        version = self.pipListCtrl.GetItemText(self.currentItem, 1)
        if version.strip(): # 提供版本号，拼接版本号
            pip_name = f'{name}=={version}'
        else:
            pip_name = name
        cmd = subprocess.Popen(f'{env.getPipOrderArgs()} {pip_name}', shell=True)
        self.cmdCodes.append(["I", cmd, pip_name,])

        obj = [_ for _ in self.datas if _["name"].lower() == name.lower()][0]
        if obj["isapp"]: # 自动检测注册
            register_name = obj["register_name"]
            position = obj["position"]
            if not djangotools.judge_installed_library(register_name):
                djangotools.add_oneline_to_listattr(djangotools.get_django_settings_path(), retools.PATT_INSTALLED_APPS, f"'{register_name}'", position=position)

    @VirtualEnvMustExistDecorator() 
    def onPopupUnInstall(self, e):
        """弹出选项 -- 卸载事件"""
        name = self.pipListCtrl.GetItemText(self.currentItem, 0)
        version = self.pipListCtrl.GetItemText(self.currentItem, 1)
        if version.strip():
            pip_name = f'{name}=={version}'
        else:
            pip_name = name
        cmd = subprocess.Popen(f'{env.getPipOrderArgs(mode="uninstall")} {pip_name}', shell=True)
        self.cmdCodes.append(["UI", cmd, pip_name])

    def onPopupInstallInfo(self, e):
        """查看安装包的详细信息"""
        RichMsgDialog.showScrolledMsgDialog(self, self.pipListCtrl.GetItemText(self.currentItem, 4), '详细描述')

    def onItemDeselected(self, e):
        """"""

    def onItemDelete(self, e):
        """"""

    def onColClick(self, e):
        """"""

    def onColRightClick(self, e):
        """"""

    def onColBeginDrag(self, e):
        """"""

    def onColDragging(self, e):
        """"""

    def onColEndDrag(self, e):
        """"""
        
    def onBeginEdit(self, e):
        """"""

    def onEndEdit(self, e):
        """"""

    def onDoubleClick(self, e):
        """"""

    def onRightDown(self, e):
        """"""

    # 给一个定时器，当 更新命令完成时，自动更新 pips.json 的信息
