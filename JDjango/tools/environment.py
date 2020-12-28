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
        for node in nodes:
            if attr in node.attrib and v == node.attrib[attr]:
                return node
        else:
            raise PathNotFoundException('路径不存在。')


    def get_node_text(self, node):
        return node.text

    def fill_base_path(self):
        pass

    def write_xml(self):
        self.TREE.write(ENV_PATH, encoding="utf-8", xml_declaration=True)

def getEnvXmlObj():
    return EnvParser(xml = os.path.join(BASE_DIR, ENV_PATH))

def getFontSize():
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('page/font-size')
    return int(node.text)

def setFontSize(step = 1, method = 'add'):
    obj = getEnvXmlObj()
    node = obj.get_xpath_node('page/font-size')
    font_size = int(node.text)
    if 'add' == method: 
        node.text = str(font_size + step)
    else:
        if font_size > 2:
            node.text = str(font_size - step)
    obj.write_xml()

# 参考
# 从字符串读取
# root = ET.fromstring(country_data_as_string)


# print(root.tag) # 查看标签
# print(root.attrib) # 查看属性
# print(root.text) # 查看文本内容（不读取子标签）
# print(root[0][1].text) # 索引取值


# 迭代子节点
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
