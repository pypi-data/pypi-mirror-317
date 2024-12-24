

#根据配置初始化数据库
import configparser
import os
import platform
import sys

from datav_server.sqlite3_db import Sqlite3Database

from datav_server.mysql_db import MySQLConnectionPool, MySQLDatabase


class DatabaseFactory:
    @staticmethod
    def get_database(input_db=None,is_commit=True):
        config = get_database_config()
        db_type = config['db_type']
        if input_db:
            db_type = input_db
        if db_type == "sqlite":
            exe_dir = get_exe_path()
            db_name = os.path.join(exe_dir, "data.db")
            db_name = get_real_path(db_name)
            database = Sqlite3Database(db_name,is_commit)
        elif db_type == "mysql":
            host = config['host']
            port = config['port']
            user = config['user']
            password = config['password']
            database = config['database']
            database = MySQLDatabase(host, port, user, password, database, is_commit, pool_size=5)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

        # 创建数据库实例后立即连接数据库
        database.connect()
        return database


def get_database_config():
    exe_dir = get_exe_path()
    filepath = os.path.join(exe_dir, 'config.ini')
    filepath = get_real_path(filepath)
    cp = configparser.ConfigParser()
    cp.read(filepath,encoding='utf-8')
    return cp['database']


def get_exe_path():
    exe_path = sys.executable
    # 获取当前脚本或exe文件所在的目录
    exe_dir = os.path.dirname(exe_path)
    cur_os = get_cur_platform()
    if not exe_dir.endswith("/") or not exe_dir.endswith("\\"):
        if cur_os == "Windows":
            exe_dir += "\\static_files\\"
        else:
            exe_dir += "/static_files/"
    else:
        if cur_os == "Windows":
            exe_dir += "static_files\\"
        else:
            exe_dir += "static_files/"
    return exe_dir

# path转换，正常传进来的是window的路径，此方法用来转为当前操作系统的路径
def get_real_path(path: str):
    cur_os = get_cur_platform()
    if cur_os == "Windows":
        path = path.replace("/", "\\")
    else:
        path = path.replace("\\", "/")
    return path


def get_cur_platform():
    # Windows Linux
    current_os = platform.system()
    return current_os

global_pools = None
def init_db_pool():
    # 建立连接池
    config = get_database_config()
    host = config['host']
    port = config['port']
    user = config['user']
    password = config['password']
    database = config['database']
    db_type = config['db_type']
    if db_type == "mysql":
        global global_pools
        global_pools = MySQLConnectionPool(host, port, user, password, database, pool_size=20)