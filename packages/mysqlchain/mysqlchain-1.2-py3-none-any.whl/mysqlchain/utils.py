# @title   utils
# @since   2024/11/25 创建
# @author  lingfeng <418155641@qq.com>

import time
import calendar
from datetime import datetime, timedelta


def listTostr(list: list, cut: str = ' ') -> str:
    """ 列表转字符串 """
    sqlList = filter(None, list)
    return cut.join(sqlList)


def dictToList(dict: dict) -> list:
    """ 字典转列表 """
    res = ['(']
    for k, v in dict.items():
        res += [k, '=', filterParam(v), 'and']
    res[-1] = ')'
    return res


def listToList(list: list) -> list:
    """ 列表转列表 """
    res = ['(']
    for v in list:
        res += [v[0], v[1], filterParam(v[2]), 'and']
    res[-1] = ')'
    return res


def filterParam(param: any) -> str:
    """ 过滤参数 """
    if isinstance(param, str):
        return f"'{str(param).replace("'", "\\'")}'"
    else:
        return str(param)


def strtotime(str: str) -> int:
    """ 日期转时间戳 """
    stra = str.split(' ')
    if len(stra) == 1:
        str = stra[0] + ' 00:00:00'
    else:
        strb = stra[1].split(':')
        strblen = len(strb)
        if strblen == 1:
            str += ':00:00'
        elif strblen == 2:
            str += ':00'
    array = time.strptime(str, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(array))


def format_year_time(year: int) -> list:
    """ 获取某年的第一天和最后一天 """
    start = str(datetime(year, 1, 1))
    end = str(datetime(year + 1, 1, 1).date() - timedelta(days = 1)) + ' 23:59:59'
    return [strtotime(start), strtotime(end)]


def format_month_time(year: int, month: int) -> list:
    """ 获取某年某月的第一天和最后一天 """
    start = str(datetime(year, month, 1))
    end = str(datetime(year, month, calendar.monthrange(year, month)[1]).date()) + ' 23:59:59'
    return [strtotime(start), strtotime(end)]


def format_week_time(type: str) -> list:
    """ 获取本周或上周的第一天和最后一天 """
    now = datetime.now()
    if type == 'this week':
        start = str(now.date() - timedelta(days=now.weekday()))
        end = str(now.date() + timedelta(days = 6 - now.weekday())) + ' 23:59:59'
    else:
        start = str(now.date() - timedelta(days=now.weekday() + 7))
        end = str(now.date() - timedelta(days=now.weekday() + 1)) + ' 23:59:59'
    return [strtotime(start), strtotime(end)]


def format_weekday_time(year: int, month: int, day: int) -> list:
    """ 获取某天开始的一周的第一天和最后一天 """
    start = str(datetime(year, month, day))
    end = str(datetime(year, month, day).date() + timedelta(days = 6)) + ' 23:59:59'
    return [strtotime(start), strtotime(end)]


def format_day_time(date: str) -> list:
    """ 获取某天的开始和结束 """
    start = date
    end = date + ' 23:59:59'
    return [strtotime(start), strtotime(end)]


def formatWhere(where: list) -> str:
    """ 格式化条件 """
    if where:
        rwhere = []
        for w in where:
            w = list(filter(None, w))
            wlen = len(w)
            wlist = [w[0]]
            if wlen == 2:
                if isinstance(w[1], dict):
                    wlist += dictToList(w[1])
                elif isinstance(w[1], list):
                    wlist += listToList(w[1])
                else:
                    wlist += ['(', w[1], ')']
            elif wlen == 3:
                wlist += ['(', w[1], '=', filterParam(w[2]), ')']
            else:
                if 'like' in w[2]:
                    if isinstance(w[3], list):
                        wlist.append('(')
                        for v in w[3]:
                            wlist += [w[1], w[2], filterParam(v), 'and']
                        wlist[-1] = ')'
                    else:
                        wlist += [w[1], w[2], filterParam(w[3])]
                elif 'between' in w[2]:
                    wlist += [w[1], w[2], filterParam(w[3][0]), 'and', filterParam(w[3][1])]
                elif 'in' in w[2]:
                    if len(w[3]) == 1:
                        wlist += [w[1], '=', filterParam(w[3][0])]
                    else:
                        wlist += [w[1], w[2], str(tuple(w[3]))]
                else:
                    wlist += [w[1], w[2], filterParam(w[3])]
            rwhere += wlist
        rwhere[0] = 'where'
        return listTostr(rwhere)
    else:
        return ''


def formatInsertData(data: list) -> str:
    """ 格式化新增数据 """
    fields = list(data[0].keys())
    marks = ['%s' for x in range(0, len(fields))]
    fields = listTostr(fields, ', ')
    marks = listTostr(marks, ', ')
    return f'({fields}) values ({marks})'


def formatUpdateData(data: str, incOrDec: bool) -> str:
    """ 格式化更新数据 """
    if incOrDec:
        return f'{data[0]} = f{data[1]}'
    else:
        data = [f'{field} = {filterParam(value)}' for field, value in data.items()]
        return listTostr(data, ', ')


def formatUpdateAllData(data: list) -> str:
    """ 格式化批量更新数据 """
    fields = list(data[0].keys())
    marks = []
    for field in fields:
        if field != 'id':
            marks.append(f'{field} = %s')
    marks = listTostr(marks, ', ')
    return f'{marks} WHERE id = %s'
