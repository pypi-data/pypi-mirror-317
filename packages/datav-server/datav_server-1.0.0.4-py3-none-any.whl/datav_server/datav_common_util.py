import datetime

from datav_server.IdUtil import genUUID
from datav_server.bas_dic_util import TableName
from datav_server.db_factory import DatabaseFactory


def get_datav_config(user_id,mof_div_code,fiscal_year):
    db = DatabaseFactory.get_database()
    sql = f"""select * from datav_task_config where exists (select 1 from datav_task_authorize  
          where mof_div_code = '{mof_div_code}' and fiscal_year = '{fiscal_year}' and user_id = '{user_id}'
          and datav_task_config.datav_task_id = datav_task_authorize.datav_task_id
          )
          """
    configs = db.select_json_data_by_sql(sql)
    if configs:
        for temp_config in configs:
            datav_task_id = temp_config.get("datav_task_id")
            sql = f"select * from datav_task_data_sets where datav_task_id = '{datav_task_id}' and mof_div_code = '{mof_div_code}' and fiscal_year = '{fiscal_year}'"
            data_sets = db.select_json_data_by_sql(sql)
            if data_sets:
                for temp_set in data_sets:
                    data_set_id = temp_set.get("data_set_id")
                    sql = f"select * from datav_data_set_column_mapping where datav_task_id = '{datav_task_id}' and datav_set_id = '{data_set_id}'"
                    mapping = db.select_json_data_by_sql(sql)
                    if mapping:
                        temp_set["column_mapping"] = mapping
            temp_config["data_sets"] = data_sets
    return configs


def update_datav_execute_record(datav_task_id,user_id,data_count:int):
    '''
    :param datav_task_id:  datav 任务id
    :param user_id:   用户ID
    :param data_count:  更新数据的条数
    :return:
    '''
    db = DatabaseFactory.get_database()
    task_record = {
        "record_id":genUUID(),
        "datav_task_id":datav_task_id,
        "user_id":user_id,
        "record_time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "task_data_count":data_count
    }
    db.insert_data(TableName.datav_task_record,task_record)
    return "success"
