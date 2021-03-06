import os

"""常用路径"""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
ENV_PATH = os.path.join(BASE_DIR, 'environment.xml')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'djangoTemplates')
CMD_DIR = os.path.join(BASE_DIR, 'miniCmd')
PRINT_PATH = os.path.join(BASE_DIR, 'tools', 'print_console.py')
BITMAP_DIR = os.path.join(BASE_DIR, 'static', 'bitmap')

"""矢量图路径"""
BITMAP_SIZE = 24 # 矢量图大小，可取值：16、24
BITMAP_EXIT_PATH = os.path.join(BITMAP_DIR, f'exit_{BITMAP_SIZE}px.png')
BITMAP_SETTINGS_PATH = os.path.join(BITMAP_DIR, f'settings_{BITMAP_SIZE}px.png')
BITMAP_DATABASE_PATH = os.path.join(BITMAP_DIR, f'database_{BITMAP_SIZE}px.png')
BITMAP_INFO_PATH = os.path.join(BITMAP_DIR, f'info_{BITMAP_SIZE}px.png')
BITMAP_RUN_PATH = os.path.join(BITMAP_DIR, f'run_{BITMAP_SIZE}px.png')
BITMAP_STOP_PATH = os.path.join(BITMAP_DIR, f'stop_{BITMAP_SIZE}px.png')
BITMAP_SPLIT_PATH = os.path.join(BITMAP_DIR, f'1split_{BITMAP_SIZE}px.png')
BITMAP_COMMAND_PATH = os.path.join(BITMAP_DIR, f'command_{BITMAP_SIZE}px.png')
BITMAP_MIGRATE_PATH = os.path.join(BITMAP_DIR, f'migrate_{BITMAP_SIZE}px.png')
BITMAP_MAKEMIGRATION_PATH = os.path.join(BITMAP_DIR, f'makemigration_{BITMAP_SIZE}px.png')
BITMAP_FILE_PATH = os.path.join(BITMAP_DIR, f'file_{BITMAP_SIZE}px.png')
BITMAP_PIPINSTALL_PATH = os.path.join(BITMAP_DIR, f'pipinstall_{BITMAP_SIZE}px.png')

"""跨域中间件"""
COR_MIDDLEWARE = "'corsheaders.middleware.CorsMiddleware'"

"""超文本文档路径"""
LOCAL_DOCS_PATH = os.path.join(BASE_DIR, 'docs', 'all', 'html')

"""Django官方文档链接"""
DJANGO_DOCS_URL = {
    '31' : r'https://docs.djangoproject.com/zh-hans/3.1/',
    '22' : r'https://docs.djangoproject.com/zh-hans/2.2/',
    'law' : r'https://flk.npc.gov.cn/', # 国家法律法规
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
        1 : ('Asia/Shanghai',), # 上海时区 
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

