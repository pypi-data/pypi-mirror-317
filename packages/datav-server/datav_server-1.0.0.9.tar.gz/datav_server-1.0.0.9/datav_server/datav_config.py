import json
import traceback

from flask import Blueprint, request

from datav_server import get_datav_config, update_datav_execute_record, insert_info_and_cols_by_json, \
    check_exists_dic_info_and_table
from datav_server.res_info_util import DataVWebResInfo

app = Blueprint('datav_config', __name__)


@app.route("/get_datav_config",methods=["GET"])
def get_datav_config_rest():
    header = request.headers
    user_info = header.get("userinfo")
    if not user_info:
        DataVWebResInfo.error("","用户信息为空")
    user_info = json.loads(user_info)

    result = get_datav_config(user_info.get("user_id"),user_info.get("mof_div_code"),user_info.get("fiscal_year"))
    return DataVWebResInfo.success(result)

@app.route("/update_datav_execute_record",methods=["POST"])
def update_datav_execute_record_rest():
    param = request.json
    datav_task_id= param.get("datav_task_id")
    user_id = param.get("user_id")
    data_count = param.get("data_count")
    update_datav_execute_record(datav_task_id,user_id,data_count)
    return DataVWebResInfo.success()



@app.route("/insert_info_and_cols_by_json_handler", methods=['POST'])
def insert_info_and_cols_by_json_handler():
    param = request.json
    header = request.headers
    user_info = header.get("userinfo")
    if not user_info:
        DataVWebResInfo.error("","用户信息为空")
    user_info = json.loads(user_info)
    try:
        insert_info_and_cols_by_json(user_info.get("user_id"),
                                     user_info.get("fiscal_year"),
                                     user_info.get("mof_div_code"),
                                     param.get("data"),
                                     param.get("table_name"),
                                     param.get("dic_type"),
                                     param.get("dict_code"),
                                     param.get("dict_name"),
                                     param.get("appguid"),
                                     param.get("menu_name"),
                                     param.get("column_type"),
                                     param.get("column_name"),
                                     param.get("dic_id"))
    except Exception as e:
        print("创建表失败############")
        print(traceback.format_exc(limit=None, chain=True))
        return DataVWebResInfo.error("","创建表失败："+traceback.format_exc(limit=None, chain=True))
    return DataVWebResInfo.success()

@app.route("/check_exists_dic_info_and_table_by_table_name", methods=['GET'])
def check_exists_dic_info_and_table_by_table_name():
    args = request.args
    if not args.get("tableName"):
        return DataVWebResInfo.error("","表名为空")
    header = request.headers
    user_info = header.get("userinfo")
    if not user_info:
        DataVWebResInfo.error("","用户信息为空")
    user_info = json.loads(user_info)
    dic_info,dic_cols,table = check_exists_dic_info_and_table(args.get("tableName"),user_info.get("fiscal_year"),user_info.get("mof_div_code"))
    result = {
        "dic_cols":dic_cols,
        "dic_info":dic_info,
        "table":table
    }
    return DataVWebResInfo.success(result)


