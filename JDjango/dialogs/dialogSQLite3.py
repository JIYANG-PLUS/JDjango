import wx, json, glob, os, re
import wx.lib.buttons as buttons
import wx.grid
from wx.lib import scrolledpanel
from ..tools._tools import *
from ..tools._re import *
from .. settings import BASE_DIR, CONFIG_PATH, CONFIG_PATH
from ..tools import environment as env
from ..tools import models as toolModel
from ..miniCmd.djangoCmd import *

class TableAttrbutesDialog(wx.Dialog):
    
    def __init__(self, parent, id, **kwargs):
        wx.Dialog.__init__(self, parent, id, f"{kwargs['node_name']}的字段属性", size=(500, 350))

        wholePanel = wx.Panel(self)
        wholeBox = wx.BoxSizer(wx.VERTICAL) # 垂直
        wholePanel.SetSizer(wholeBox)

        self.attrbutesGrid = wx.grid.Grid( wholePanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
        self.attrbutesGrid.CreateGrid( 26, 26 )
        self.attrbutesGrid.EnableEditing( False )
        self.attrbutesGrid.EnableGridLines( True )
        self.attrbutesGrid.EnableDragGridSize( False )
        self.attrbutesGrid.SetMargins( 0, 0 )

        # Columns
        self.attrbutesGrid.EnableDragColMove( False )
        self.attrbutesGrid.EnableDragColSize( True )
        self.attrbutesGrid.SetColLabelSize( 40 )
        self.attrbutesGrid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Rows
        self.attrbutesGrid.EnableDragRowSize( True )
        self.attrbutesGrid.SetRowLabelSize( 90 )
        self.attrbutesGrid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
        self.attrbutesGrid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        wholeBox.Add( self.attrbutesGrid, 1, wx.EXPAND | wx.ALL, 2 )

        if 'datas' in kwargs:
            self.datas = datas
        else:
            self.datas = None

        # 初始化同步数据
        self._init_data()

    def _init_data(self):
        """初始化数据"""
        pass


