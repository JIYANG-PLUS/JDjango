import wx
import wx.grid

class TableAttrbutesDialog(wx.Dialog):
    
    def __init__(self, parent, id, **kwargs):
        wx.Dialog.__init__(self, parent, id, f"{kwargs['node_name']}的字段属性", size=(660, 350))

        self.wholePanel = wx.Panel(self)
        self.wholeBox = wx.BoxSizer(wx.VERTICAL) # 垂直
        self.wholePanel.SetSizer(self.wholeBox)

        if 'datas' in kwargs:
            self.datas = kwargs['datas']
            self._init_table()
        else:
            self.datas = None

        # 初始化同步数据
        self._init_data()

    def _init_table(self):
        """初始化表格"""
        self.row_len = len(self.datas) # 行数
        self.col_len = len(self.datas[0]) if len(self.datas) > 0 else 0 # 列数

        self.attrbutesGrid = wx.grid.Grid( self.wholePanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
        self.attrbutesGrid.CreateGrid( self.row_len+1, self.col_len ) # row  col
        self.attrbutesGrid.EnableEditing( False )
        self.attrbutesGrid.EnableGridLines( True )
        self.attrbutesGrid.EnableDragGridSize( False )
        self.attrbutesGrid.SetMargins( 0, 0 )

        # Columns
        self.attrbutesGrid.EnableDragColMove( False )
        self.attrbutesGrid.EnableDragColSize( True )
        self.attrbutesGrid.SetColLabelSize( 30 )
        self.attrbutesGrid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Rows
        self.attrbutesGrid.EnableDragRowSize( True )
        self.attrbutesGrid.SetRowLabelSize( 70 )
        self.attrbutesGrid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
        self.attrbutesGrid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        self.wholeBox.Add( self.attrbutesGrid, 1, wx.EXPAND | wx.ALL, 2 )

        self._init_header()
        self._init_data()

    def _init_header(self):
        """设置表头"""
        headers = ('序号', '列名', '类型', '允许为NULL', '默认值', '主键')[:self.col_len]
        for i, _ in enumerate(headers):
            self.attrbutesGrid.SetCellValue(0, i, _)
            self.attrbutesGrid.SetCellBackgroundColour(0, i, 'yellow')

    def _init_data(self):
        """初始化数据"""
        for row, _ in enumerate(self.datas):
            for col, data in enumerate(_):
                self.attrbutesGrid.SetCellValue(row+1, col, f'{data}')
