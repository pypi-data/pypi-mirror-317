# coding=utf-8

"""
@fileName       :   db_client_2.py
@data           :   2024/5/11
@author         :   jiangmenggui@hosonsoft.com
"""
from logging import Logger
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Iterable
import threading
from lljz_tools.log_manager import LogManager
from lljz_tools.color import Color







@dataclass
class DatabaseConfig:
    db_type: str
    user: str
    password: str
    host: str
    port: int
    db: str
    qs: dict = field(default_factory=dict)
    cursorclass: Any = None 
    charset: str = 'utf8mb4'


@dataclass
class SSHConfig:
    user: str
    password: str
    host: str
    port: int


def parse_db_uri(uri: str):
    """
    解析数据库连接字符串
    """
    obj = re.match(
        r'^(?P<db_type>.+)://(?P<user>.+):(?P<password>.+)@(?P<host>.+):(?P<port>\d+)/(?P<db>.+?)(?:\?(?P<qs>.+))?$',
        uri
    )
    if not obj:
        raise ValueError(
            f'{uri!r} 格式错误！期望的格式为：db_type://user:password@host:port/db?qs')
    database_config = obj.groupdict()
    if database_config['qs']:
        qs = {k: v for k, v in (i.split('=', maxsplit=1)
                                for i in database_config.pop('qs').split('&'))}
        database_config.update(qs=qs)
    else:
        database_config.pop('qs')
    database_config['port'] = int(database_config['port'])
    return DatabaseConfig(**database_config)  # type: ignore


sql_logger = LogManager(
    'print_sql', console_level='DEBUG', file_path=None
).get_logger()

ArgsType = list | tuple | None

# 创建一个线程局部存储对象
thread_local = threading.local()


class MySQLClient:
    """
    MySQL数据库连接池，支持ssh隧道连接
    """

    def __init__(self, uri: str, ssh_uri: str | None = None, show_sql: bool | Logger = True):
        """
        初始化MySQL连接池

        :param uri: MySQL连接字符串，格式：mysql://user:password@host:port/database
            - user: 用户名
            - password: 密码
            - host: 主机地址
            - port: 端口
            - database: 数据库名
        :param ssh_uri: SSH隧道连接字符串，格式：ssh://user:password@host:port
            - user: 用户名
            - password: 密码
            - host: 主机地址
            - port: 端口，端口可以省略，默认22
        :param show_sql: 是否显示SQL语句
        """
        try:
            import pymysql
            import pymysql.cursors
            from pymysql.cursors import DictCursor
            from dbutils.pooled_db import PooledDB
        except ImportError:
            raise ImportError(f'package not installed! use "{Color.color('pip install pymysql dbutils', style='i u yellow')}"')

        database_config = parse_db_uri(uri)
        database_config.cursorclass = DictCursor
        if database_config.db_type.upper() != 'MYSQL':
            raise ValueError(f'数据库类型必须为mysql，你输入的是{database_config.db_type!r}')
        self._ssh = None
        if show_sql is True:
            self.show_sql = sql_logger
        elif show_sql is False:
            self.show_sql = None
        else:
            self.show_sql = show_sql

        if ssh_uri:
            try:
                from lljz_tools.client.utils import setup_ssh_tunnel
            except ImportError:
                raise ImportError(f'package not installed! use "{Color.color('pip install sshtunnel', style='i u yellow')}"')

            
            self._ssh = setup_ssh_tunnel(database_config.host, database_config.port, ssh_uri)
            database_config.host = '127.0.0.1'
            database_config.port = self._ssh.local_bind_port
        database_config_dict = asdict(database_config)
        database_config_dict.pop('db_type')
        qs = database_config_dict.pop('qs')
        if 'autocommit' not in qs:
            qs['autocommit'] = True 
        elif qs['autocommit'] == 'false':
            qs['autocommit'] = False
        else:
            qs['autocommit'] = True

        # 创建连接池
        self._pool = PooledDB(
            creator=pymysql,
            # 其他参数根据你的应用需求调整
            mincached=1,
            maxcached=5,
            maxconnections=10,
            blocking=True,  # 如果没有可用连接，调用者将等待而不是抛出异常
            **qs,
            **database_config_dict
        )
        

    def close(self):
        self._pool.close()
        if self._ssh:
            self._ssh.stop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        # 检查当前线程是否已经有连接
        if not hasattr(thread_local, 'conn'):
            thread_local.conn = MySQLConnection(self._pool.connection(), self.show_sql)
        else:
            # 检查连接是否可用
            if not thread_local.conn.is_connected():
                thread_local.conn = MySQLConnection(self._pool.connection(), self.show_sql)  # 重新连接
        return thread_local.conn

    def select(self, sql: str, args: ArgsType = None, limit: int = 1000) -> list[dict[str, Any]]:
        return self.connect().select(sql, args, limit)

    def select_one(self, sql: str, args: ArgsType = None) -> dict[str, Any]:
        return self.connect().select_one(sql, args)
    
    def select_one_or_none(self, sql: str, args: ArgsType = None) -> dict[str, Any] | None:
        return self.connect().select_one_or_none(sql, args)

    def select_all(self, sql: str, args: ArgsType = None) -> list[dict[str, Any]]:
        return self.connect().select_all(sql, args)
    
    def insert(self, sql: str, args: ArgsType = None) -> int:
        return self.connect().insert(sql, args)

    def insert_data(self, table_name: str, data: Iterable[dict]) -> int:
        return self.connect().insert_data(table_name, data)
    
    def insert_many(self, sql: str, args: list[tuple | list] | tuple[list | tuple]) -> int:
        return self.connect().insert_many(sql, args)
    
    def update(self, sql: str, args: ArgsType = None) -> int:
        return self.connect().update(sql, args)
    
    def delete(self, sql: str, args: ArgsType = None) -> int:
        return self.connect().delete(sql, args)
    
    def commit(self):
        return self.connect().commit()
    
    def rollback(self):
        return self.connect().rollback()

class MySQLConnection:

    def __init__(self, conn, logger: Logger | None = None):
        self.conn = conn
        self._logger = logger

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def print_sql(self, sql: str, args: ArgsType = None):
        with self.conn.cursor() as cursor:
            self._print_sql(cursor, sql, args)

    def _print_sql(self, cursor: Any, sql: str, args: ArgsType = None):
        if not self._logger:
            return 
        try:
            self._logger.debug(cursor.mogrify(sql, args), stacklevel=3)
        except TypeError as e:
            self._logger.error(f'[ERROR SQL] sql: {sql}, args: {args}', stacklevel=3)
            self._logger.exception(e, stacklevel=3)

    def select(self, sql: str, args: ArgsType = None, limit: int = 1000) -> list[dict[str, Any]]:
        """
        查询数据，默认查询1000行

        :param sql: 查询语句
        :param args: 查询参数
        :param limit: 查询行数
        :return: 查询结果
        """
        sql = sql.lstrip()
        sql_type, _ = sql.split(maxsplit=1)
        if sql_type.upper() == 'SELECT':
            sql = f"SELECT * FROM ({sql}) t LIMIT {limit}"
        sql = sql.replace('?', '%s')
        with self.conn.cursor() as cursor:
            self._print_sql(cursor, sql, args)
            cursor.execute(sql, args)
            return cursor.fetchmany(limit)
        
    def select_one(self, sql: str, args: ArgsType = None) -> dict[str, Any]:
        data = self.select_one_or_none(sql, args)
        if not data:
            raise ValueError('query result is empty!')
        return data 

    def select_one_or_none(self, sql: str, args: ArgsType = None) -> dict[str, Any] | None:
        """
        查询一条数据

        :param sql: 查询语句
        :param args: 查询参数
        :return: 查询结果
        """
        sql = sql.lstrip()
        sql_type, _ = sql.split(maxsplit=1)
        if sql_type.upper() == 'SELECT':
            sql = f"SELECT * FROM ({sql}) t LIMIT 1"
        sql = sql.replace('?', '%s')
        
        with self.conn.cursor() as cursor:  
            self._print_sql(cursor, sql, args)
            cursor.execute(sql, args)
            return cursor.fetchone()

    def select_all(self, sql: str, args: ArgsType = None) -> list[dict[str, Any]]:
        """
        查询所有数据

        :param sql: 查询语句
        :param args: 查询参数
        :return: 查询结果
        """
        sql = sql.replace('?', '%s')
        with self.conn.cursor() as cursor:
            self._print_sql(cursor, sql, args)
            cursor.execute(sql, args)
            return cursor.fetchall()

    def insert(self, sql: str, args: ArgsType = None) -> int:
        """
        插入数据

        :param sql: 插入语句
        :param args: 插入参数
        :return: 插入的数据ID
        """
        sql = sql.lstrip()
        sql_type, _ = sql.split(maxsplit=1)
        if sql_type.upper() != 'INSERT':
            raise ValueError(f'NOT INSERT SQL: {sql}')
        sql = sql.replace('?', '%s')
        with self.conn.cursor() as cursor:
            self._print_sql(cursor, sql, args)
            cursor.execute(sql, args)
            return cursor.lastrowid

    def insert_data(self, table_name: str, data: Iterable[dict]) -> int:
        """
        插入数据

        :param table_name: 表名
        :param data: 数据
        :return: 插入行数
        """
        data = tuple(data)
        if not data:
            raise ValueError('data不能为空')
        sql = f"INSERT INTO {table_name} ({', '.join(data[0].keys())}) VALUES ({', '.join(['%s'] * len(data[0]))})"
        with self.conn.cursor() as cursor:
            self._print_sql(cursor, sql, data)
            cursor.executemany(sql, data)
            return cursor.rowcount
        
    def insert_many(self, sql: str, args: list[tuple | list] | tuple[list | tuple]) -> int:
        """
        批量插入数据

        :param sql: 插入语句
        :param args: 插入参数
        :return: 插入行数
        """
        sql = sql.lstrip()
        sql_type, _ = sql.split(maxsplit=1)
        if sql_type.upper() != 'INSERT':
            raise ValueError(f'NOT INSERT SQL: {sql}')
        sql = sql.replace('?', '%s')
        with self.conn.cursor() as cursor:
            for arg in args:
                self._print_sql(cursor, sql, arg)
            cursor.executemany(sql, args)
            return cursor.rowcount

    def update(self, sql: str, args: ArgsType = None) -> int:
        """
        更新数据

        :param sql: 更新语句
        :param args: 更新参数
        :return: 更新行数
        """
        sql = sql.lstrip()
        sql_type, _ = sql.split(maxsplit=1)
        if sql_type.upper() != 'UPDATE':
            raise ValueError(f'NOT UPDATE SQL: {sql}')
        sql = sql.replace('?', '%s')
        with self.conn.cursor() as cursor:
            self._print_sql(cursor, sql, args)
            cursor.execute(sql, args)
            return cursor.rowcount

    def delete(self, sql: str, args: ArgsType = None) -> int:
        """
        删除数据

        :param sql: 删除语句
        :param args: 删除参数
        :return: 删除行数
        """
        sql = sql.lstrip()
        sql_type, _ = sql.split(maxsplit=1)
        if sql_type.upper() != 'DELETE':
            raise ValueError(f'NOT DELETE SQL: {sql}')
        sql = sql.replace('?', '%s')
        with self.conn.cursor() as cursor:
            self._print_sql(cursor, sql, args)
            cursor.execute(sql, args)
            return cursor.rowcount

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def is_connected(self) -> bool:
        """检查连接是否可用"""
        try:
            self.conn.ping(reconnect=False)  # 检查连接状态
            return True
        except Exception:
            return False


if __name__ == '__main__':
    pass
