import wx, json, glob, os, re
import wx.lib.buttons as buttons
from wx.lib import scrolledpanel
from ..tools._tools import *
from ..tools._re import *
from .. settings import BASE_DIR, CONFIG_PATH, CONFIG_PATH
from ..tools import environment as env
from ..tools import models as toolModel
from ..miniCmd.djangoCmd import *

class SelectSQLite3Dialog(wx.Dialog):
    
    def __init__(self, parent, id, **kwargs):
        wx.Dialog.__init__(self, parent, id, '选择数据库', size=(300, 150))

        wholePanel = wx.Panel(self)
        wholeBox = wx.BoxSizer(wx.VERTICAL) # 垂直
        wholePanel.SetSizer(wholeBox)


        # 初始化同步数据
        self._init_data()

    def _init_data(self):
        """初始化数据"""
        pass


