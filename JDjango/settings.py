import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LANGUAGE = 'C' # 当前语言环境（C中文，E英文）

# if 'miniCmd.py' not in os.listdir('.'):
#     BASE_DIR = os.path.join(os.getcwd(), 'minicmd') # 追踪到miniCmd.py所在路径
#     os.chdir(BASE_DIR) # 若运行出错，请检查项目路径是否正确
# else: BASE_DIR = os.getcwd()


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

