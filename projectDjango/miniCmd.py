#!/usr/bin/env python3
import os, json, sys, shutil, re
from functools import wraps
from .settings import (LANGUAGE
    , SUPPORT_UNPACK , SUPPORT_LS, BASE_DIR)    

with open('./tips.json', encoding='utf-8') as f: TIPS = json.load(f)
with open('./errors.json', encoding='utf-8') as f: ERRORS = json.load(f)
with open('./args.json', encoding='utf-8') as f: ARGS = json.load(f)


class BeautifulShow:
    def __init__(self, *args, tips=False, mode=0, **kwargs):
        self.tips = tips
        self.mode = mode
    def __call__(self, func):
        @wraps(func)
        def show(obj, *args):
            outStr = TIPS[func.__name__][LANGUAGE] if self.tips else ''
            infos = list(func(obj, *args))
            if 1 == self.mode: outStr += '  '.join(infos) + '\n'
            else: outStr += '\n'.join(infos) + '\n'
            if infos: return outStr
            else: return ''
        return show

class ErrorRemind:
    def __init__(self, *args, **kwargs): pass
    def __call__(self, func):
        @wraps(func)
        def register(obj, *args):
            if 0 == len(args): return func(obj, *args)
            t_tips = ARGS[func.__name__]
            if '***' in t_tips: return func(obj, *args)
            for _ in args:
                if _ not in t_tips: break
            else: return func(obj, *args)
            return ERRORS[func.__name__][LANGUAGE]
        return register

def tab(): pass # TAB自动补全功能（还在构思中）

class CmdTools:
    
    def __init__(self, *args, **kwargs): self.namespace = {}
    
    @BeautifulShow(mode = 1)
    @ErrorRemind()
    def ls(self, *args):
        dirs = os.listdir(os.getcwd())
        if not args: return dirs
        elif 1 == len(args):
            param = args[0]
            if '-F' == param: return (_ for _ in dirs if  os.path.isdir(_))
            elif '-f' == param: return (_ for _ in dirs if  os.path.isfile(_))
            elif param in SUPPORT_LS: return (_ for _ in dirs if os.path.splitext(_)[1]==param)

    @BeautifulShow()
    @ErrorRemind()
    def cd(self, *args):
        if not args: return ERRORS[sys._getframe().f_code.co_name][LANGUAGE]
        if 1 == len(args):
            param = args[0]
            if '..' == param: os.chdir(os.path.dirname(os.getcwd()))
            elif '../..' == param:
                os.chdir(os.path.dirname(os.getcwd()))
                os.chdir(os.path.dirname(os.getcwd()))
            else:
                try:
                    if os.path.isabs(param): os.chdir(param)
                    else: os.chdir(os.path.join(os.getcwd(), param))
                except: return ERRORS[sys._getframe().f_code.co_name][LANGUAGE]
        return []

    @BeautifulShow(tips=True)
    def pwd(self, *args): return [os.getcwd(),]

    @BeautifulShow(tips=True)
    def date(self, *args):
        from datetime import datetime
        return [f'{datetime.now():%Y-%m-%d %H:%M:%S}',]

    @BeautifulShow()
    @ErrorRemind()
    def zip(self, *args):
        if not args: return ERRORS[sys._getframe().f_code.co_name][LANGUAGE]
        if 1 == len(args): param = args[0]
        return []

    @BeautifulShow()
    @ErrorRemind()
    def unzip(self, *args):
        if not args: return ERRORS[sys._getframe().f_code.co_name][LANGUAGE]
        if 1 == len(args):
            param = args[0]
            if '-help' == param:
                return ("支持的解压格式：",) + SUPPORT_UNPACK
            if os.path.splitext(param)[1] in SUPPORT_UNPACK and os.path.exists(param):
                shutil.unpack_archive(param, '.')
            else: return ERRORS[sys._getframe().f_code.co_name][LANGUAGE]
        else: return ERRORS[sys._getframe().f_code.co_name][LANGUAGE]
        return []

    @BeautifulShow()
    @ErrorRemind()
    def rm(self, *args):
        if not args: return ERRORS[sys._getframe().f_code.co_name][LANGUAGE]
        if '-f' in args and len(args) >= 2:
            args = list(args)
            args.remove('-f')
            for param in args:
                if os.path.exists(param) and os.path.isfile(param):
                    os.remove(param)
        elif '-rf' in args and len(args) >= 2:
            args = list(args)
            args.remove('-rf')
            for param in args:
                if os.path.exists(param) and os.path.isdir(param):
                    shutil.rmtree(param)
        else: return ERRORS[sys._getframe().f_code.co_name][LANGUAGE]
        return []

    @BeautifulShow()
    @ErrorRemind()
    def mkdir(self, *args):
        if not args: return ERRORS[sys._getframe().f_code.co_name][LANGUAGE]
        for param in args: os.mkdir(param)
        return []

    @BeautifulShow()
    @ErrorRemind()
    def mkfile(self, *args):
        if not args: return ERRORS[sys._getframe().f_code.co_name][LANGUAGE]
        for param in args:
            with open(param, 'w', encoding='utf-8') as f: pass
        return []

    @BeautifulShow()
    @ErrorRemind()
    def ping(self, *args):
        if not args: return ERRORS[sys._getframe().f_code.co_name][LANGUAGE]
        if 1 == len(args):
            param = args[0]
            status = os.system(f'Ping {param}')
            if 0 == status: return ['Ping success.', ]
            else: return ['ping failure.', ]
        else: return ERRORS[sys._getframe().f_code.co_name][LANGUAGE]
        return []

    @BeautifulShow()
    def exec(self, code): 
        try: exec(code, {}, self.namespace)
        except Exception as e: return [f'错误：{e}',]
        else: return []

    @BeautifulShow()
    def print(self, code): 
        try: exec(f'print({code})', {}, self.namespace)
        except Exception as e: return [f'错误：{e}',]
        else: return []

    