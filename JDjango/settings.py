import os

"""常用路径"""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
ENV_PATH = os.path.join(BASE_DIR, 'environment.xml')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'djangoTemplates')
CMD_DIR = os.path.join(BASE_DIR, 'miniCmd')

"""超文本文档路径"""
LOCAL_DOCS_PATH = os.path.join(BASE_DIR, 'docs', 'all', 'html')

"""Django官方文档链接"""
DJANGO_DOCS_URL = {
    '31' : r'https://docs.djangoproject.com/zh-hans/3.1/',
    '22' : r'https://docs.djangoproject.com/zh-hans/2.2/',
}

"""settings.py文件所需常量"""
SETTINGSS = {
    # 这里的0和1表示单选框组的第一个和第二个
    'LANGUAGE_CODE' : {
        0 : ('zh-Hans', 'zh_Hans'), # 中文
        1 : ('en-us', 'en_us', ), # 英文
    },
    'TIME_ZONE' : {
        0 : ('UTC',), # 伦敦时区
        1 : ('Asia/Shanghai',), # 北京时区 
        2 : ('America/Chicago',), # 美国芝加哥
    },
}

"""本软件运行环境（该功能待定）"""
LANGUAGE = 'C' # 当前语言环境（C中文，E英文）

"""软件支持的文件后缀名"""
SUPPORT_UNPACK = (
    '.tar.bz2', '.tbz2', '.tar.gz', '.tgz', '.tar'
    , '.tar.xz', '.txz', '.zip',
)
SUPPORT_LS = (
    '.docx', '.py', '.txt', '.zip', '.rar'
    , '.xlsx', '.xls', '.rtf', '.ppt', '.pptx'
    , '.doc', '.exe', '.dll', '.png', '.jpg'
    , '.sql', '.bmp', '.css', '.less', '.js'
    , '.vue', '.c', '.java', '.cpp', '.cs'
    , '.sln', '.xml', '.json', 
)

