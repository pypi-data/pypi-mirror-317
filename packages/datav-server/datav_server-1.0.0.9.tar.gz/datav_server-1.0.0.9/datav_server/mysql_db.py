import time
import traceback
from typing import List

import mysql.connector
import sqlparse
from sqlparse.sql import TokenList, Identifier, IdentifierList

from datetime import datetime
import mysql.connector.pooling

from datav_server.common_db import CommonDatabase


class MySQLConnectionPool:
    def __init__(self, host, port, user, password, database, pool_size=5):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.pool_size = pool_size
        self._create_pool()

    def _create_pool(self):
        # """创建连接池"""
        config = {
            'database': self.database,
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'port': self.port,
            'pool_size': self.pool_size,  # 连接池中的连接数
            'ssl_disabled': True
            # 'max_idle_time': 300  # 连接最大空闲时间（秒）
        }

        self.pool = mysql.connector.pooling.MySQLConnectionPool(**config)
        # self.pool = []
        # try:
        #     for _ in range(self.pool_size):
        #         conn = mysql.connector.connect(
        #             host=self.host,
        #             port=self.port,
        #             user=self.user,
        #             password=self.password,
        #             database=self.database
        #         )
        #         self.pool.append(conn)
        # except Error as e:
        #     print(f"Error while creating MySQL connection pool: {e}")

    def get_connection(self):
        """从池中获取一个连接"""
        if not self.pool:
            raise Exception("No available connections")
        return self.pool.get_connection()

    def release_connection(self, conn):
        """将连接放回池中"""
        conn.close()


class MySQLDatabase(CommonDatabase):
    key_words = ["desc"]
    """MySQL 数据库操作类"""

    def __init__(self, host, port, user, password, database, is_commit=True, pool_size=5):
        from datav_server.db_factory import global_pools
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        if global_pools:
            self.pool = global_pools
        else:
            self.pool = MySQLConnectionPool(host, port, user, password, database)
        self.connection = None
        self.cursor = None
        self.is_commit = is_commit

    def table_exists(self,table_name):
        """
        判断 表是否存在
        """
        check_table_exists_sql = f"select table_name from information_schema.`TABLES` where table_schema='{self.database}' and table_type='BASE TABLE' and lower(table_name) = '{table_name}';"
        self.cursor.execute(check_table_exists_sql)
        existing_table = [row[0] for row in self.cursor.fetchall()]
        if existing_table:
            return True
        else:
            return False

    def connect(self):
        """连接到MySQL数据库"""
        self.connection = self.pool.get_connection()
        self.cursor = self.connection.cursor()

    def disconnect(self):
        """断开与MySQL数据库的连接"""
        if self.connection:
            self.pool.release_connection(self.connection)
            self.connection = None
            self.cursor = None

    def create_table(self, table_name, columns: str):
        """创建表格"""
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(sql)
        if self.is_commit:
            self.connection.commit()

    def executesql(self, sql: str):
        """执行SQL语句"""
        self.cursor.execute(sql)
        if self.is_commit:
            self.connection.commit()

    def drop_table(self, table_name):
        """删除表格"""
        sql = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(sql)
        if self.is_commit:
            self.connection.commit()

    def insert_data(self, table_name, data: dict):
        columns = ""
        for column_name in data.keys():
            if column_name.lower() in self.key_words:
                column_name = f"`{column_name}`"
            columns += column_name + ","
        columns = columns[:-1]
        """插入数据"""
        placeholders = ', '.join(['%s' for _ in data.keys()])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, tuple(data.values()))
        if self.is_commit:
            self.connection.commit()

    def insert_datas(self, table_name, data: list):
        """插入多条数据"""
        if not data:
            return
        columns = ""
        for column_name in data[0].keys():
            if column_name.lower() in self.key_words:
                column_name = f"`{column_name}`"
            columns += column_name + ","
        columns = columns[:-1]
        placeholders = ', '.join(['%s' for _ in data[0].keys()])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        values = [tuple(item.values()) for item in data]
        self.cursor.executemany(sql, values)
        if self.is_commit:
            self.connection.commit()

    def update_data(self, table_name, data: dict, condition):
        """更新数据"""
        set_clause = ""
        for key in data.keys():
            if key.lower() in self.key_words:
                key = f"`{key}`"
            set_clause += f"{key} = %s,"
        set_clause = set_clause[:-1]
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        self.cursor.execute(sql, tuple(data.values()))
        if self.is_commit:
            self.connection.commit()

    def update_datas(self, table_name, data: list, condition):
        """更新多条数据"""
        if not data:
            return
        set_clause = ""
        for key in data[0].keys():
            if key.lower() in self.key_words:
                key = f"`{key}`"
            set_clause += f"{key} = %s,"
        set_clause = set_clause[:-1]
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        values = [tuple(item.values()) for item in data]
        self.cursor.executemany(sql, values)
        if self.is_commit:
            self.connection.commit()

    def delete_data(self, table_name, condition):
        """删除数据"""
        sql = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(sql)
        if self.is_commit:
            self.connection.commit()

    def select_data(self, table_name, columns=None, condition=None):
        """
        查询数据
        :param table_name: 字符串
        :param columns: 字符串逗号分割
        :param condition: "id = '1' and name = '2'"
        :return:
        """
        if columns is None:
            columns = '*'
        if condition is None:
            condition = ''
        else:
            condition = f"WHERE {condition}"
        sql = f"SELECT {columns} FROM {table_name} {condition}"
        print(f"执行脚本====》{sql}")

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def select_json_data(self, table_name, columns=None, condition=None):
        """查询数据 返回格式为 key-value 格式"""
        if columns is None:
            columns = '*'
        if condition is None:
            condition = ''
        else:
            condition = f"WHERE {condition}"
        sql = f"SELECT {columns} FROM {table_name} {condition}"

        print(f"执行脚本--》 {sql}")
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        datas = []
        if len(rows) == 0:
            return datas
        column_names = [description[0].decode('utf-8') if isinstance(description[0], bytes) else description[0] for
                        description in self.cursor.description]
        for row in rows:
            dict_data = {}
            for idx in range(len(column_names)):
                key = column_names[idx]
                value = row[idx]
                if isinstance(row[idx], datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                dict_data[key] = value
            datas.append(dict_data)

        return datas

    def get_create_table(self, table_name):
        """获取创建表的 SQL 语句"""
        sql = f"SHOW CREATE TABLE {table_name}"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res[0][1]  # `SHOW CREATE TABLE` 返回的第二列是创建表的 SQL

    def get_cols_by_table_name(self, table_name):
        """获取表的列信息"""
        sql = f"DESCRIBE {table_name}"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def select_data_with_sql(self, sql):
        print(f"传入查询脚本====》{sql}")
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def select_json_data_by_sql(self, sql):
        print("传入查询脚本--》 {}", sql)
        sql = self.adapt_sql_for_framework(sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        datas = []
        if len(rows) == 0:
            return datas
        column_names = [description[0].decode('utf-8') if isinstance(description[0], bytes) else description[0] for
                        description in self.cursor.description]
        for row in rows:
            dict_data = {}
            for idx in range(len(column_names)):
                key = column_names[idx]
                value = row[idx]
                if isinstance(row[idx], datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                dict_data[key] = value
            datas.append(dict_data)
        return datas

        # 获取数据库里所有的表名

    def get_db_tables(self):
        self.cursor.execute(
            f"select table_name from information_schema.TABLES where table_type='BASE TABLE' and table_schema = '{self.database}'")
        datas = []
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            return datas
        column_names = [description[0].lower() for description in self.cursor.description]
        for row in rows:
            dict_data = {}
            for idx in range(len(column_names)):
                dict_data[column_names[idx]] = row[idx]
            datas.append(dict_data)
        return datas

    def adapt_sql_for_framework(self, sql):
        sql_tokens = sqlparse.parse(sql)[0]
        adapted_tokens = []

        def process_tokens(tokens):
            nonlocal adapted_tokens
            for token in tokens:
                # 检查是否是复杂结构而非简单递归
                if isinstance(token, (Identifier, IdentifierList)):
                    adapted_tokens.append(str(token))
                elif isinstance(token, TokenList):
                    process_tokens(token.tokens)  # 使用迭代处理内部 tokens
                elif token.value.upper() == 'ISNULL':  # 修改为仅依赖 token.value 检查
                    adapted_tokens.append('IS NULL')
                else:
                    adapted_tokens.append(token.value)

        process_tokens(sql_tokens.tokens)

        # 用列表拼接时添加空格逻辑，保持原有结构的空格格式
        result = []
        for i, token in enumerate(adapted_tokens):
            if i > 0 and not (adapted_tokens[i - 1].endswith(' ') or token.startswith(' ')):
                result.append(' ')
            result.append(token)
        return ''.join(result)

    def save_or_update_data(self, table_name, data: dict, keys: list):
        new_data = {}
        for key, value in data.items():
            if isinstance(value, dict):
                value = str(value)
            new_data.setdefault(key, value)
        existing_record = None
        if keys:
            condition = ' and '.join(f"{key} = '{data.get(key)}'" for key in keys)

            select_sql = f"SELECT * FROM {table_name} WHERE {condition}"
            self.cursor.execute(select_sql, new_data)
            existing_record = self.cursor.fetchone()

        if existing_record:
            set_clause = ', '.join(f"{key} = '{data.get(key)}'" for key in data.keys())
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            self.cursor.execute(sql, new_data)
        else:
            columns = ', '.join(new_data.keys())
            placeholders = ', '.join(['%s' for _ in new_data.keys()])
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(sql, new_data)

        # 提交事务
        if self.is_commit:
            self.connection.commit()

    def save_or_update_datas(self, table_name, arr: List[dict], keys: list):
        print("save_or_update_datas开始, table_name: {}, 执行时间: {}".format(table_name,
                                                                        time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                      time.localtime())))
        # if arr:
        #     columns = ",".join(arr[0].keys())
        #     self.create_table(table_name, columns)

        add_list = []
        update_list = []
        query_list = []
        if len(keys):
            columns = ', '.join(keys)
            sql = f"SELECT {columns} FROM {table_name}"
            self.cursor.execute(sql)
            res_q = self.cursor.fetchall()
            for row in res_q:
                query_list.append('-'.join([val for val in row if val]))

        for data in arr:
            value = '-'.join(data[key] for key in keys if key in data and data[key])
            if value in query_list:
                update_list.append(data)
            else:
                add_list.append(data)

        if len(add_list) > 0:
            columns = ', '.join(add_list[0].keys())
            placeholders = ', '.join([':' + key for key in add_list[0].keys()])
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            print(f"save_or_update_datas : 执行sql1:{sql}")
            try:
                self.cursor.executemany(sql, add_list)
            except  Exception as e:
                print(traceback.format_exc(limit=None, chain=True))
                print(f'执行sql1异常：sql【{sql}】,第一条数据：【{add_list[0]}】')
                raise e
        if len(update_list) > 0:
            condition = ' and '.join(f"{key} = :{key}" for key in keys)
            set_clause = ', '.join(f"{key} = :{key}" for key in update_list[0].keys())
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            print(f"save_or_update_datas : 执行sql2:{sql}")
            try:
                self.cursor.executemany(sql, update_list)
            except  Exception as e:
                print(traceback.format_exc(limit=None, chain=True))
                print(f'执行sql2异常：sql【{sql}】,第一条数据：【{update_list[0]}】')
                raise e
        # 提交事务
        if self.is_commit:
            self.connection.commit()
        print("save_or_update_datas结束, table_name: {}, 执行时间: {}".format(table_name,
                                                                        time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                      time.localtime())))

    def __del__(self):
        """关闭数据库连接"""
        self.disconnect()
