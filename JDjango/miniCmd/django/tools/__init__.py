"""
### 关于 settings.py 的说明：
# 不允许在 settings.py 中引入任何的第三方库（尽管这是可行的行为）；
# 若想要做一些环境初始化（如：MySQL配置），请移步到同目录下的 __init__.py 文件中设置。

### 关于别名的一些注意点：
# 根路由默认为urls.py，如非必要，请勿取别名。

"""
from .common import *
from .gets import *
from .sets import *
from .judge import *
from .other import *
from . import config as SCONFIGS
