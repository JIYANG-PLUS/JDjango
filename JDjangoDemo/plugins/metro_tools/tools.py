"""
2020年02月06号
tools.Searcher.get_all_ways('2号线','学则路站','1号线','南京站') # 提供详细信息
tools.Searcher.lack_endline_get_all_ways('2号线','学则路站','南京站') # 缺少终点线路名称
tools.Searcher.lack_begin_and_endline_get_all_ways('雨山路站','金牛湖站') # 缺少起始和终点线路名称
tools.Searcher.lack_beginline_get_all_ways('学则路站','1号线','南京站') # 缺少起始线路名称
# 便捷函数
tools.get_all_ways(
        begin_station = '学则路站', # 必选
        end_station = '南京站', # 必选
        begin_line = '2号线', # 可选
        end_line = '1号线' # 可选
    )
"""

from .metro_data import *
from typing import Tuple,Set
import itertools as iters
from collections import deque

__all__ = [
    'NANJIN_METRO_BASE_INFO',

    'get_all_lines_name',
    'get_one_line_stations',

    'TOTAL_LINES',
    'get_all_ways',

    'Searcher',
]

def get_all_lines_name()->Tuple:
    return tuple(NANJIN_METRO_BASE_INFO.keys())

def get_one_line_stations(line)->Tuple:
    return NANJIN_METRO_BASE_INFO[line]['STATIONS']

def _search_all_cross_station()->Set:
    lines = get_all_lines_name()
    stations = []
    for line in lines: stations.extend(get_one_line_stations(line))
    temp,cross_stations = set(),set()
    for station in stations:
        if station in temp: cross_stations.add(station)
        else: temp.add(station)
    return cross_stations

# 每个中转站都属于哪些线
def _match_belong_lines():
    lines = get_all_lines_name()
    station_to_lines = dict(
        zip(CROSS_STATIONS,[[] for i in range(len(CROSS_STATIONS))])
    ) # 中转站属于哪些线
    for cross_station in CROSS_STATIONS:
        for line in lines:
            if cross_station in NANJIN_METRO_BASE_INFO[line]['STATIONS']:
                station_to_lines[cross_station].append(line)
    return station_to_lines

# 每条线包含哪些中转站
def _match_belong_stations():
    lines = get_all_lines_name()
    line_to_stations = dict(
        zip(lines,[[] for i in range(len(lines))])
    ) # 线包含哪些中转站
    for line in lines:
        for cross_station in CROSS_STATIONS:
            if cross_station in NANJIN_METRO_BASE_INFO[line]['STATIONS']:
                line_to_stations[line].append(cross_station)
    return line_to_stations

# 线路认识关系
def _line_known_lines():
    lines = tuple(LINE_RELATED_STATIONS.keys())
    line_known_lines = dict(
        zip(lines,[set() for i in range(len(lines))])
    )
    for line in lines:
        for station in LINE_RELATED_STATIONS[line]:
            for l,s_list in LINE_RELATED_STATIONS.items():
                if station in s_list:
                    line_known_lines[line].add(l)
    return {k:tuple(sorted([_ for _ in v if _ != k],reverse=False)) for k,v in line_known_lines.items()}

TOTAL_LINES = len(get_all_lines_name()) # 总计线路数量

#####################################################################
# 以下常量在地铁线路增加或者站数增加时启用。建议将从metro_data.py导入的常量屏蔽。
# 可以重新放到一个模块里当做训练数据的工具使用。
# 
# CROSS_STATIONS = _search_all_cross_station()
# STATION_RELATED_LINES = _match_belong_lines()
# LINE_RELATED_STATIONS = _match_belong_stations()
# LINE_KNOWN_LINES = _line_known_lines()
# 
#####################################################################

class Searcher:
    all = []

    class Line:
        def __init__(self,name,control,t_str):
            self.name = name
            self.control = control
            self.t_str = t_str

    @classmethod
    def _dfs_abstract_search_ways(cls,begin_line,end_line,control,result=''):
        """
        测试递归函数，不推荐使用
        退出条件前提：一定且绝对有通路。
        """
        for line in LINE_KNOWN_LINES[begin_line]:
            if line != end_line:
                if line not in control:
                    cls._dfs_abstract_search_ways(
                        line,end_line,
                        control.union({line}),
                        f'{result}${line}'
                    )
            else: cls.all.append(f'{result}${line}')

    @classmethod
    def re_get_abstract_ways(cls,begin_line,end_line):
        """消除递归，线路编码集"""
        if begin_line == end_line:
            return ['myself',begin_line]
        results = []
        check_stack = [cls.Line(_,{begin_line,},begin_line) for _ in LINE_KNOWN_LINES[begin_line]]
        while check_stack:
            pop_line = check_stack.pop() # 出栈
            if pop_line.name != end_line:
                if pop_line.name not in pop_line.control:
                    check_stack.extend(
                        [cls.Line(_,pop_line.control.union((pop_line.name,)),f'{pop_line.t_str}${pop_line.name}') for _ in LINE_KNOWN_LINES[pop_line.name]]
                    )
            else: results.append(f'{pop_line.t_str}${pop_line.name}')
        return results or [None]
        
    @classmethod
    def get_abstract_ways(cls,begin_line,end_line):
        """不推荐使用"""
        cls.all.clear() # 清空数据集
        cls._dfs_abstract_search_ways(begin_line,end_line,{begin_line,},result=begin_line)
        return cls.all

    @classmethod
    def get_real_way(cls,abstract_line,begin_station,end_station):
        """异线路解码"""
        results = cls._explain_one_abstract_way(abstract_line,begin_station,end_station)
        r_1,r_2 = results[0].split('#'),results[1].split('#')
        t_str = f'（{r_1[1]}出发）'
        lines = list(NANJIN_METRO_BASE_INFO[r_1[1]]['STATIONS'])
        if lines.index(r_1[0])>lines.index(r_2[0])+1: lines.reverse()
        t_str += '-->'.join(lines[lines.index(r_1[0]):lines.index(r_2[0])+1])
        for i in range(1,len(results)-1):
            r_1,r_2 = results[i].split('#'),results[i+1].split('#')
            exchange = r_1[1].split('_TO_')
            lines = list(NANJIN_METRO_BASE_INFO[exchange[1]]['STATIONS'])
            t_str += f'（{exchange[0]}_转_{exchange[1]}）-->'
            if lines.index(r_1[0])+1>lines.index(r_2[0])+1: lines.reverse()
            t_str += '-->'.join(lines[lines.index(r_1[0])+1:lines.index(r_2[0])+1])
        t_str += f"（{results[-1].split('#')[1]}到达）"
        if (end_station in t_str.split('-->')): # 防止自己经过自己（此处算法需改进）
            return ''
        else:
            return t_str
    
    @classmethod
    def get_real_way_by_same_line(cls,line,begin_station,end_station):
        """同线路解码"""
        lines = list(NANJIN_METRO_BASE_INFO[line]['STATIONS'])
        t_str = f'（{line}出发）'
        if lines.index(begin_station)>lines.index(end_station): lines.reverse() # 纠正行进方向
        t_str += '-->'.join(lines[lines.index(begin_station):lines.index(end_station)+1])
        t_str += f"（{line}到达）"
        return t_str

    @classmethod
    def get_all_ways(cls,begin_line,begin_station,end_line,end_station):
        original_data = cls.re_get_abstract_ways(begin_line,end_line)
        if original_data[0] == 'myself':
            return [cls.get_real_way_by_same_line(original_data[1],begin_station,end_station),]
        all_abstract_ways = sorted(original_data,key=lambda _:len(_.split('$'))) # 按照转站次数从低到高排序
        all_lines = []
        for abstract_line in all_abstract_ways:
            t_way = cls.get_real_way(abstract_line,begin_station,end_station)
            if '' != t_way: all_lines.append(t_way)
        return all_lines

    @classmethod
    def lack_endline_get_all_ways(cls,begin_line,begin_station,end_station):
        lines = get_all_lines_name()
        end_lines = []
        for l in lines:
            if end_station in get_one_line_stations(l): end_lines.append(l)
        all_lines = []
        for end_line in end_lines:
            all_lines.extend(cls.get_all_ways(begin_line,begin_station,end_line,end_station))
        return all_lines

    @classmethod
    def lack_beginline_get_all_ways(cls,begin_station,end_line,end_station):
        lines = get_all_lines_name()
        begin_lines = []
        for l in lines:
            if begin_station in get_one_line_stations(l): begin_lines.append(l)
        all_lines = []
        for begin_line in begin_lines:
            all_lines.extend(cls.get_all_ways(begin_line,begin_station,end_line,end_station))
        return all_lines

    @classmethod
    def lack_begin_and_endline_get_all_ways(cls,begin_station,end_station):
        lines = get_all_lines_name()
        begin_lines,end_lines = [],[]
        for l in lines:
            stations = get_one_line_stations(l)
            if end_station in stations: end_lines.append(l)
            if begin_station in stations: begin_lines.append(l)
        all_lines = []
        for begin_line in begin_lines:
            for end_line in end_lines:
                all_lines.extend(cls.get_all_ways(begin_line,begin_station,end_line,end_station))
        return all_lines

    @classmethod
    def _get_two_line_cross_station(cls,line1,line2):
        """基于常识：两条线路不可能有两个交点（不符合现实）"""
        stations = LINE_RELATED_STATIONS[line1]+LINE_RELATED_STATIONS[line2]
        check = set()
        for s in stations:
            if s in check: return s
            else: check.add(s)

    @classmethod
    def _explain_one_abstract_way(cls,abstract_line,begin_station,end_station):
        """解码内核"""
        split_lines = abstract_line.split('$') # 抽象线路的分解
        result = [f'{begin_station}#{split_lines[0]}',]
        # 两两一组
        for i in range(len(split_lines)-1):
            line1,line2 = split_lines[i],split_lines[i+1]
            cross_station = cls._get_two_line_cross_station(line1,line2)
            result.append(f'{cross_station}#{line1}_TO_{line2}')
        result.append(f'{end_station}#{split_lines[-1]}')
        return result

    @classmethod
    def get_all_ways_common(cls,begin_station=None,end_station=None,begin_line=None,end_line=None):
        if None == begin_station or None == end_station: return []
        if None == begin_line and None == end_line:
            return cls.lack_begin_and_endline_get_all_ways(begin_station,end_station)
        if None == begin_line:
            return cls.lack_beginline_get_all_ways(begin_station,end_line,end_station)
        if None == end_line:
            return cls.lack_endline_get_all_ways(begin_line,begin_station,end_station)
        return cls.get_all_ways(begin_line,begin_station,end_line,end_station)

# 全局便利函数
get_all_ways = Searcher.get_all_ways_common
