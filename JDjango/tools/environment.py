import os, re
import xml.etree.ElementTree as ET
from typing import Any, List
from ..settings import BASE_DIR, ENV_PATH, CONFIG_PATH
from ._tools import *

class XMLFileParserException(Exception): pass
class PathNotFoundException(Exception): pass

class EnvParser:

    def __init__(self, *args, **kwargs):

        if 'xml' in kwargs:

            self._init_tree(kwargs['xml'])
            self._init_root()
            if not self._check_ok():
                raise XMLFileParserException('文件不存在或XML格式不正确。')
        else:
            raise XMLFileParserException('XML文件读取异常。')
        self._init_pattern()

    def _init_tree(self, xml: str)->Any:
        try:
            self.TREE = ET.parse(xml)
        except:
            self.TREE = None

    def _init_root(self)->Any:
        if self.TREE:
            self.ROOT = self.TREE.getroot()
        else:
            self.ROOT = None

    def _init_pattern(self)->None:
        """XML专属正则"""
        # 捕捉属性及其值
        self.patt_match_xpath = re.compile(r'([a-z]+?)\[([a-z]+?)=([a-z][0-9a-z].*?)\]') # 如：'path/json/prop[name=config]'

    def _check_ok(self)->bool:
        """检测XML是否读取成功"""
        if not self.TREE or not self.ROOT:
            return False
        return True

    def get_xpath_node(self, xpath: str)->object:
        """通过路径语法获取节点"""
        searcher = self.ROOT # 从根节点开始往下延伸寻找
        xpath_split = xpath.split('/')
        for _ in xpath_split: # 逐级查找
            temp = self.patt_match_xpath.match(_)
            if temp: # 如果包含属性限制
                label, attr, v = (
                    temp.group(1)
                    , temp.group(2)
                    , temp.group(3)
                )
                nodes = searcher.findall(label)
                searcher = self._get_node_by_attr(
                    nodes
                    , attr
                    , v = v
                )
            else: # 不包含属性的节点
                try:
                    searcher = searcher.find(_)
                except:
                    raise PathNotFoundException('路径不存在。')
        return searcher

    def _get_node_by_attr(self, nodes: object, attr: str, v: str=''):
        """通过属性限制获取节点"""
        for node in nodes: # 循环遍历节点
            # node.attrib: 获取所有的节点属性名
            # node.attrib[attr]: 获取属性名为attr的值
            if attr in node.attrib and v == node.attrib[attr]:
                return node
        else:
            raise PathNotFoundException('路径不存在。')

    def get_node_text(self, node):
        """获取节点文本"""
        return node.text

    def get_childnode_lists(self, path):
        """获取所有直接孩子节点的文本内容"""
        node = self.get_xpath_node(path)
        return [_.text for _ in node]

    def save(self):
        """保存XML更改"""
        self.TREE.write(ENV_PATH, encoding="utf-8", xml_declaration=True)

### 赋值

def setFontSize(step = 1, method = 'add'):
    """设置字体大小"""
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('page/font-size')
    font_size = int(node.text)
    if 'add' == method: 
        node.text = str(font_size + step)
    else:
        if font_size > 2:
            node.text = str(font_size - step)
    obj.save()

def setPython3Env(path: str):
    """选择设置虚拟环境"""
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('env/python3')
    node.text = str(path)
    obj.save()

def setPlatfrom(name: str):
    """设置当前运行平台"""
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('env/platform')
    node.text = str(name)
    obj.save()

### 取值

def getEnvXmlObj():
    """获取对象"""
    return EnvParser(xml = os.path.join(BASE_DIR, ENV_PATH))

def getFontSize()->int:
    """获取字体大小"""
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('page/font-size')
    return int(node.text)

def getModelsAlias()->List[str]:
    """获取所有models.py的别名"""
    obj = getEnvXmlObj()
    return obj.get_childnode_lists('alias/file[name=models]')

def getAdminAlias()->List[str]:
    """获取所有admin.py的别名"""
    obj = getEnvXmlObj()
    return obj.get_childnode_lists('alias/file[name=admin]')

def getViewsAlias()->List[str]:
    """获取所有views.py的别名"""
    obj = getEnvXmlObj()
    return obj.get_childnode_lists('alias/file[name=views]')

def getUrlsAlias()->List[str]:
    """获取所有urls.py的别名"""
    obj = getEnvXmlObj()
    return obj.get_childnode_lists('alias/file[name=urls]')

def getDjangoRunPort()->int:
    """获取Django的运行端口"""
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('env/port')
    return int(node.text)

def getPython3Env()->str:
    """获取项目运行虚拟环境"""
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('env/python3')
    return node.text if node.text else ''

def getPlatform()->str:
    """获取当前运行的平台"""
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('env/platform')
    return node.text if node.text else ''

def getAllSupportPlatform()->List[str]:
    """获取软件已支持的平台类型"""
    obj = getEnvXmlObj()
    return obj.get_childnode_lists('env/support[name=all]')

def getSupportEnvPlatform()->List[str]:
    """获取软件已支持虚拟环境运行的平台类型"""
    obj = getEnvXmlObj()
    return obj.get_childnode_lists('env/support[name=virtualenv]')

def getDjangoSupportDatabase()->List[str]:
    """获取Django支持的所有数据库"""
    obj = getEnvXmlObj()
    return obj.get_childnode_lists('env/database')

def getRealPythonOrder()->str:
    """获取非虚拟环境的Python命令"""
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('real/python3')
    return node.text

def getConflictFieldsName():
    """获取冲突列表里的字段名集合"""
    obj = getEnvXmlObj()
    return obj.get_childnode_lists('conflict-list/field-name')

def getDjangoOrderArgs(mode: str = 'manage.py')->str:
    """获取Django的命令参数形式，如：python manage.py"""
    path = os.path.join(get_configs(CONFIG_PATH)['dirname'], mode)
    env_python3 = os.path.splitext(getPython3Env())[0]
    return f"{env_python3} {path}"

def getPipOrderArgs(mode = 'install'):
    """获取虚拟环境pip install命令"""
    env_python3_pip = os.path.join(os.path.dirname(getPython3Env()), 'pip')
    return f'{env_python3_pip} {mode}'

### 其它

def killProgress(port = None):
    """终止进程"""
    import subprocess, platform
    p = platform.system()
    if not port:
        port = getDjangoRunPort()
    if p.lower() == 'linux': # 企鹅系统
        pass
    elif p.lower() == 'windows': # 微软系统
        p = subprocess.Popen(f'netstat -ano |findstr {port}', shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()
        temp = []
        for line in out.splitlines():
            try:
                jc = [_ for _ in line.decode(encoding='utf-8').split(' ') if _][-1]
                temp.append(jc)
            except: ...
        for _ in set(temp):
            t = subprocess.Popen(f'taskkill /f /t /im {_}', shell=True)
            t.wait()
    elif p.lower() == 'darwin':
        pass
    else: # 其他系统
        raise Exception('UnKnown system.')
