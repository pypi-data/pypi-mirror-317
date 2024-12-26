# mysqlchain [![Version][version-badge]][version-link]

`mysqlchain` 是用链式方法操作mysql数据库的扩展包

### 安装

```
$ pip install mysqlchain
```

### 使用方法

```
from mysqlchain import chain

config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'testdata',
    'charset': 'utf8'
}
db = chain(config)
```

### 使用手册

[查看手册](https://www.kancloud.cn/lingfengcms/mysqlchain/2646275)

[version-badge]:   https://img.shields.io/badge/version-1.1-brightgreen.svg
[version-link]:    https://pypi.org/project/mysqlchain/