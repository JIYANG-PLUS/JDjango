__all__ = [
    'Code',
]
import string, random, re

class Code:
    CONTANST = string.ascii_letters + string.digits
    
    # 去除掉不易分辨的字符的随机串
    def get_code(self, n):
        t_str = ''
        length = self.len_constant
        for _ in range(n):
            t_str += self.easy_constant[random.randint(0, length-1)]
        return t_str
    
    # 全字符的随机串
    def get_code_complex(self, n):
        t_str = ''
        length = len(self.CONTANST)
        for _ in range(n):
            t_str += self.CONTANST[random.randint(0, length-1)]
        return t_str

    @property
    def len_constant(self):
        return len(self.easy_constant)

    @property
    def easy_constant(self):
        patt = re.compile(r'([iIl10oOzZ2]*?)')
        return patt.sub('', self.CONTANST)

class SensitiveKey:
    """敏感词汇"""
    SENSITIVE_KEY = [
        'admin',
    ]
    
    @property
    def keys(self):
        return self.SENSITIVE_KEY