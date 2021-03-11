from .dialogDocument import *
from .dialogModels import *
from .dialogOption import *
from .dialogORM import *
from .dialogSettings import *
from .dialogSQLite3 import *
from .dialogTips import *
from .dialogViews import *


"""
### 有关别名的一些说明：
# 如果路径改变，可在environment.xml中配置完整的路径别名（如，windows下 admin.py 可扩展成 myfloder/admin.py，但是要确保路径紧邻该app路径下！）

### 后台重命名规则
# 默认在admin.py及其别名处命名后台；
# 若从没有显示命名过，则任选一处命名；
# 若只有一处命名，则修改当前处命名；
# 若有两个及以上的地方命名，会在修改界面予以警告。一旦触发修改，会删除所有，再任选一处命名。

### 添加最大化最小化样式（默认样式 + 最大化 + 最小化 + 边界可调整）
style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER

#无上级父窗口控制
wx.DIALOG_NO_PARENT

"""
