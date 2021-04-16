import os, re

### HTML
patt_del_comment_html = re.compile(r'(<!--.*?-->)') # 删掉注释
patt_del_space_html = re.compile(r'(\s+)') # 删除多余的空格，只保留一个

### CSS
patt_del_comment_css = re.compile(r'(/[*].*?[*]/)')
patt_del_space_css = re.compile(r'(\s+)')

### JS
patt_del_comment_js = re.compile(r'(/[*].*?[*]/)')
patt_del_space_js = re.compile(r'(\s+)')

### JSON
patt_del_space_json = re.compile(r'(\s+)')

class FileTools:
    @classmethod
    def get_text_list(cls, path):
        if os.access(path, os.R_OK):
            with open(path, encoding='utf-8') as f:
                content = f.readlines()
            return [_.strip() for _ in content]
        else:
            return []

class Reducer:
    @classmethod
    def reduce_html(cls, path):
        list_text = FileTools.get_text_list(path)
        join_text = ''.join(list_text)
        clear_comment = patt_del_comment_html.sub('', join_text)
        clear_space = patt_del_space_html.sub(' ', clear_comment)
        return clear_space

    @classmethod
    def reduce_css(cls, path):
        list_text = FileTools.get_text_list(path)
        join_text = ''.join(list_text)
        clear_comment = patt_del_comment_css.sub('', join_text)
        clear_space = patt_del_space_css.sub(' ', clear_comment)
        return clear_space

    @classmethod
    def reduce_js(cls, path):
        list_text = FileTools.get_text_list(path)
        # 清除//注释的内容
        clear_double = []
        for _ in list_text:
            clear_double.append(_.split('//')[0].strip())
        join_text = ''.join(clear_double)
        clear_comment = patt_del_comment_js.sub('', join_text)
        clear_space = patt_del_space_js.sub(' ', clear_comment)
        return clear_space

    @classmethod
    def reduce_json(cls, path):
        list_text = FileTools.get_text_list(path)
        join_text = ''.join(list_text)
        return patt_del_space_json.sub(' ', join_text)

    @classmethod
    def html_save_to(cls, path):
        with open('./reduce.txt', 'w', encoding='utf-8') as f:
            f.write(cls.reduce_html(path))

    @classmethod
    def css_save_to(cls, path):
        with open('./reduce.txt', 'w', encoding='utf-8') as f:
            f.write(cls.reduce_css(path))
    
    @classmethod
    def js_save_to(cls, path):
        with open('./reduce.txt', 'w', encoding='utf-8') as f:
            f.write(cls.reduce_js(path))

    @classmethod
    def json_save_to(cls, path):
        with open('./reduce.txt', 'w', encoding='utf-8') as f:
            f.write(cls.reduce_json(path))

if __name__ == "__main__":
    os.chdir(r'C:\Users\PC\desktop')
    Reducer.json_save_to('./test.json')
