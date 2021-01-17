import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
ENV_PATH = os.path.join(BASE_DIR, 'environment.xml')

DJANGO_DOCS_URL = {
    '31' : r'https://docs.djangoproject.com/zh-hans/3.1/',
    '22' : r'https://docs.djangoproject.com/zh-hans/2.2/',
}


LANGUAGE = 'C' # 当前语言环境（C中文，E英文）

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

