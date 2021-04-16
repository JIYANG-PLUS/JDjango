import re

PATT_BASE_DIR = re.compile(r'BASE_DIR\s*=\s*os.path.dirname\s*\(\s*os.path.dirname\s*\(\s*os.path.abspath\s*\(\s*__file__\s*\)\s*\)\s*\)')
PATT_INSTALLED_APPS = re.compile(r"(?ms:INSTALLED_APPS\s.*?=\s.*?\[.*?\])")
PATT_MIDDLEWARE = re.compile(r"(?ms:MIDDLEWARE\s.*?=\s.*?\[.*?\])")
PATT_SECRET_KEY = re.compile(r"SECRET_KEY\s*=\s*[\'\"](.*?)[\'\"]")
PATT_DEBUG = re.compile(r"DEBUG\s*=\s*(False|True)")
PATT_ALLOWED_HOSTS = re.compile(r"ALLOWED_HOSTS\s*=\s*\[([\'\"]*.*?[\'\"]*)\]")
PATT_X_FRAME_OPTIONS = re.compile(r"\nX_FRAME_OPTIONS\s*=\s*('ALLOWALL')")
PATT_LANGUAGE_CODE = re.compile(r"LANGUAGE_CODE\s*=\s*'(.*?)'")
PATT_TIME_ZONE = re.compile(r"TIME_ZONE\s*=\s*'(.*?)'")
PATT_USE_I18N = re.compile(r"USE_I18N\s*=\s*(False|True)")
PATT_USE_L10N = re.compile(r"USE_L10N\s*=\s*(False|True)")
PATT_DATABASES = re.compile(r'(?ms:DATABASES\s*=\s*\{.*)')
PATT_USE_TZ = re.compile(r"USE_TZ\s*=\s*(False|True)")
PATT_CORS_ORIGIN_ALLOW_ALL = re.compile(r"CORS_ORIGIN_ALLOW_ALL\s*=\s*(False|True)")
PATT_STATIC_URL = re.compile(r"STATIC_URL\s*=\s*[\'\"](.*?)[\'\"]")
PATT_TEMPLATES = re.compile(r'(?ms:TEMPLATES\s*=\s*\[.*)')
PATT_ROOT_URLCONF = re.compile(r"ROOT_URLCONF\s*=\s*[\'\"](.*?)[\'\"]")

PATT_CHARS = re.compile(r'^[a-zA-Z_]*$')
PATT_CHARS_REVERSED = re.compile(r'[^a-zA-Z_]+')
PATT_DIGITS_WHOLE = re.compile(r'^[1-9][0-9]*$')
PATT_DIGITS_REVERSED = re.compile(r'[^0-9]+')
PATT_CHARSNUMBER = re.compile(r'^[a-zA-Z0-9]*$')
PATT_REPLACE = re.compile(r'[$][{](.*?)[}]') # 模板定位替换语法
PATT_TITLE_NAME = re.compile(r'admin.site.site_title\s*=\s*[\"\'](.*?)[\"\']')
PATT_HEADER_NAME = re.compile(r'admin.site.site_header\s*=\s*[\"\'](.*?)[\"\']')
PATT_URLPATTERNS = re.compile(r'(?ms:urlpatterns\s*=\s*\[.*)')
PATT_MODEL = re.compile(r'class\s+(.+?)\(\s*[a-zA-Z0-9]*?[.]*?Model\s*\):') # 定位模型类
PATT_CAPTURE_URLSPATH_ARGS = re.compile(r'<(.+?)>') # 捕捉路由参数信息
PATT_FUNC_ARGS = re.compile(r'def\s+.+?\((.*?)\)')
PATT_COMMENT = re.compile(r'(\s*#.*?$)') # 注释
PATT_REGISTER = re.compile(r'admin.site.register\s*\(\s*(.+?)\s*\)')
PATT_INCLUDE = re.compile(r'include\s*\((.*)\)')
