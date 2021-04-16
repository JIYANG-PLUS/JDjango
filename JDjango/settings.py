import os

"""常用路径"""
BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    , 'resources'
)

### pyinstaller 打包专用路径
if not os.path.exists(BASE_DIR):
    BASE_DIR = os.path.join(os.getcwd(), 'resources')

CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
ENV_PATH = os.path.join(BASE_DIR, 'environment.xml')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'djangoTemplates')
CMD_DIR = os.path.join(BASE_DIR, 'miniCmd')
PRINT_PATH = os.path.join(BASE_DIR, 'tools', 'print_console.py')
SITE_PACKAGES_PATH = os.path.join(BASE_DIR, 'tools', 'get_site_packages.py')
BITMAP_DIR = os.path.join(BASE_DIR, 'static', 'bitmap')
KV_PATH = os.path.join(BASE_DIR, 'propertys.json')
PIPS_PATH = os.path.join(BASE_DIR, 'pips.json')

"""矢量图路径"""
BITMAP_SIZE = 16 # 矢量图大小，可取值：16、24
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
BITMAP_CODE_PATH = os.path.join(BITMAP_DIR, f'code_{BITMAP_SIZE}px.png')

BITMAP_LIST_FIT_PATH = os.path.join(BITMAP_DIR, f'database_24px.png')

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
