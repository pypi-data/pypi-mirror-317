from abc import ABCMeta, abstractmethod
from typing import List


class CommonDatabase(metaclass=ABCMeta):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def create_table(self, table_name, columns: str):
        pass

    @abstractmethod
    def table_exists(self, table_name):
        pass

    @abstractmethod
    def executesql(self, sql: str):
        pass

    @abstractmethod
    def drop_table(self, table_name):
        pass

    @abstractmethod
    def insert_data(self, table_name, data: dict):
        pass

    @abstractmethod
    def insert_datas(self, table_name, data: []):
        pass

    @abstractmethod
    def update_data(self, table_name, data: dict, condition):
        pass

    @abstractmethod
    def update_datas(self, table_name, data: [], condition):
        pass

    @abstractmethod
    def delete_data(self, table_name, condition):
        pass

    @abstractmethod
    def select_data(self, table_name, columns=None, condition=None):
        pass

    @abstractmethod
    def select_json_data(self, table_name, columns=None, condition=None):
        pass

    @abstractmethod
    def get_create_table(self, table_name):
        pass

    @abstractmethod
    def get_cols_by_table_name(self, table_name):
        pass

    @abstractmethod
    def select_data_with_sql(self, sql):
        pass
    # 获取数据库内所有的表名
    @abstractmethod
    def get_db_tables(self, sql):
        pass

    @abstractmethod
    def select_json_data_by_sql(self, sql):
        pass

    @abstractmethod
    def adapt_sql_for_framework(self, sql):
        pass