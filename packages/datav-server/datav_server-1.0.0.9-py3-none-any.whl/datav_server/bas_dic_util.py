import datetime
import uuid

from datav_server.db_factory import DatabaseFactory

"""
返回三个值 
第一个 bas_dic_info 数据是否存在
第二个 bas_dic_cols 数据是否存在
第三个 数据库表是否存在
其实如果第三个验证数据库表不存在的话 可以将bas_dic_info表 和 bas_dic_cols 表数据删除后重新创建
不想浪费时间搞这些逻辑  先按上边说的这么弄
"""
def check_exists_dic_info_and_table(table_name,fiscal_year,mof_div_code):
    if not table_name:
        print("check_exists_dic_info_and_table："+"表名为空")
        return True
    db = DatabaseFactory.get_database()
    common_condition = f"fiscal_year = '{fiscal_year}'  and mof_div_code = '{mof_div_code}'"
    condition = f" {common_condition} and data_source_table = '{table_name}' "
    dic_info = db.select_json_data(TableName.bas_dic_info,None,condition)
    condition = f"{common_condition} and dic_id in (select guid from bas_dic_info where data_source_table = '{table_name}')"
    dic_cols = db.select_json_data(TableName.bas_dic_cols,None,condition)
    table = db.table_exists(table_name)
    return dic_info,dic_cols,table


def insert_info_and_cols_by_json(user_id,fiscal_year,mof_div_code,data:dict,table_name:str,dic_type='',dict_code='',
                                 dict_name='',appguid='',menu_name='',column_type={},column_name={},dic_id=''):
    if not data:
        print("调用生成bas_dic_info and bas_dic_cols 方法数据为空")
        raise Exception("调用生成bas_dic_info and bas_dic_cols 方法数据为空")
    if not table_name:
        print("调用生成bas_dic_info and bas_dic_cols 方法表名为空")
        raise Exception("调用生成bas_dic_info and bas_dic_cols 方法表名为空")
    if not dic_id:
        dic_id = str(uuid.uuid4()).replace("-", "")

    bas_dic_info = {
        "guid": dic_id,
        "dic_code": dict_code,
        "dic_name": dict_name,
        "parent_id": "0",
        "remark": dict_name,
        "order_num": "",
        "dic_type": dic_type,
        "editable": "1",
        "ischeck": "1",
        "isfolder": "0",
        "kind": "2",
        "systemflag": "",
        "creater": user_id,
        "updater": "DAE09256C08249ECAED6D3CD8900F64A",
        "create_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "is_deleted": "2",
        "mof_div_code": mof_div_code,
        "fiscal_year": fiscal_year,
        "is_imate_form": None,
        "is_leaf": None,
        "dic_id": "",
        "menu_name": menu_name,
        "data_source_table": table_name,
        "row_high": None,
        "is_init_table": "2",
        "appguid": appguid,
        "reportlet": ""
    }
    columns = data.keys()
    if not columns:
        print("调用生成bas_dic_info and bas_dic_cols 数据的key为空")
        raise Exception(":调用生成bas_dic_info and bas_dic_cols 数据的key为空")
    bas_dic_cols = []
    bas_dic_cols_id = {} #父子关系
    for index,temp in enumerate(columns):
        cols_id = str(uuid.uuid4()).replace("-", "")
        bas_dic_cols_id[temp]= cols_id
        temp_cols = {
            "guid": cols_id,
            "dic_id": dic_id,
            "field": "",
            "title": column_name.get(temp),
            "title_tip": "",
            "parent_id": "0",
            "remark": column_name.get(temp),
            "order_num": index,
            "type": "2",
            "clengh": "200",
            "editable": "0",
            "disabled": "1",
            "align": "left",
            "sortable": "0",
            "visible": "1",
            "required": "0",
            "options": "",
            "width": "180",
            "placeholder": "",
            "default_value": "",
            "formula": "",
            "calcpri": "",
            "creater": "",
            "updater": "",
            "create_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "is_deleted": "2",
            "mof_div_code": mof_div_code,
            "fiscal_year": fiscal_year,
            "column_name": temp,
            "formula_show": "",
            "is_export_col": "1",
            "graded_summary": None,
            "fixed": "",
            "is_search_col": None,
            "constraint_exp": "",
            "is_standard": None,
            "synonyms": "",
            "isleaf": "1",
            "col_option_type": "",
            "level": "99",
            "level_summary": "1",
            "show_code": "2"
        }
        bas_dic_cols.append(temp_cols)
    db = DatabaseFactory.get_database()
    sql = f"delete from bas_dic_info where guid = '{dic_id}'"
    db.executesql(sql)
    sql = f"delete from bas_dic_cols where dic_id = '{dic_id}'"
    db.executesql(sql)
    sql = f"drop table if exists {table_name}"
    db.executesql(sql)
    # 先删除后新增
    db.insert_data(TableName.bas_dic_info, bas_dic_info)
    db.insert_datas(TableName.bas_dic_cols, bas_dic_cols)
    columns = list(columns)
    columns.append("user_id")
    columns.append("mof_div_code")
    columns.append("fiscal_year")
    columns = list(set(columns))
    db.create_table(table_name=table_name,columns = ','.join(list(columns)))


class TableName:

    bas_dic_info = "bas_dic_info"
    bas_dic_cols = "bas_dic_cols"
    datav_task_record = "datav_task_record"