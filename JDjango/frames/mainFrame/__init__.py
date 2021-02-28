from .final_gui import MainFrameFinalGUI

"""

### 新增一个菜单按钮步骤
#1 在菜单合适的位置添加按钮控件；
#2 控制它的可用性，在项目引入之前开放还是之后；
#3 为了简便控制，可以直接加载任意一个功能的create模块下，已达到可用性控制。（不可取但可行）

### 新增命令的步骤
#1 使用 subprocess 添加命令进程；
#2 将进程添加进 cmdCodes 中;
#3 在 info_cmdCodes 添加对照提示信息即可。

"""