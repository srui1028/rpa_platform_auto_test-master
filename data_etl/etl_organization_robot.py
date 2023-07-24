#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
from sqlalchemy import distinct

# from db_to_rest_compare_tools.orms.dwd_requirement import Requirement
# from db_to_rest_compare_tools.project_path import DEFAULT_ORG_LIST
from utils.search_from_db import *

def get_robot_organization_id(env, robot_id):
    """
    需求列表
    :return:
    """
    session = get_data_db_session(env)
    data_engine = get_data_db_engine(env)
    sql = "SELECT organization_id from rpa_orc_serv.organization_robot where robot_id = '" + robot_id + "'"
    # print(sql)
    statistics_list = pd.read_sql(sql, data_engine)
    session.close()
    return str(statistics_list.iat[0,0])

if __name__ == '__main__':
    print(get_robot_organization_id("huaweicloud_province", "1158744594972928"))
    # get_requirement_task_id( "65d288f5-a345-11ec-8545-fa163eee70bf")