import os, re
import xml.etree.ElementTree as ET

class XMLFileParserException(Exception): pass

class EnvParser:
    patt_match_xpath = re.compile(r'([a-z]+?)\[([a-z]+?)\]')

    def __init__(self, *args, **kwargs):
        if 'xml' in kwargs:
            self._init_tree(kwargs['xml'])
            self._init_root()
            if not self._check_ok():
                raise XMLFileParserException('文件不存在或XML格式不正确。')
        else:
            raise XMLFileParserException('XML文件读取异常。')

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

    def _check_ok(self):
        if not self.TREE or not self.ROOT:
            return False
        return True

    def get_xpath(self, xpath):
        xpath_split = xpath.split('/')

        return xpath_split

    def get_node_text(self):
        return self.ROOT[1][0].text


if __name__ == "__main__":
    e = EnvParser(xml = './environment.xml')
    o = e.get_xpath('path/json/prop[config]')
    print(o)
