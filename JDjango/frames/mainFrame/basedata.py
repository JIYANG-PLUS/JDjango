from .common import *

"""
    作用：基础数据
"""

class BaseData:

    def __init__(self) -> None:

        self.cmdCodes = [] # 所有的控制台指令（用于监听是否结束）
        self.info_cmdCodes = {} # 用于对照输出指令提示信息

        self.allInitBtns = {} # 所有需要控制的按钮
        self._init_control_btn() # 初始化运行时控制按钮

        # 独立于初始化之外的其它变量（检测和修复功能专用）
        self.unapps = set()  # 未注册的应用程序
        self.unurls = set() # 未注册的路由
        self.needfix = set() # 需要修复的模块

    def _init_control_btn(self):
        """初始化功能按钮控制器"""
        for _ in classifies:
            self.allInitBtns[_] = {
                CON_CONTROL_CHECK : []
                , CON_CONTROL_FIX : []
                , CON_CONTROL_CREATE : []
                , CON_CONTROL_OTHER : []
            }
