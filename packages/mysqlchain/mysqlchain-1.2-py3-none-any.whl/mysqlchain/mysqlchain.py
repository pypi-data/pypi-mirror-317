# @title   mysqlchain
# @since   2024/11/25 创建
# @author  lingfeng <418155641@qq.com>

import pymysql
import utils
import time
from typing import Union
from datetime import datetime, timedelta


class Chain:


    def __init__(self, config: dict = {}):
        """ 初始化 """
        default = {
            'host': 'localhost',
            'port': 3306,
            'user': '',
            'password': '',
            'database': '',
            'charset': 'utf8'
        }
        self.connect(dict(default, **config))


    def initParams(self):
        """ 初始化参数 """
        self.params = {
            'type': 'select',
            'distinct': '',
            'field': '',
            'from': 'from',
            'name': '',
            'alias': '',
            'force': '',
            'join': [],
            'union': [],
            'where': [],
            'group': '',
            'having': '',
            'order': '',
            'limit': '',
            'lock': '',
            'comment': ''
        }
        self.data = []
        self.ignoreStr = ''
        self.lastId = False
        self.incOrDec = False


    def connect(self, config: dict):
        """ 连接数据库 """
        try:
            self.db = pymysql.connect(host=config['host'],
                                      port=config['port'],
                                      user=config['user'],
                                      password=config['password'],
                                      database=config['database'],
                                      charset=config['charset'])
            self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        except Exception as e:
            raise ValueError(e)


    def formatSql(self, type: str) -> str:
        """ 格式化SQL语句 """
        if type == 'select':
            self.params['field'] = self.params['field'] if self.params['field'] else '*'
            self.params['join'] = utils.listTostr(self.params['join'])
            self.params['union'] = utils.listTostr(self.params['union'])
            self.params['where'] = utils.formatWhere(self.params['where'])
            sqlList = list(self.params.values())
            sql = utils.listTostr(sqlList)
        elif type == 'insert':
            dataField = utils.formatInsertData(self.data)
            sql = utils.listTostr(['insert', self.ignoreStr, 'into', self.params['name'], dataField])
        elif type == 'update':
            data = utils.formatUpdateData(self.data, self.incOrDec)
            where = utils.formatWhere(self.params['where'])
            sql = utils.listTostr(['update', self.params['name'], 'set', data, where])
        elif type == 'updateAll':
            dataField = utils.formatUpdateAllData(self.data)
            sql = utils.listTostr(['update', self.params['name'], 'set', dataField])
        elif type == 'delete':
            where = utils.formatWhere(self.params['where'])
            sql = utils.listTostr(['delete', 'from', self.params['name'], where])
        return sql


    def query(self, sql: str = '', mode: str = 'fetchall') -> any:
        """ 执行查询sql """
        try:
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
        except Exception as e:
            raise ValueError(e)
        else:
            if mode == 'fetchone':
                result = self.cursor.fetchone()
                if result:
                    return result
                else:
                    return {}
            elif mode == 'fetchall':
                result = self.cursor.fetchall()
                if result:
                    return result
                else:
                    return []
            else:
                return True


    def execute(self, sql: str, mode: str = None) -> any:
        """ 执行新增和更新sql """
        if mode == 'insert' or mode == 'updateAll':
            data = []
            if mode == 'insert':
                for val in self.data:
                    data.append(tuple(val.values()))
            else:
                for val in self.data:
                    transition = []
                    for k, v in val.items():
                        if k != 'id':
                            transition.append(v)
                    transition.append(val['id'])
                    data.append(tuple(transition))
            try:
                self.db.ping(reconnect=True)
                total = self.cursor.executemany(sql, data)
                self.db.commit()
                if self.lastId:
                    total = self.cursor.lastrowid
            except Exception as e:
                self.db.rollback()
                raise ValueError(e)
            else:
                return total
        else:
            try:
                self.db.ping(reconnect=True)
                result = self.cursor.execute(sql)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                raise ValueError(e)
            else:
                return result


    def distinct(self, distinct: bool = True) -> object:
        """ 指定DISTINCT查询 """
        if distinct:
            self.params['distinct'] = 'distinct'
        else:
            self.params['distinct'] = ''
        return self


    def field(self, field: str = '*') -> object:
        """ 指定查询字段 """
        if isinstance(field, list):
            self.params['field'] = ','.join(field)
        else:
            self.params['field'] = field
        return self


    def withoutField(self, field: str) -> object:
        """ 指定排除的查询字段 """
        columns = self.columnsInfo()
        fields = []
        for column in columns:
            fields.append(column['Field'])
        if isinstance(field, str):
            dfields = field.replace(' ','').split(',')
        else:
            dfields = field
        fields = list(filter(lambda v: v not in dfields, fields))
        if fields:
            self.params['field'] = ','.join(fields)
        return self


    def name(self, name: str) -> object:
        """ 指定数据表名 """
        self.initParams()
        self.params['name'] = name
        return self


    def alias(self, alias: str) -> object:
        """ 指定数据表别名 """
        self.params['alias'] = alias
        return self


    def force(self, force: str) -> object:
        """ 指定强制索引 """
        self.params['force'] = f'force index ({force})'
        return self


    def join(self, join: str, where: str) -> object:
        """ 指定INNER JOIN查询 """
        self.params['join'].append(f'inner join {join} on {where}')
        return self


    def leftJoin(self, join: str, where: str) -> object:
        """ 指定LEFT JOIN查询 """
        self.params['join'].append(f'left join {join} on {where}')
        return self


    def rightJoin(self, join: str, where: str) -> object:
        """ 指定RIGHT JOIN查询 """
        self.params['join'].append(f'right join {join} on {where}')
        return self


    def union(self, union: Union[str, list]) -> object:
        """ 指定UNION查询 """
        if isinstance(union, list):
            for val in union:
                self.params['union'].append(f'union ({val})')
        else:
            self.params['union'].append(f'union ({union})')
        return self


    def unionAll(self, union: Union[str, list]) -> object:
        """ 指定UNION ALL查询 """
        if isinstance(union, list):
            for val in union:
                self.params['union'].append(f'union all ({val})')
        else:
            self.params['union'].append(f'union all ({union})')
        return self


    def where(self, field: str, operator: str = None, value: str = None) -> object:
        """ 指定AND查询条件 """
        self.params['where'].append(['and', field, operator, value])
        return self


    def whereOr(self, field: str, operator: str = None, value: str = None) -> object:
        """ 指定OR查询条件 """
        self.params['where'].append(['or', field, operator, value])
        return self


    def whereTime(self, field: str, operator: str, range: Union[str, list]) -> object:
        """ 指定查询日期或时间 """
        if isinstance(range, str):
            self.params['where'].append(['and', field, operator, utils.strtotime(range)])
        else:
            self.params['where'].append(['and', field, operator, [utils.strtotime(range[0]), utils.strtotime(range[1])]])
        return self


    def whereBetweenTime(self, field: str, startTime: str, endTime: str) -> object:
        """ 指定查询日期或时间在范围内 """
        self.params['where'].append(['and', field, 'between', [utils.strtotime(startTime), utils.strtotime(endTime)]])
        return self


    def whereNotBetweenTime(self, field: str, startTime: str, endTime: str) -> object:
        """ 指定查询日期或时间不在范围内 """
        self.params['where'].append(['and', field, 'not between', [utils.strtotime(startTime), utils.strtotime(endTime)]])
        return self


    def whereBetweenTimeField(self, startField: str, endField: str) -> object:
        """ 指定查询当前时间在两个时间字段范围内 """
        nowtime = str(int(time.time()))
        self.params['where'].append(['and', startField, '<=', nowtime])
        self.params['where'].append(['and', endField, '>=', nowtime])
        return self


    def whereNotBetweenTimeField(self, startField: str, endField: str) -> object:
        """ 指定查询当前时间不在两个时间字段范围内 """
        nowtime = str(int(time.time()))
        self.params['where'].append(['or', startField, '>', nowtime])
        self.params['where'].append(['or', endField, '<', nowtime])
        return self


    def whereYear(self, field: str, year: str = 'this year') -> object:
        """ 指定查询年数据 """
        thisyear = datetime.now().year
        if year == 'this year':
            timeList = utils.format_year_time(thisyear)
        elif year == 'last year':
            timeList = utils.format_year_time(thisyear - 1)
        else:
            timeList = utils.format_year_time(year)
        self.params['where'].append(['and', field, 'between', timeList])
        return self


    def whereMonth(self, field: str, month: str = 'this month') -> object:
        """ 指定查询月数据 """
        thisyear = datetime.now().year
        thismonth = datetime.now().month
        if month == 'this month':
            timeList = utils.format_month_time(thisyear, thismonth)
        elif month == 'last month':
            timeList = utils.format_month_time(thisyear, thismonth - 1)
        else:
            year, month = month.split('-')
            timeList = utils.format_month_time(int(year), int(month))
        self.params['where'].append(['and', field, 'between', timeList])
        return self


    def whereWeek(self, field: str, week: str = 'this week') -> object:
        """ 指定查询周数据 """
        if week == 'this week' or week == 'last week':
            timeList = utils.format_week_time(week)
        else:
            year, month, day = week.split('-')
            timeList = utils.format_weekday_time(int(year), int(month), int(day))
        self.params['where'].append(['and', field, 'between', timeList])
        return self


    def whereDay(self, field: str, day: str = 'today') -> object:
        """ 指定查询天数据 """
        if day == 'today':
            date = str(date.today())
        elif day == 'yesterday':
            date = str(datetime.now().date() - timedelta(days = 1))
        else:
            date = day
        timeList = utils.format_day_time(date)
        self.params['where'].append(['and', field, 'between', timeList])
        return self


    def group(self, group: str) -> object:
        """ 指定group查询 """
        self.params['group'] = f'group by {group}'
        return self


    def having(self, having: str) -> object:
        """ 指定having查询 """
        self.params['having'] = f'having {having}'
        return self


    def order(self, order: str, sort: str = '') -> object:
        """ 指定排序规则 """
        if sort:
            self.params['order'] = f'order by {order} {sort}'
        else:
            self.params['order'] = f'order by {order}'
        return self


    def orderRand(self) -> object:
        """ 指定随机排序 """
        self.params['order'] = 'order by rand()'
        return self


    def limit(self, offset: str, length: int = 0) -> object:
        """ 指定查询条数 """
        if length:
            self.params['limit'] = f'limit {offset},{length}'
        else:
            self.params['limit'] = f'limit {offset}'
        return self


    def page(self, page: int, listRows: int) -> object:
        """ 指定分页 """
        offset = (page - 1) * listRows
        self.params['limit'] = f'limit {offset},{listRows}'
        return self


    def lock(self, lock: bool = True) -> object:
        """ 指定LOCK锁定 """
        if isinstance(lock, str):
            self.params['lock'] = lock
        else:
            self.params['lock'] = 'for update'
        return self


    def comment(self, comment: str) -> object:
        """ 指定查询注释 """
        self.params['comment'] = f'/* {comment} */'
        return self


    def ignore(self, ignore: bool = True) -> object:
        """ 指定是否忽略已存在的数据 """
        if ignore:
            self.params['ignore'] = 'ignore'
        else:
            self.params['ignore'] = ''
        return self


    def inc(self, field: str, step: int = 1) -> object:
        """ 指定字段自增更新 """
        self.data = [field, f'{field} + {str(step)}']
        self.incOrDec = True
        return self


    def dec(self, field: str, step: int = 1) -> object:
        """ 指定字段自减更新 """
        self.data = [field, f'{field} - {str(step)}']
        self.incOrDec = True
        return self


    def find(self) -> dict:
        """ 查询一条数据 """
        self.limit(1)
        sql = self.formatSql('select')
        return self.query(sql, 'fetchone')


    def select(self) -> list:
        """ 查询多条数据 """
        sql = self.formatSql('select')
        return self.query(sql)


    def value(self, field: str) -> any:
        """ 查询某个字段的值 """
        self.params['field'] = field
        data = self.find()
        if data:
            return data[field]


    def column(self, field: str, index: str = '') -> list:
        """ 查询某一列 """
        if isinstance(field, list):
            self.params['field'] = ','.join(field)
        else:
            self.params['field'] = field.replace(' ','')
        data = self.select()
        if data and index:
            ndata = {}
            for v in data:
                ndata[v[index]] = v
            return ndata
        else:
            return data


    def count(self, field: str = '*') -> int:
        """ count查询 """
        self.params['field'] = f'count({field}) as f_count'
        sql = self.formatSql('select')
        result = self.query(sql, 'fetchone')
        return result['f_count']


    def max(self, field: str) -> Union[int, float]:
        """ max查询 """
        self.params['field'] = f'max({field}) as f_max'
        sql = self.formatSql('select')
        result = self.query(sql, 'fetchone')
        return result['f_max']


    def min(self, field: str) -> Union[int, float]:
        """ min查询 """
        self.params['field'] = f'min({field}) as f_min'
        sql = self.formatSql('select')
        result = self.query(sql, 'fetchone')
        return result['f_min']


    def avg(self, field: str) -> Union[int, float]:
        """ avg查询 """
        self.params['field'] = f'avg({field}) as f_avg'
        sql = self.formatSql('select')
        result = self.query(sql, 'fetchone')
        return result['f_avg']


    def sum(self, field: str) -> Union[int, float]:
        """ sum查询 """
        self.params['field'] = f'sum({field}) as f_sum'
        sql = self.formatSql('select')
        result = self.query(sql, 'fetchone')
        return result['f_sum']


    def insert(self, data: dict) -> int:
        """ 新增单条数据 """
        if isinstance(data, dict):
            self.data = [data]
            sql = self.formatSql('insert')
            return self.execute(sql, 'insert')
        else:
            return 0


    def insertGetId(self, data: dict) -> int:
        """ 新增单条数据并获取ID """
        self.lastId = True
        return self.insert(data)


    def insertAll(self, data: list) -> int:
        """ 新增多条数据 """
        if isinstance(data, list):
            self.data = data
            sql = self.formatSql('insert')
            return self.execute(sql, 'insert')
        else:
            raise ValueError('data 必须是列表')


    def update(self, data: dict) -> int:
        """ 更新数据 """
        if isinstance(data, dict):
            self.data = data
            sql = self.formatSql('update')
            return self.execute(sql)
        else:
            raise ValueError('data 必须是字典')


    def updateAll(self, data: list) -> int:
        """ 更新多条数据(自动识别id主键) """
        if isinstance(data, list):
            all_have_id = all('id' in item for item in data)
            if all_have_id:
                self.data = data
                sql = self.formatSql('updateAll')
                return self.execute(sql, 'updateAll')
            else:
                raise ValueError('data 中必须包含id主键')
        else:
            raise ValueError('data 必须是列表')


    def delete(self, data: Union[list, bool] = None) -> int:
        """ 删除数据 """
        if not data is None:
            if isinstance(data, bool) and data == True:
                sql = self.formatSql('delete')
                return self.execute(sql)
            else:
                columns = self.columnsInfo()
                for column in columns:
                    if 'auto_increment' in column.values():
                        field = column['Field']
                        break
                if field:
                    if isinstance(data, list):
                        self.params['where'].append(['and', field, 'in', data])
                    else:
                        self.params['where'].append(['and', field, '=', data])
                    sql = self.formatSql('delete')
                    return self.execute(sql)
                else:
                    return 0
        elif self.params['where']:
            sql = self.formatSql('delete')
            return self.execute(sql)
        else:
            return 0


    def columnsInfo(self):
        """ 获取数据表的所有列信息 """
        sql = f'show full columns from {self.params['name']}'
        return self.query(sql)


    def truncate(self):
        """ 清空数据表 """
        sql = f'truncate table {self.params['name']}'
        return self.query(sql, 'truncate')


    def fetchSql(self):
        """ 输出sql """
        return self.formatSql('select')
