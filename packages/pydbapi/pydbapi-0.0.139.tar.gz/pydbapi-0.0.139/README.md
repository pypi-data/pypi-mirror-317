# pydbapi

## Installation
```python
pip install pydbapi
```

## 支持的数据库类型
+ sqlite
```python
from pydbapi.api import SqliteDB
db = SqliteDB(database=None)  # 或者传入路径
sql = 'select * from [table];'
cursor, action, result = db.execute(sql)
```
+ Amazon Redshift
```python
from pydbapi.api import RedshiftDB
db = RedshiftDB(host, user, password, database, port='5439', safe_rule=True)
sql = 'select * from [schema].[table];'
cursor, action, result = db.execute(sql)
```
+ Mysql
```python
from pydbapi.api import MysqlDB
db = MysqlDB(host, user, password, database, port=3306, safe_rule=True, isdoris=False)
sql = 'select * from [table];'
cursor, action, result = db.execute(sql)
```
+ Trino
```python
from pydbapi.api import TrinoDB
db = TrinoDB(host, user, password, database, catalog, port=8443, safe_rule=True)
sql = 'select * from [table];'
cursor, action, result = db.execute(sql)
```
+ Snowflake(删除)
```python
from pydbapi.api import SnowflakeDB
db = SnowflakeDB(user, password, account, warehouse, database, schema, safe_rule=True)
sql = 'select * from [table];'
cursor, action, result = db.execute(sql)
```

+ instance模式
```python
from pydbapi.api import SqliteDB
db = SqliteDB.get_instance(database=None)  # 或者传入路径
sql = 'select * from [table];'
cursor, action, result = db.execute(sql)
```

## Result
+ 转换成dataframe
```python
from pydbapi.api import TrinoDB
db = TrinoDB(host, user, password, database, catalog, port=8443, safe_rule=True)
sql = 'select * from [table];'
cursor, action, result = db.execute(sql)

df = result.to_dataframe()
df
```
+ 输出到csv
```python
from pydbapi.api import TrinoDB
db = TrinoDB(host, user, password, database, catalog, port=8443, safe_rule=True)
sql = 'select * from [table];'
cursor, action, result = db.execute(sql)

result.to_csv(outfile)
```

## Column
`from pydbapi.model import ColumnModel`
+ ColumnModel
    + 代码
        `col = ColumnModel(newname, coltype='varchar', sqlexpr=None, func=None, order=0)`
    + params
        * `newname`: 新命名；
        * `coltype`: 类型
        * `sqlexpr`: 查询sql表达式
        * `func`: 查询函数，暂时支持'min', 'max', 'sum', 'count'
        * `order`: 排序

+ ColumnsModel
    + 代码
        `cols = ColumnsModel(ColumnModel, ColumnModel, ……)`
    + property
        * `func_cols`: 返回col列表
        * `nonfunc_cols`: 返回col列表
        * `new_cols`: 返回拼接字符串
        * `create_cols`: 返回拼接字符串
        * `select_cols`: 返回拼接字符串
        * `group_cols`: 返回拼接字符串
        * `order_cols`: 返回拼接字符串
    + mothed
        * get_column_by_name
            - `cols.get_column_by_name(name)`
            - 返回`ColumnModel`
            
## Sql
+ SqlStatement
```python
from pydbapi.sql import SqlStatement
sql = 'select * from tablename where part_date >= $part_date;'
sqlstmt = SqlStatement(sql)
```

+ **属性**  

    - tokens  
    - sql
    - comment
    - action
    - tablename
    - params
    - subqueries

+ **方法**  

    + from_sqlsnippets
    ```python
    sstmt1 = '-- comment'
    sqlstmt = SqlStatement.from_sqlsnippets(sstmt1, sql)
    ```
    + add
    ```python
    sstmt2 = 'and part_date <= $end_date'
    sqlstmt += sstmt2
    ```
    + sub
    ```python
    sqlstmt -= sstmt2
    ```
    + substitute_params
    ```python
    sqlstmt = sqlstmt.substitute_params(part_date="'2024-01-01'")
    ```
    + get_with_testsql(only support CETs)
    ```python
    sqlstmt = sqlstmt.get_with_testsql(idx=1)
    ```

+ SqlStatements
```python
from pydbapi.sql import SqlStatements
sql = '''
    select * from tablename1 where part_date >= $part_date;
    select * from tablename2 where part_date >= $part_date;
'''
sqlstmts = SqlStatements(sql)
```

+ **属性**  

    - statements  
    - SqlStatement的属性

+ **方法**  

    + SqlStatement
    ```python
    sqlstmts = sqlstmts.substitute_params(part_date='2024-01-01')
    ```
    + iter
    ```python
    for stmts in sqlstmts:
        stmts
    ```
    - len
    ```python
    len(sqlstmts)
    ```
    - getitem
    ```python
    sqlstmts[0]
    sqlstmts[:2]
    ```


## 支持的操作
+ execute[【db/base.py】](https://github.com/longfengpili/pydbapi/blob/master/pydbapi/db/base.py)
    + 代码  
        `db.execute(sql, count=None, ehandling=None, verbose=0)`
    + params
        * `count`: 返回结果的数量;
        * `ehandling`: sql执行出错的时候处理方式, default: None
        * `verbose`: 执行的进度展示方式（0：不打印， 1：文字进度， 2：进度条）
+ select
    + 代码  
        `db.select(tablename, columns, condition=None, verbose=0)`
    + params
        * `tablename`: 表名;
        * `columns`： 列内容; 
        * `condition`: sql where 中的条件
+ create
    + sqlite/redshift
        + 代码  
        `db.create(tablename, columns, indexes=None, verbose=0)`
        + params
            - `tablename`: 表名;
            - `columns`： 列内容;
            - `indexes`: 索引，sqlite暂不支持索引
            - `verbose`： 是否打印执行进度。
    + mysql
        + 代码  
        `db.create(tablename, columns, indexes=None, index_part=128, ismultiple_index=True, partition=None, verbose=0)`
        + params
            - `tablename`: 表名;
            - `columns`： 列内容;
            - `indexes`: 索引
            - `index_part`: 索引part
            - `ismultiple_index`: 多重索引
            - `partition`: 分区
            - `verbose`： 是否打印执行进度。
    + trino
        + 代码  
        `db.create(tablename, columns, partition=None, verbose=0)`
        + params
            - `tablename`: 表名;
            - `columns`： 列内容;
            - `partition`: 分区
            - `verbose`： 是否打印执行进度。
+ insert[【db/base.py】](https://github.com/longfengpili/pydbapi/blob/master/pydbapi/db/base.py)
    + 代码  
        `db.insert(tablename, columns, inserttype='value', values=None, chunksize=1000, fromtable=None, condition=None)`
    + params
        * `tablename`: 表名;
        * `columns`： 列内容;
        * `inserttype`: 插入数据类型，支持value、select
        * `values`: inserttype='value',插入的数值; 
        * `chunksize`: inserttype='value', 每个批次插入的量级; 
        * `fromtable`: inserttype='select',数据来源表;
        * `condition`:  inserttype='select',数据来源条件;
+ drop[【db/base.py】](https://github.com/longfengpili/pydbapi/blob/master/pydbapi/db/base.py)
    + 代码  
        `db.drop(tablename)`
    + params
        * `tablename`: 表名;
+ delete[【db/base.py】](https://github.com/longfengpili/pydbapi/blob/master/pydbapi/db/base.py)
    + 代码  
        `db.delete(tablename, condition)`
    + params
        * `tablename`: 表名;
        * `condition`: 插入的数值; 
+ get_columns
    + 代码  
        `db.get_columns(tablename)`
    + params
        * `tablename`: 表名;
+ add_columns
    + 代码  
        `db.add_columns(tablename, columns)`
    + params
        * `tablename`: 表名;
        * `columns`： 列内容; 
+ get_filesqls[【db/fileexec.py】](https://github.com/longfengpili/pydbapi/blob/master/pydbapi/db/fileexec.py)
    + 代码  
        `db.get_filesqls(filepath, **kw)`
    + params
        * `filepath`: sql文件路径;
        * `kw`： sql文件中需要替换的参数，会替换sqlfile中的arguments;
+ file_exec[【db/fileexec.py】](https://github.com/longfengpili/pydbapi/blob/master/pydbapi/db/fileexec.py)
    + 代码  
        `db.file_exec(filepath, ehandling=None, verbose=0, **kw)`
    + params
        * `filepath`: sql文件路径; 文件名以<font color=red>`test`</font>开始或者结尾会打印sql执行的步骤;
        * `ehandling`: sql执行出错的时候处理方式, default: None
        * `verbose`: 执行的进度展示方式（0：不打印， 1：文字进度， 2：进度条）
        * `kw`： sql文件中需要替换的参数 在sql文件中用`$param`, 会替换sqlfile中的arguments;
    + sql文件格式(在desc中增加<font color=red>`verbose`</font>会打印sql执行的步骤;)
        ```sql
        #【arguments】#
        ts = '2020-06-28'
        date = today
        date_max = date + timedelta(days=10)
        #【arguments】#
        ###
        --【desc1 [verbose]】 #sql描述
        --step1
        sql1;
        --step2
        sql2 where name = $name;
        ###
        ###
        --【desc2 [verbose]】 #sql描述
        --step1
        sql1;
        --step2
        sql2;
        ###
        ```
    + arguments
        * 支持python表达式（datetime、date、timedelta）
        * 支持全局变量和当前sqlfile设置过的变量
        * now：获取执行的时间
        * today: 获取执行的日期

## 魔法命令
+ 注册方法  
命令行中执行`pydbapimagic`

+ 参数
    * 帮助  
    `%dbconfig`
    * 配置  
        ```python
        %dbconfig DBTYPE = 'mysql'
        %dbconfig HOST = 'localhost'
        %dbconfig USER = 'longfengpili'
        %dbconfig PASSWORD = '123456abc'
        %dbconfig DATABASE = 'test'
        %dbconfig PORT = 3306
        ```
    * 查看  
    `%dbconfig DBTYPE`

## 支持的的settings[【conf/settings.py】](https://github.com/longfengpili/pydbapi/blob/master/pydbapi/conf/logconf.py)
+ AUTO_RULES  
    可以自动执行表名（表名包含即可）
