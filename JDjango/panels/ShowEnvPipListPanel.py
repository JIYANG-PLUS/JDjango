from .common import *

class ShowEnvPipListPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self._init_UI()
        self._init_data()

    def _init_UI(self):

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        self.panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(topsizer)
        topsizer.SetSizeHints(self.panel)
        sizer.Add(self.panel, 1, wx.EXPAND)

        '''
            列表页
        '''
        self.envPipListView = wxdv.DataViewCtrl(self.panel,
            style = wx.BORDER_THEME
            | wxdv.DV_ROW_LINES # 背景交替色
            # | wxdv.DV_HORIZ_RULES
            | wxdv.DV_VERT_RULES
            | wxdv.DV_MULTIPLE
        )
        topsizer.Add(self.envPipListView, 1, wx.EXPAND | wx.ALL, 5)

        '''
            定义列
        '''
        index = self.envPipListView.PrependTextColumn("序号", 0, width=40, align=wx.ALIGN_CENTER)
        self.envPipListView.AppendTextColumn("三方库名称", 1, width=270, mode=wxdv.DATAVIEW_CELL_EDITABLE, align=wx.ALIGN_CENTER)
        self.envPipListView.AppendTextColumn("版本号", 2, width=260, mode=wxdv.DATAVIEW_CELL_EDITABLE, align=wx.ALIGN_CENTER)

        '''
            序号列参数设置
        '''
        index.Alignment = wx.ALIGN_RIGHT
        index.Renderer.Alignment = wx.ALIGN_RIGHT
        index.MinWidth = 40

        '''
            列属性集体设置
        '''
        for c in self.envPipListView.Columns:
            c.Sortable = True
            c.Reorderable = True

        index.Reorderable = False

        self.Bind(wxdv.EVT_DATAVIEW_ITEM_EDITING_DONE, self.onEditingDone, self.envPipListView)
        self.Bind(wxdv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.onValueChanged, self.envPipListView)

    def _init_data(self):
        """初始化列表数据"""
        data = self.get_data()
        self.model = ShowAllPipsModel(data)
        self.envPipListView.AssociateModel(self.model)

    def get_data(self):
        """获取构建数据包"""
        data = []

        p = subprocess.Popen(f'{env.getPipOrderArgs(mode="freeze")}', shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()
        if err:
            return []

        for i, _ in enumerate(out.splitlines()):
            temp = _.decode(encoding='utf-8').strip().split('==')
            data.append([str(i+1), temp[0], temp[-1]])
        
        return data

    def onEditingDone(self, e):
        """"""

    def onValueChanged(self, e):
        """"""
