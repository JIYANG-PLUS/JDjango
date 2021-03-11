from ..common import *
from functools import wraps

"""
作用：共用库，主要功能键
"""

cmd = CmdTools() # 命令行对象

classifies = ['global', 'apps', 'views', 'urls', 'templates', 'forms', 'models', 'database', 'admin'] # 所有的功能按钮

class VirtualEnvMustExistDecorator:
    """装饰器：虚拟环境必须存在！！！"""
    def __init__(self, *args, **kwargs): ...
    def __call__(self, func, e=None):
        @wraps(func)
        def decorator(obj, *args, **kwargs):
            env_path = env.getPython3Env()
            if '' == env_path.strip() or not os.path.exists(env_path):
                wx.MessageBox(f'虚拟环境未绑定，或绑定失败！', CON_TIPS_COMMON, wx.OK | wx.ICON_INFORMATION)
                return
            if len(args) > 0:
                e = args[0]
            return func(obj, e)
        return decorator

class RegisterOriginOrderDecorator:
    """系统命令装饰"""
    def __init__(self, *args, **kwargs):
        self.cmdCodes = []
        self.info_cmdCodes = {}
        if 'msg' in kwargs:
            self.msg = kwargs['msg']
        else:
            self.msg = 'UnKnown'
    def __call__(self, func, e=None):
        @wraps(func)
        def decorator(obj, *args, **kwargs):
            if len(args) > 0:
                e = args[0]
            func_return = func(obj, e)
            if not func_return:
                return
            cmdObj, self.cmdCodes, self.info_cmdCodes = func_return
            self.cmdCodes.append(cmdObj)
            self.info_cmdCodes[cmdObj] = self.msg
        return decorator
