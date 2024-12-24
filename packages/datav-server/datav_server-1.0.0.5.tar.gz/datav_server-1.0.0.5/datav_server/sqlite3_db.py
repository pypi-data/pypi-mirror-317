import sqlite3
import time
import traceback
from typing import List



class SQLiteConnectionPool:
    def __init__(self, db_file, pool_size=5):
        self.db_file = db_file
        self.pool_size = pool_size
        self._create_pool()

    def _create_pool(self):
        """创建连接池"""
        self.pool = [sqlite3.connect(self.db_file) for _ in range(self.pool_size)]

    def get_connection(self):
        """从池中获取一个连接"""
        if not self.pool:
            raise Exception("No available connections")
        return self.pool.pop()

    def release_connection(self, conn):
        """将连接放回池中"""
        self.pool.append(conn)

class Sqlite3Database():
    """SQLite 数据库操作类"""

    def __init__(self, db_name, is_commit=True, pool_size=5):
        self.db_name = db_name
        self.pool = SQLiteConnectionPool(db_file=self.db_name, pool_size=pool_size)
        self.connection = None
        self.cursor = None
        self.is_commit = is_commit

    def connect(self):
        """连接到SQLite数据库"""
        self.connection = self.pool.get_connection()
        self.cursor = self.connection.cursor()

    def disconnect(self):
        """断开与SQLite数据库的连接"""
        if self.connection:
            self.pool.release_connection(self.connection)
            self.connection = None
            self.cursor = None


    def create_table(self, table_name, columns: str, types=""):
        """创建表格指定类型, 没有指定类型，默认为text, 存在科学计数法的表示情况"""
        columns_list = columns.split(",")
        if types:
            types_list = types.split(",")
        else:
            types_list = ["text" for _ in range(len(columns_list))]
        column_type_list = list()
        for column, column_type in zip(columns_list, types_list):
            column_type_list.append(f"{column.strip()} {column_type.strip()}")
        column_type_str = ",".join(column_type_list)
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_type_str})"
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
        """插入数据"""
        columns = ', '.join(data.keys())
        placeholders = ':' + ', :'.join(data.keys())
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        print(f"执行sql：{sql}")
        new_data = {}
        for key,value in data.items():
            if isinstance(value, dict):
                value = str(value)
            new_data.setdefault(key,value)
        self.cursor.execute(sql, new_data)
        if self.is_commit:
            self.connection.commit()

    def insert_datas(self, table_name, data: []):
        print("insert_datas开始, table_name: {}, 执行时间: {}".format(table_name, time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                                time.localtime())))
        """插入数据"""
        columns = ', '.join(data[0].keys())
        placeholders = ', '.join([':' + key for key in data[0].keys()])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.executemany(sql, data)
        if self.is_commit:
            self.connection.commit()
        print("insert_datas结束, table_name: {}, 执行时间: {}".format(table_name, time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                                time.localtime())))

    def update_data(self, table_name, data: dict, condition):
        """更新数据"""
        set_clause = ', '.join(f"{key} = :{key}" for key in data.keys())
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        print(f"update_data方法执行sql:{sql}")
        self.cursor.execute(sql, data)
        if self.is_commit:
            self.connection.commit()

    def update_datas(self, table_name, data: [], keys: list):
        print("update_datas开始, table_name: {}, 执行时间: {}".format(table_name, time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                                time.localtime())))
        condition = ' and '.join(f"{key} = :{key}" for key in keys)
        """更新数据"""
        set_clause = ', '.join(f"{key} = :{key}" for key in data[0].keys())
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        self.cursor.executemany(sql, data)
        if self.is_commit:
            self.connection.commit()
        print("update_datas开始, table_name: {}, 执行时间: {}".format(table_name, time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                                time.localtime())))

    def save_or_update_data(self, table_name, data: dict, keys: list):
        new_data = {}
        for key,value in data.items():
            if isinstance(value, dict):
                value = str(value)
            new_data.setdefault(key,value)
        existing_record = None
        if keys:
            condition = ' and '.join(f"{key} = :{key}" for key in keys)

            select_sql = f"SELECT * FROM {table_name} WHERE {condition}"
            self.cursor.execute(select_sql, new_data)
            existing_record = self.cursor.fetchone()

        if existing_record:
            set_clause = ', '.join(f"{key} = :{key}" for key in data.keys())
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            self.cursor.execute(sql, new_data)
        else:
            columns = ', '.join(new_data.keys())
            placeholders = ':' + ', :'.join(new_data.keys())
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(sql, new_data)

        # 提交事务
        if self.is_commit:
            self.connection.commit()

    def save_or_update_datas(self, table_name, arr: List[dict], keys: list):
        print("save_or_update_datas开始, table_name: {}, 执行时间: {}".format(table_name,
                                                                              time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                           time.localtime())))
        if arr:
            columns = ",".join(arr[0].keys())
            self.create_table(table_name, columns)

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

    # def save_or_update_datas(self, table_name, arr: List[dict], keys: list):
    #     condition = ' and '.join(f"{key} = :{key}" for key in keys)
    #
    #     # 使用事务来提高性能并确保数据完整性
    #     self.conn.execute('BEGIN TRANSACTION')
    #     for data in arr:
    #         select_sql = f"SELECT * FROM {table_name} WHERE {condition}"
    #         self.cursor.execute(select_sql, data)
    #         existing_record = self.cursor.fetchone()
    #
    #         if existing_record:
    #             set_clause = ', '.join(f"{key} = :{key}" for key in data.keys())
    #             sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
    #             self.cursor.execute(sql, data)
    #         else:
    #             columns = ', '.join(data.keys())
    #             placeholders = ':' + ', :'.join(data.keys())
    #             sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    #             self.cursor.execute(sql, data)
    #     # 提交事务
    #     if self.is_commit:
    #         self.connection.commit()

    def delete_data(self, table_name, condition):
        """删除数据"""
        sql = f"DELETE FROM {table_name} WHERE {condition}"
        print(f"删除方法执行语句：{sql}")
        self.cursor.execute(sql)
        if self.is_commit:
            self.connection.commit()

    def select_data(self, table_name, columns=None, condition=None, order_by=None):
        """
        查询数据
        order_by : "age ASC, hits DESC"  age按照升序排序，hits按照降序排序
        """
        if columns is None:
            columns = '*'
        if condition is None:
            condition = ''
        else:
            condition = f"WHERE {condition}"
        if not order_by:
            order_by = ""
        else:
            order_by = f"ORDER BY {order_by}"

        sql = f"SELECT {columns} FROM {table_name} {condition} {order_by}"

        print("执行脚本--》 {}", sql)

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    """
    去重查询列
    """
    def select_distinct_column(self,table_name,column):
        if column is None:
            column = "*"

        sql = f"select distinct {column} from {table_name} where {column} is not null"
        print("执行脚本--》 {}", sql)

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def column_exists(self, table_name, column_name):
        """
        判断列名是否存在
        :param table_name:
        :param column_name:
        :return:
        """
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        existing_columns = [row[1] for row in self.cursor.fetchall()]
        return column_name in existing_columns

    def table_exists(self,table_name):
        """
        判断 表是否存在
        """
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        existing_table = [row[0] for row in self.cursor.fetchall()]
        if existing_table:
            return True
        else:
            return False
    def get_all_columns(self, table_name):
        """
        获取表中的所有列
        """
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        existing_columns = [row[1] for row in self.cursor.fetchall()]
        return existing_columns

    def insert_column(self, table_name, new_column, column_type):
        """
        表中插入新的列,SQLite不支持同时增加多个列，一次只能增加一列。
        :param table_name:
        :param new_column:
        :param column_type: TEXT,INT
        :return:
        """
        self.cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {new_column} {column_type}")

    def select_json_data(self, table_name, columns=None, condition=None):
        """查询数据 返回格式为key value格式"""
        if columns is None:
            columns = '*'
        if condition is None:
            condition = ''
        else:
            condition = f"WHERE {condition}"
        sql = f"SELECT {columns} FROM {table_name} {condition}"

        print("执行脚本--》 {}", sql)
        result = self.cursor.execute(sql)
        datas = []
        rows = result.fetchall()
        if len(rows) == 0:
            return datas
        column_names = [description[0] for description in self.cursor.description]
        for row in rows:
            dict_data = {}
            for idx in range(len(column_names)):
                dict_data[column_names[idx]] = row[idx]
            datas.append(dict_data)

        print('查询的json数据,查看前1行 --》 {}', datas[:1])
        return datas

    def delete_column(self, table_name, delete_column):
        """
        删除列
        :param table_name:
        :param delete_column:
        :return:
        """

        self.cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {delete_column}")
        print(f"删除表{table_name}中列名{delete_column}成功")

    def column_number_sum(self, table_name, column):
        """
        列求和
        :param table_name:
        :param column:
        :return:
        """
        total = self.cursor.execute(f"SELECT SUM({column}) FROM {table_name}")
        return total.fetchone()[0]

    def count(self, table_name, condition):
        """
        按条件统计
        :param table_name:
        :param condition:
        :return:
        """
        if not table_name:
            return 0
        if not condition:
            condition = ""
        sql = f"SELECT  count(1)  FROM {table_name} {condition}"
        print("执行脚本--》 {}", sql)
        result = self.cursor.execute(sql)
        datas = []
        rows = result.fetchall()
        if len(rows) == 0:
            return 0
        else:
            return rows[0][0]

    def select_json_data_by_sql(self, sql):
        """
        传入sql查询
        :param sql:
        :return:
        """
        if not sql:
            return None
        else:
            print("执行脚本---》{}", sql)
        result = self.cursor.execute(sql)
        datas = []
        rows = result.fetchall()
        if len(rows) == 0:
            return datas
        column_names = [description[0] for description in self.cursor.description]
        for row in rows:
            dict_data = {}
            for idx in range(len(column_names)):
                dict_data[column_names[idx]] = row[idx]
            datas.append(dict_data)

        print('查询的json数据,查看前1行 --》 {}', datas[:1])
        return datas



    def business_less_than(self, business_count, user_code, data_date, month, fiscal_year):
        """
        业务操作少于的条数
        :param data_date:
        :param month:
        :param fiscal_year:
        :param business_count:
        :param user_code:
        :return:
        """
        print("business_less_than 方法")
        if not business_count or not user_code:
            return []
        sql = f"select sum(business_count) as business_count,user_code,data_date from user_operate_business_log " \
              f"group by user_code,fiscal_year,data_date having business_count < {business_count} and fiscal_year = {fiscal_year} and data_month = {month} and user_code <> '{user_code}' and data_date = '{data_date}'"
        print("执行脚本---》{}", sql)
        result = self.cursor.execute(sql)
        rows = result.fetchall()
        return len(rows)

    def count_login_count_by_date(self, user_code, date_str):

        sql = f"select (data_month||'.'||data_date) as real_date,login_count  from user_operate_system_log" \
              f" where user_code = '{user_code}' and real_date in ({date_str})  order by real_date asc"
        print("执行脚本---》{}", sql)
        datas = []
        result = self.cursor.execute(sql)
        rows = result.fetchall()
        if len(rows) == 0:
            return datas
        column_names = [description[0] for description in self.cursor.description]
        for row in rows:
            dict_data = {}
            for idx in range(len(column_names)):
                dict_data[column_names[idx]] = row[idx]
            datas.append(dict_data)

        print('查询的json数据,查看前1行 --》 {}', datas[:1])
        return datas

    def count_business_count_by_date(self, user_code, date_str):

        sql = f"select (data_month||'.'||data_date) as real_date,sum(business_count) as business_count " \
              f"from user_operate_business_log where user_code = '{user_code}' and real_date  in ({date_str}) GROUP BY real_date  order by real_date asc"
        print("执行脚本---》{}", sql)
        datas = []
        result = self.cursor.execute(sql)
        rows = result.fetchall()
        if len(rows) == 0:
            return datas
        column_names = [description[0] for description in self.cursor.description]
        for row in rows:
            dict_data = {}
            for idx in range(len(column_names)):
                dict_data[column_names[idx]] = row[idx]
            datas.append(dict_data)

        print('查询的json数据,查看前1行 --》 {}', datas[:1])
        return datas

    def count_by_business_name(self, user_code, fiscal_year, month, day):
        sql = f"select business_name as name,business_count as value from user_operate_business_log where user_code = '{user_code}' " \
              f"and fiscal_year = {fiscal_year} and data_month = {month} and data_date = {day}  group by name "
        print("执行脚本---》{}", sql)
        datas = []
        result = self.cursor.execute(sql)
        rows = result.fetchall()
        if len(rows) == 0:
            return datas
        column_names = [description[0] for description in self.cursor.description]
        for row in rows:
            dict_data = {}
            for idx in range(len(column_names)):
                dict_data[column_names[idx]] = row[idx]
            datas.append(dict_data)

        print('查询的json数据,查看前1行 --》 {}', datas[:1])
        return datas

    def count_by_menu_name(self, user_code, fiscal_year, month, day):
        sql = f"select menu_name as name,business_count as value from user_operate_business_log where user_code = '{user_code}' " \
              f"and fiscal_year = {fiscal_year} and data_month = {month} and data_date = {day}  group by name "
        print("执行脚本---》{}", sql)
        datas = []
        result = self.cursor.execute(sql)
        rows = result.fetchall()
        if len(rows) == 0:
            return datas
        column_names = [description[0] for description in self.cursor.description]
        for row in rows:
            dict_data = {}
            for idx in range(len(column_names)):
                dict_data[column_names[idx]] = row[idx]
            datas.append(dict_data)

        print('查询的json数据,查看前1行 --》 {}', datas[:1])
        return datas

    def money_by_menu_name(self, user_code, fiscal_year, month, day):
        sql = f"select menu_name as name,sum(business_money) as value from user_operate_business_log where user_code = '{user_code}' " \
              f"and fiscal_year = {fiscal_year} and data_month = {month} and data_date = {day}  group by name "
        print("执行脚本---》{}", sql)
        datas = []
        result = self.cursor.execute(sql)
        rows = result.fetchall()
        if len(rows) == 0:
            return datas
        column_names = [description[0] for description in self.cursor.description]
        for row in rows:
            dict_data = {}
            for idx in range(len(column_names)):
                dict_data[column_names[idx]] = row[idx]
            datas.append(dict_data)

        print('查询的json数据,查看前1行 --》 {}', datas[:1])
        return datas

    def money_by_business_name(self, user_code, fiscal_year, month, day):
        sql = f"select business_name as name,sum(business_money) as value from user_operate_business_log where user_code = '{user_code}' " \
              f"and fiscal_year = {fiscal_year} and data_month = {month} and data_date = {day}  group by name "
        print("执行脚本---》{}", sql)
        datas = []
        result = self.cursor.execute(sql)
        rows = result.fetchall()
        if len(rows) == 0:
            return datas
        column_names = [description[0] for description in self.cursor.description]
        for row in rows:
            dict_data = {}
            for idx in range(len(column_names)):
                dict_data[column_names[idx]] = row[idx]
            datas.append(dict_data)

        print('查询的json数据,查看前1行 --》 {}', datas[:1])
        return datas

    def executesql(self,sql):
        print(f"executesql 方法执行sql：{sql}")
        self.cursor.execute(sql)
        if self.is_commit:
            self.connection.commit()

    def update_hits_by_sql(self, table_name, hits_count, condition):
        print("执行update_hits_by_sql方法")
        sql = f"update {table_name} set hits = hits+{hits_count} "
        if condition is not None and condition != '':
            sql = sql + f"  {condition}"
            print(f"执行sql语句:{sql}")
            self.cursor.execute(sql)
            if self.is_commit:
                self.connection.commit()
        else:
            pass

    def select_talk_info(self, mec_mac,user_id):
        """查询数据 返回格式为key value格式"""
        condition = ""
        if mec_mac is not None and mec_mac !="":
            condition = f" and mec_mac = '{mec_mac}'"
        if user_id is not None and user_id !="":
            condition = condition + f" and user_id = '{user_id}'"
        sql = f"select * from talk_info where question is not null  {condition} order by create_time desc"
        print("执行脚本--》 {}", sql)
        result = self.cursor.execute(sql)
        datas = []
        rows = result.fetchall()
        if len(rows) == 0:
            return datas
        column_names = [description[0] for description in self.cursor.description]
        for row in rows:
            dict_data = {}
            for idx in range(len(column_names)):
                dict_data[column_names[idx]] = row[idx]
            datas.append(dict_data)

        print('查询的json数据,查看前1行 --》 {}', datas[:1])
        return datas

    # 批量执行脚本
    def execute_script(self,sqls):
        self.cursor.executescript(sqls)
        if self.is_commit:
            self.connection.commit()



    def create_special_table(self):
        sql = f"select ele_table_source   from ele_catalog "
        # sql = f"PRAGMA table_info(ba_bgt_info)"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result


    def name_table(self,data):

        all_data = []
        for na in data:
            sql = "select ele_name, synonyms   from {} ".format(na)
            # sql = f"PRAGMA table_info(ba_bgt_info)"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            for re in result:
                if re[0] != None and re[0] != '':
                    all_data.append(re[0])
                if re[1] !=None and re[1] != '':
                    all_data.extend(re[1].split(','))

        return all_data
    #bas_dic_cols
    def bas_dic_cols(self):
        sql = f"select title, synonyms   from bas_dic_cols "
        # sql = f"PRAGMA table_info(ba_bgt_info)"

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        all_data = []
        for re in result:
            if re[0] != None and re[0] != '':
                all_data.append(re[0])
            if re[1] != None and re[1] != '':
                all_data.extend(re[1].split(','))

        return all_data
    #bas_synonyms
    def bas_synonyms(self):
        sql = f"select synonyms   from bas_synonyms "
        # sql = f"PRAGMA table_info(ba_bgt_info)"

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        all_data = []
        for re in result:
            if re[0] != None and re[0] != '':
                all_data.append(re[0])
        return all_data
    def que_table(self):

        sql = f"select question, key_word, synonyms   from work_sheet_info "
        # sql = f"PRAGMA table_info(ba_bgt_info)"

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        data = []
        for re in result:
            if re[0] !=None and re[0] != '':
                data.append(re[0])
            if re[1] !=None and re[1] != '':
                data.extend(re[1].split(','))
            if re[2] !=None and re[2] != '':
                data.extend(re[2].split(','))
            # print(data)
        # print(data)
        return data

    # app_info
    def app_info(self):
        sql = f"select app_name   from app_info "
        # sql = f"PRAGMA table_info(ba_bgt_info)"

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        all_data = []
        for re in result:
            if re[0] !=None and re[0] != '':
                all_data.append(re[0])
        # print(all_data)
        return all_data
    # menu_info
    def menu_info(self):
        sql = f"select  name   from menu_info "
        # sql = f"PRAGMA table_info(ba_bgt_info)"

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        all_data = []
        for re in result:
            if re[0] !=None and re[0] != '':
                all_data.append(re[0])
        # print(len(all_data))
        return all_data

    def __del__(self):
        self.disconnect()