from django import template
import json, re
from collections import Iterable

register = template.Library()

@register.filter
def index(item, i):
    return item[i]

@register.filter
def multiply(item, v):
    return item*v

@register.filter
def split(item, v):
    return item.split(v)

@register.filter
def tojson(item):
    try:
        temp = json.loads(item)
    except:
        return []
    else:
        if isinstance(temp,Iterable):
            return temp
        else:
            return []

@register.filter
def my_in(item, v):
    if v in item: return True
    else: return False

@register.filter
def my_dict(item, v):
    return item[v]

@register.filter
def codeSplit(item):
    patt = r'^([$]+)(.+)$'
    result = re.match(patt, item)
    if None == result: return 0,item
    else: return len(result.group(1)), result.group(2)

@register.filter
def judgeVote(item, s_obj):
    obj = item.filter(suggest=s_obj)
    if len(obj) > 0:
        return obj[0].isvote
    else:
        return False
