import datetime, json, re, string, random
from typing import List, Dict, NoReturn, Any

LEVEL = {
    1: '【success】',
    2: '【warning】',
    3: '【error】',
}


def out_infos(info: str, level: int=None) -> str:
    """正常提示信息"""
    d = datetime.datetime.now()
    if level:
        l_info = LEVEL[level]
    else:
        l_info = ''
    return f'{d:%Y/%m/%d %H:%M:%S}{l_info}：{info}\n'


def out_command_infos(info: str) -> str:
    """命令形式输出"""
    return f'>>> {info}\n'

def read_file(path: str) -> str:
    """读整个文件"""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def read_file_list(path: str) -> List[str]:
    """读取文件列表"""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.readlines() # 包含\n字符
    return content

def read_file_list_del_comment(path: str) -> List[str]:
    """删掉注释，读取文件列表"""
    patt = re.compile(r'(\s*#.*?$)')
    return [patt.sub(' ', _) for _ in read_file_list(path)]

def write_file(path: str, content: str) -> NoReturn:
    """一次性写入文件"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def dump_json(file_name: str, configs: Dict[str, Any]) -> NoReturn:
    """写入JSON"""
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(configs, f, indent=4)

def get_configs(path: str) -> Dict[str, Any]:
    """读取目标项目配置"""
    with open(path, 'r', encoding='utf-8') as f:
        configs = json.load(f)
    return configs

def new_file(path: str, content: List[str]=None) -> NoReturn:
    """新增文件（可同时赋值）"""
    with open(path, 'w', encoding='utf-8') as f:
        if content:
            f.writelines(content)

def append_file(path: str, content: List[str]=[]) -> NoReturn:
    """向文本末尾追加内容列表"""
    with open(path, 'a', encoding='utf-8') as f:
        f.write('\n' + ''.join(content))

def generate_secret_key(length: int=50) -> str:
    """更新 SECRET_KEY"""
    allChars = list(string.printable)
    minusChars = f'{string.whitespace}\'"\\'
    for _ in minusChars:
        allChars.remove(_)
    secret = []
    for i in range(length):
        secret.append(random.choice(allChars))
    return ''.join(secret)

def cut_content_by_doublecode(text: str, leftCode: str='[', rightCode: str=']') -> str:
    """获取成对的中括号中的文本（不包含两侧成对符号）"""
    # 如：[asd[cvb]] 会获取到 asd[cvb]
    stack = []
    cut_text = ""
    for _ in text:
        if len(stack) > 0:
            cut_text += _
        if leftCode == _:
            stack.append(_)
        if rightCode == _:
            stack.pop()
            if 0 == len(stack):
                return cut_text[:-1]
    return ''

