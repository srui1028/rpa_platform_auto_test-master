#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
from sqlalchemy import distinct

# from db_to_rest_compare_tools.orms.dwd_requirement import Requirement
# from db_to_rest_compare_tools.project_path import DEFAULT_ORG_LIST
from utils.common_tools import CommonTool
from utils.search_from_db import *


def get_requirement_id(env, process_instance_id):
    '''
    获取需求id
    :param env:
    :param process_instance_id:
    :return:
    '''
    session = get_data_db_session(env)
    data_engine = get_data_db_engine(env)
    sql = "SELECT id from data_entity.requirement where process_instance_id = '" + process_instance_id + "'"
    # sql = "SELECT id from data_entity.requirement where process_instance_id = '65d288f5-a345-11ec-8545-fa163eee70bf'"
    # print(sql)
    statistics_list = pd.read_sql(sql, data_engine)
    session.close()
    return statistics_list.iat[0,0]



if __name__ == '__main__':
    print(get_requirement_id("huaweicloud_master", "65d288f5-a345-11ec-8545-fa163eee70bf"))
    # get_requirement_task_id( "65d288f5-a345-11ec-8545-fa163eee70bf")