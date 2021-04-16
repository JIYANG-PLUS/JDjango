from .SettingsPropertyPanel import *
from .PipListCtrlPanel import *
from .NotFoundPanel import *
from .UrlsListPanel import *
from .AutoGenModelsPanel import *
from .AutoGenViewsPanel import *
from .BatchExcelPanel import *
from .WxPythonCtrlsPanel import *
from .PythonEditor import *

'''
新增属性步骤：
1、在 propertys.json 中添加属性参数；
2、在 SettingsPropertyPanel 中设置 保存 操作的相关值
3、在 refresh_config 的 set_configs 中添加属性纯文本读取操作
'''
