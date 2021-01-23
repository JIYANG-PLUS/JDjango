import os, re
import xml.etree.ElementTree as ET
from ..settings import BASE_DIR, ENV_PATH

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

    def _init_tree(self, xml):
        try:
            self.TREE = ET.parse(xml)
        except:
            self.TREE = None

    def _init_root(self):
        if self.TREE:
            self.ROOT = self.TREE.getroot()
        else:
            self.ROOT = None

    def _init_pattern(self):
        self.patt_match_xpath = re.compile(r'([a-z]+?)\[([a-z]+?)=([a-z][0-9a-z].*?)\]') # 'path/json/prop[name=config]'

    def _check_ok(self):
        if not self.TREE or not self.ROOT:
            return False
        return True

    def get_xpath_node(self, xpath):
        """通过路径语法获取节点"""
        searcher = self.ROOT
        xpath_split = xpath.split('/')
        for _ in xpath_split:
            temp = self.patt_match_xpath.match(_)
            if temp:
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
            else:
                try:
                    searcher = searcher.find(_)
                except:
                    raise PathNotFoundException('路径不存在。')
        return searcher

    def _get_node_by_attr(self, nodes, attr, v=''):
        """通过属性限制获取节点"""
        for node in nodes:
            if attr in node.attrib and v == node.attrib[attr]:
                return node
        else:
            raise PathNotFoundException('路径不存在。')


    def get_node_text(self, node):
        return node.text

    def fill_base_path(self):
        pass

    def get_childnode_lists(self, path):
        """获取所有直接孩子节点的文本内容"""
        node = self.get_xpath_node(path)
        return [_.text for _ in node]

    def save(self):
        self.TREE.write(ENV_PATH, encoding="utf-8", xml_declaration=True)


def getEnvXmlObj():
    """获取对象"""
    return EnvParser(xml = os.path.join(BASE_DIR, ENV_PATH))

def getFontSize():
    """获取字体大小"""
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('page/font-size')
    return int(node.text)

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

def setPython3Env(path):
    """选择设置虚拟环境"""
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('env/python3')
    node.text = str(path)
    obj.save()

def getModelsAlias():
    """获取所有models.py的别名"""
    obj = getEnvXmlObj()
    return obj.get_childnode_lists('alias/file[name=models]')

def getAdminAlias():
    """获取所有admin.py的别名"""
    obj = getEnvXmlObj()
    return obj.get_childnode_lists('alias/file[name=admin]')

def getUrlsAlias():
    """获取所有urls.py的别名"""
    obj = getEnvXmlObj()
    return obj.get_childnode_lists('alias/file[name=urls]')

def getDjangoRunPort():
    """获取Django的运行端口"""
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('env/port')
    return int(node.text)

def getPython3Env():
    """获取项目运行虚拟环境"""
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('env/python3')
    return node.text if node.text else ''

def getPlatform():
    """获取当前运行的平台"""
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('env/platform')
    return node.text if node.text else ''

def setPlatfrom(name):
    """设置当前运行平台"""
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('env/platform')
    node.text = str(name)
    obj.save()

def getAllSupportPlatform():
    """获取软件已支持的平台类型"""
    obj = getEnvXmlObj()
    return obj.get_childnode_lists('env/support[name=all]')

def getSupportEnvPlatform():
    """获取软件已支持虚拟环境运行的平台类型"""
    obj = getEnvXmlObj()
    return obj.get_childnode_lists('env/support[name=virtualenv]')

def killProgress():
    """终止进程"""
    import subprocess, platform
    p = platform.system()
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

# print(root.tag) # 查看标签
# print(root.attrib) # 查看属性
# print(root.text) # 查看文本内容（不读取子标签）
# print(root[0][1].text) # 索引取值

# for child in root:
#     print(child.tag, child.attrib)


# 遍历所有子集
# for neighbor in root.iter('name'):
#     print('HHH: ', neighbor.attrib)


# 查找当前元素的直接子元素中带有特定标签的元素
# Element.findall("property")

# Element.find("property") 找带有特定标签的第一个子级
# Element.text 访问文本内容
# Element.get 访问元素的属性
